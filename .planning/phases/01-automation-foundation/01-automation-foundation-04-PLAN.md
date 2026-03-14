---
phase: 01-automation-foundation
plan: 04
type: execute
wave: 2
depends_on: [01-automation-foundation-02, 01-automation-foundation-03]
files_modified: [scripts/data_manager.py, data/fallacies.json]
autonomous: true
requirements: [AUTO-05, AUTO-06, AUTO-07, PERF-05, PERF-06, SEC-02, SEC-03]

must_haves:
  truths:
    - "JSON data structure stores detected fallacies with required fields"
    - "Atomic writes prevent data corruption during concurrent operations"
    - "Archive rotation policy prevents exceeding 100 MB GitHub Pages limit"
    - "Error logging captures all failures (Reddit, HF, JSON writes)"
    - "Fallback placeholder tarot cards used when image generation fails"
    - "No database used (JSON file storage only - SEC-02, SEC-03)"
  artifacts:
    - path: "scripts/data_manager.py"
      provides: "JSON data manager with atomic writes and archive rotation"
      exports: ["DataManager", "load_fallacies()", "save_fallacies()"]
    - path: "data/fallacies.json"
      provides: "Main data file for fallacy entries"
      contains: "entries", "metadata"
  key_links:
    - from: "scripts/data_manager.py"
      to: "data/fallacies.json"
      via: "Atomic write (temp file + rename)"
      pattern: "temp.*\.json"
    - from: "scripts/main.py"
      to: "scripts/data_manager.py"
      via: "Import for data persistence"
      pattern: "from data_manager import"
    - from: "scripts/data_manager.py"
      to: "data/automation.log"
      via: "Error logging"
      pattern: "logging.FileHandler"
---

<objective>
Create JSON data manager with atomic writes, archive rotation policy, and comprehensive error logging.

Purpose: Reliable data persistence that prevents corruption, handles concurrent writes, and manages storage within GitHub Pages limits. Zero-cost JSON-only storage.
Output: Production-ready data manager module.
</object>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
@/Users/volkanakkaya/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/research/SUMMARY.md

# Existing code context
@scripts/fallacy_analyzer.py
@scripts/analyze.py
@data/archive.json
@docs/data/fallacies.json
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create JSON data manager with atomic writes and archive rotation</name>
  <files>scripts/data_manager.py</files>
<action>
Create scripts/data_manager.py with atomic writes and rotation policy:

