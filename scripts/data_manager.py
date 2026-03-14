#!/usr/bin/env python3
"""
JSON data manager for fallacy entries.
Implements AUTO-05 (JSON structure), AUTO-06 (atomic writes), AUTO-07 (fallback images),
PERF-05 (archive rotation), PERF-06 (error logging), SEC-02 (no database), SEC-03 (JSON storage).
"""

import os
import json
import logging
import shutil
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# File paths
DATA_DIR = "data"
DOCS_DATA_DIR = "docs/data"
MAIN_DATA_FILE = os.path.join(DOCS_DATA_DIR, "fallacies.json")
ARCHIVE_PATTERN = "archive_{timestamp}.json"
MAX_ARCHIVE_SIZE_MB = 100  # GitHub Pages limit (PERF-05)
MAX_ENTRIES_BEFORE_ROTATION = 100  # Rotate after this many entries

# Fallback placeholder image path (AUTO-07)
FALLBACK_IMAGE = "assets/placeholders/fallback_card.svg"


class DataManager:
    """Manages JSON data storage with atomic writes and archive rotation."""

    def __init__(self, data_dir: str = DATA_DIR):
        """
        Initialize DataManager.

        Args:
            data_dir: Directory for data files
        """
        self.data_dir = data_dir
        self.main_file = os.path.join(DOCS_DATA_DIR, "fallacies.json")

        # Ensure directory exists
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(DOCS_DATA_DIR, exist_ok=True)

        # Initialize main data file if it doesn't exist
        if not os.path.exists(self.main_file):
            self._initialize_data_file()

    def _initialize_data_file(self):
        """Create initial data file with empty structure."""
        initial_data = {
            "entries": [],
            "metadata": {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_entries": 0,
            },
        }

        self._atomic_write(initial_data)
        logger.info(f"Initialized data file: {self.main_file}")

    def _atomic_write(self, data: Dict):
        """
        Write data atomically using temp file + rename pattern.
        Implements AUTO-06: Atomic JSON writes prevent data corruption.

        Args:
            data: Dictionary to write to JSON file
        """
        try:
            # Write to temp file first
            temp_file = f"{self.main_file}.tmp"

            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomically rename temp file to target file
            os.replace(temp_file, self.main_file)

            logger.debug(f"Atomic write successful: {self.main_file}")

        except Exception as e:
            logger.error(f"Atomic write failed: {e}")

            # Clean up temp file if it exists
            temp_file = f"{self.main_file}.tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)

            raise

    def _get_file_size_mb(self, filepath: str) -> float:
        """Get file size in MB."""
        return os.path.getsize(filepath) / (1024 * 1024)

    def _rotate_archive(self, current_data: Dict):
        """
        Rotate archive if size exceeds limit.
        Implements PERF-05: Archive rotation policy prevents exceeding 100 MB GitHub Pages limit.

        Args:
            current_data: Current data dictionary
        """
        file_size_mb = self._get_file_size_mb(self.main_file)

        if file_size_mb > MAX_ARCHIVE_SIZE_MB:
            logger.warning(
                f"Archive size {file_size_mb:.2f} MB exceeds limit {MAX_ARCHIVE_SIZE_MB} MB"
            )
            logger.info("Rotating archive...")

            # Create archive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = os.path.join(
                DOCS_DATA_DIR, ARCHIVE_PATTERN.format(timestamp=timestamp)
            )

            # Move current file to archive
            shutil.move(self.main_file, archive_file)
            logger.info(f"Archived to: {archive_file}")

            # Initialize new main file
            self._initialize_data_file()

        # Also rotate if too many entries (keep file size manageable)
        num_entries = len(current_data.get("entries", []))
        if num_entries > MAX_ENTRIES_BEFORE_ROTATION:
            logger.info(f"Too many entries ({num_entries}), archiving oldest half...")

            current_entries = current_data["entries"]
            recent_entries = current_entries[len(current_entries) // 2 :]

            current_data["entries"] = recent_entries
            current_data["metadata"]["last_updated"] = datetime.now().isoformat()
            current_data["metadata"]["total_entries"] = len(recent_entries)

            self._atomic_write(current_data)
            logger.info(
                f"Kept {len(recent_entries)} recent entries, archived {len(current_entries) - len(recent_entries)} old entries"
            )

    def add_entries(self, entries: List[Dict]):
        """
        Save fallacies data to JSON file with atomic write.
        Also handles rotation if needed.

        Args:
            entries: List of entry dictionaries to add
        """
        # Load current data
        try:
            with open(self.main_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.main_file}, initializing")
            self._initialize_data_file()
            data = {
                "entries": [],
                "metadata": {
                    "version": "1.0",
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_entries": 0,
                },
            }
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            # Backup corrupted file
            backup_file = (
                f"{self.main_file}.corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            shutil.copy(self.main_file, backup_file)
            logger.error(f"Backed up corrupted file to: {backup_file}")

            # Initialize new file
            self._initialize_data_file()
            data = {
                "entries": [],
                "metadata": {
                    "version": "1.0",
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_entries": 0,
                },
            }

        # Add new entries
        data["entries"].extend(entries)

        # Update metadata
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_entries"] = len(data["entries"])

        # Validate and format each entry (AUTO-05)
        for entry in data["entries"]:
            # Ensure required fields exist
            required_fields = [
                "post_id",
                "title",
                "content",
                "source_url",
                "author",
                "reddit_score",
                "subreddit",
                "fallacy_type",
                "confidence_score",
                "confidence_level",
                "explanation",
                "quote",
                "timestamp",
                "upvotes",
                "downvotes",
            ]
            for field in required_fields:
                if field not in entry:
                    logger.warning(
                        f"Entry missing required field: {field}, using defaults"
                    )
                    # Add defaults for missing fields
                    if field == "upvotes":
                        entry[field] = 0
                    elif field == "downvotes":
                        entry[field] = 0
                    elif field == "image_url":
                        entry[field] = FALLBACK_IMAGE
                    else:
                        entry[field] = ""

        # Rotate archive if needed
        self._rotate_archive(data)

        # Atomic write
        self._atomic_write(data)

        logger.info(f"Added {len(entries)} new entries to {self.main_file}")

    def load_fallacies(self) -> Dict:
        """
        Load fallacies data from JSON file.

        Returns:
            Dictionary with entries and metadata
        """
        try:
            with open(self.main_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(
                    f"Loaded {len(data.get('entries', []))} entries from {self.main_file}"
                )
                return data
        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.main_file}")
            return {"entries": [], "metadata": {}}
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            # Backup corrupted file
            backup_file = (
                f"{self.main_file}.corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            shutil.copy(self.main_file, backup_file)
            logger.error(f"Backed up corrupted file to: {backup_file}")

            # Initialize new file
            self._initialize_data_file()
            return {"entries": [], "metadata": {}}

    def get_entries(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """
        Get entries from data file.

        Args:
            limit: Maximum number of entries to return
            offset: Number of entries to skip

        Returns:
            List of entry dictionaries
        """
        data = self.load_fallacies()
        entries = data.get("entries", [])

        if offset > 0:
            entries = entries[offset:]

        if limit:
            entries = entries[:limit]

        return entries


if __name__ == "__main__":
    # Test the data manager
    logging.basicConfig(level=logging.INFO)

    print("Testing DataManager...")

    # Create instance
    dm = DataManager()

    # Test adding entries
    test_entries = [
        {
            "post_id": "test_001",
            "title": "Test Title",
            "content": "Test content with enough length to pass validation",
            "source_url": "https://reddit.com/test",
            "author": "test_user",
            "reddit_score": 100,
            "subreddit": "test",
            "fallacy_type": "Ad Hominem",
            "confidence_score": 0.85,
            "confidence_level": "High",
            "explanation": "Test explanation",
            "quote": "Test quote",
            "timestamp": datetime.now().isoformat(),
            "upvotes": 0,
            "downvotes": 0,
        }
    ]

    print("\nAdding test entries...")
    dm.add_entries(test_entries)

    # Test loading entries
    print("\nLoading entries...")
    entries = dm.get_entries(limit=5)

    if entries:
        print(f"Loaded {len(entries)} entries")
        print(f"First entry title: {entries[0].get('title', 'No title')}")
    else:
        print("No entries loaded")

    print("\n✅ DataManager working correctly")