```python
#!/usr/bin/env python3
"""
JSON data manager for fallacy entries.
Implements AUTO-05 (JSON structure), AUTO-06 (atomic writes), AUTO-07 (fallback),
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

    def __init__(self, data_dir: str = DOCS_DATA_DIR):
        """
        Initialize DataManager.

        Args:
            data_dir: Directory for data files
        """
        self.data_dir = data_dir
        self.main_file = os.path.join(data_dir, "fallacies.json")

        # Ensure directory exists
        os.makedirs(data_dir, exist_ok=True)

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
                "total_entries": 0
            }
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

            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomically rename temp file to target file
            # This prevents partial writes if process crashes mid-write
            os.replace(temp_file, self.main_file)

            logger.debug(f"Atomic write successful: {self.main_file}")

        except Exception as e:
            logger.error(f"Atomic write failed: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    def _get_file_size_mb(self, filepath: str) -> float:
        """Get file size in MB."""
        return os.path.getsize(filepath) / (1024 * 1024)

    def _rotate_archive(self, current_data: Dict):
        """
        Rotate archive if size exceeds limit.
        Implements PERF-05: Archive rotation policy prevents exceeding 100 MB limit.

        Args:
            current_data: Current data dictionary
        """
        file_size_mb = self._get_file_size_mb(self.main_file)

        if file_size_mb > MAX_ARCHIVE_SIZE_MB:
            logger.warning(f"Archive size {file_size_mb:.2f} MB exceeds limit {MAX_ARCHIVE_SIZE_MB} MB")
            logger.info("Rotating archive...")

            # Create archive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = os.path.join(self.data_dir, ARCHIVE_PATTERN.format(timestamp=timestamp))

            # Move current file to archive
            shutil.move(self.main_file, archive_file)
            logger.info(f"Archived to: {archive_file}")

            # Initialize new main file
            self._initialize_data_file()

        # Also rotate if too many entries (keeps file size manageable)
        num_entries = len(current_data.get("entries", []))
        if num_entries > MAX_ENTRIES_BEFORE_ROTATION:
            logger.info(f"Too many entries ({num_entries}), archiving oldest entries")

            # Keep only most recent entries
            entries = current_data["entries"]
            recent_entries = entries[:MAX_ENTRIES_BEFORE_ROTATION // 2]  # Keep half

            current_data["entries"] = recent_entries
            current_data["metadata"]["last_updated"] = datetime.now().isoformat()
            current_data["metadata"]["total_entries"] = len(recent_entries)

            self._atomic_write(current_data)
            logger.info(f"Archived {num_entries - len(recent_entries)} old entries")

    def load_fallacies(self) -> Dict:
        """
        Load fallacies data from JSON file.

        Returns:
            Dictionary with entries and metadata
        """
        try:
            with open(self.main_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.debug(f"Loaded {len(data.get('entries', []))} entries from {self.main_file}")
            return data

        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.main_file}, initializing")
            self._initialize_data_file()
            return self.load_fallacies()

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            # Backup corrupted file
            backup_file = f"{self.main_file}.corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy(self.main_file, backup_file)
            logger.error(f"Backed up corrupted file to: {backup_file}")

            # Initialize new file
            self._initialize_data_file()
            return self.load_fallacies()

    def save_fallacies(self, data: Dict):
        """
        Save fallacies data to JSON file with atomic write.

        Args:
            data: Dictionary with entries and metadata
        """
        # Update metadata
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_entries"] = len(data.get("entries", []))

        # Rotate if needed
        self._rotate_archive(data)

        # Atomic write
        self._atomic_write(data)
        logger.info(f"Saved {len(data.get('entries', []))} entries to {self.main_file}")

    def add_entries(self, entries: List[Dict]):
        """
        Add new entries to the data file.

        Args:
            entries: List of entry dictionaries to add
        """
        data = self.load_fallacies()

        # Validate and format each entry
        for entry in entries:
            # Ensure required fields exist (AUTO-05)
            required_fields = ['post_id', 'title', 'content', 'fallacy_type', 'confidence_score', 'timestamp']
            for field in required_fields:
                if field not in entry:
                    logger.warning(f"Entry missing required field: {field}, using defaults")
                    entry[field] = entry.get(field, '')

            # Ensure fallback image if generation failed (AUTO-07)
            if 'image_url' not in entry or not entry['image_url']:
                entry['image_url'] = FALLBACK_IMAGE
                logger.info(f"Using fallback image for entry: {entry.get('post_id', 'unknown')}")

            # Add default votes if not present
            if 'upvotes' not in entry:
                entry['upvotes'] = 0
            if 'downvotes' not in entry:
                entry['downvotes'] = 0

            # Add to beginning of list (newest first)
            data["entries"].insert(0, entry)

        # Save
        self.save_fallacies(data)

        logger.info(f"Added {len(entries)} new entries")

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

# Convenience functions for backward compatibility
def load_fallacies() -> Dict:
    """Load fallacies data from JSON file."""
    manager = DataManager()
    return manager.load_fallacies()

def save_fallacies(data: Dict):
    """Save fallacies data to JSON file."""
    manager = DataManager()
    manager.save_fallacies(data)

if __name__ == "__main__":
    # Test the data manager
    logging.basicConfig(level=logging.INFO)

    print("Testing DataManager...")

    manager = DataManager()

    # Test adding entries
    test_entries = [
        {
            "post_id": "test_001",
            "title": "Test Title",
            "content": "Test content with enough length to pass validation",
            "fallacy_type": "Ad Hominem",
            "confidence_score": 0.85,
            "timestamp": datetime.now().isoformat(),
            "image_url": "assets/test.png"
        }
    ]

    print("\nAdding test entries...")
    manager.add_entries(test_entries)

    # Test loading entries
    print("\nLoading entries...")
    entries = manager.get_entries(limit=5)
    print(f"Loaded {len(entries)} entries")

    if entries:
        print(f"First entry: {entries[0].get('title', 'No title')}")

    print("\n✅ DataManager working correctly")
```

This implementation:
- Uses atomic writes (temp file + rename) to prevent corruption (AUTO-06)
- Implements archive rotation when file size exceeds 100 MB (PERF-05)
- Uses fallback placeholder images when generation fails (AUTO-07)
- Validates required fields (AUTO-05)
- No database - JSON file storage only (SEC-02, SEC-03)
  </action>
  <verify>
python3 scripts/data_manager.py
  </verify>
  <done>DataManager created with atomic writes, archive rotation, and validation</done>
</task>

<task type="auto">
  <name>Task 2: Update main orchestration script to integrate all components</name>
  <files>scripts/main.py</files>
  <action>
Update scripts/main.py (created in Plan 01) to properly integrate all components:

```python
#!/usr/bin/env python3
"""
Main orchestration script for Fallacy Tarot automation.
Coordinates Reddit scraping, LLM analysis, and data persistence.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Configure logging (PERF-06: Error logging captures all failures)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import client modules
try:
    from reddit_client import fetch_reddit_posts
    from hf_client import analyze_fallacy
    from data_manager import DataManager
except ImportError as e:
    logger.error(f"Failed to import client modules: {e}")
    logger.info("Please ensure all client modules are implemented")
    sys.exit(1)

def main():
    """Main orchestration function"""
    logger.info("=" * 60)
    logger.info("🔮 Fallacy Tarot Automation Started")
    logger.info("=" * 60)

    try:
        # Step 1: Fetch Reddit posts
        logger.info("Step 1: Fetching Reddit posts...")
        posts = fetch_reddit_posts(limit=10)
        logger.info(f"Fetched {len(posts)} posts")

        if not posts:
            logger.warning("No posts fetched, exiting gracefully")
            return

        # Step 2: Analyze posts for fallacies
        logger.info("Step 2: Analyzing posts for fallacies...")
        analyzed_posts = []

        for i, post in enumerate(posts, 1):
            logger.info(f"Analyzing post {i}/{len(posts)}: {post['id']}")
            try:
                analysis = analyze_fallacy(post['content'])

                if analysis and analysis.get('has_fallacy'):
                    # Format entry according to AUTO-05 requirements
                    entry = {
                        'post_id': post['id'],
                        'title': post['title'],
                        'content': post['content'],
                        'source_url': post['url'],
                        'author': post['author'],
                        'reddit_score': post['score'],
                        'subreddit': post['subreddit'],
                        'fallacy_type': analysis['fallacy_type'],
                        'confidence_score': analysis['confidence'],
                        'confidence_level': analysis['confidence_level'],
                        'explanation': analysis['explanation'],
                        'quote': analysis['quote'],
                        'timestamp': datetime.now().isoformat(),
                        'upvotes': 0,
                        'downvotes': 0
                    }
                    analyzed_posts.append(entry)
                    logger.info(f"  → Detected: {analysis['fallacy_type']} (confidence: {analysis['confidence']:.2f} - {analysis['confidence_level']})")
                else:
                    logger.info(f"  → No fallacy detected")

            except Exception as e:
                logger.error(f"Error analyzing post {post['id']}: {e}", exc_info=True)
                # Continue with next post (graceful degradation)
                continue

        logger.info(f"Analysis complete: {len(analyzed_posts)}/{len(posts)} posts have fallacies")

        if not analyzed_posts:
            logger.info("No fallacies detected in this batch")
            return

        # Step 3: Save data using DataManager
        logger.info("Step 3: Saving analyzed data...")
        data_manager = DataManager()
        data_manager.add_entries(analyzed_posts)

        # Log summary
        logger.info("=" * 60)
        logger.info("✅ Automation completed successfully")
        logger.info(f"   New entries: {len(analyzed_posts)}")
        logger.info(f"   Total entries: {len(data_manager.get_entries())}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error in automation: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

Updates:
- Properly imports all client modules
- Formats entries according to AUTO-05 requirements (all required fields)
- Uses DataManager for atomic writes and validation
- Logs comprehensive error information (PERF-06)
- Gracefully handles failures at each step
  </action>
  <verify>
python3 -c "from scripts.main import main; print('✅ Main script imports correctly')"
  </verify>
  <done>Main orchestration script updated to integrate all components</done>
</task>

</tasks>

<verification>
Verify DataManager functionality:
- [ ] Atomic writes use temp file + rename pattern
- [ ] Archive rotation triggers at 100 MB limit
- [ ] Required fields validated before adding entries
- [ ] Fallback placeholder image used when image_url missing
- [ ] JSON file storage only (no database)
- [ ] Comprehensive error logging to automation.log

Test atomic write:
```python
from scripts.data_manager import DataManager
dm = DataManager()
# Add entry
dm.add_entries([{
    'post_id': 'test',
    'title': 'Test',
    'content': 'Test content for validation',
    'fallacy_type': 'Ad Hominem',
    'confidence_score': 0.8,
    'timestamp': '2024-01-01T00:00:00'
}])
# Verify entry was added
entries = dm.get_entries()
assert len(entries) > 0
```
</verification>

<success_criteria>
JSON data manager that:
- Stores fallacies with all required fields (AUTO-05)
- Uses atomic writes to prevent corruption (AUTO-06)
- Rotates archive at 100 MB limit (PERF-05)
- Uses fallback placeholder images (AUTO-07)
- Logs all failures to automation.log (PERF-06)
- Uses JSON file storage only (SEC-02, SEC-03)
- Main orchestration script integrates all components
</success_criteria>

<output>
After completion, create `.planning/phases/01-automation-foundation/01-automation-foundation-04-SUMMARY.md`
</output>
