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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("data/automation.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Import client modules (these will be created in subsequent plans)
try:
    from reddit_client import fetch_reddit_posts
    from hf_client import analyze_fallacy
    from data_manager import DataManager
except ImportError as e:
    logger.error(f"Failed to import client modules: {e}")
    logger.info("Client modules will be created in subsequent plans")
    sys.exit(0)


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
                analysis = analyze_fallacy(post["content"])

                if analysis and analysis.get("has_fallacy"):
                    post["analysis"] = analysis
                    analyzed_posts.append(post)
                    logger.info(
                        f"  → Detected: {analysis['fallacy_type']} (confidence: {analysis['confidence']:.2f})"
                    )
                else:
                    logger.info(f"  → No fallacy detected")

            except Exception as e:
                logger.error(f"Error analyzing post {post['id']}: {e}")
                # Continue with next post (graceful degradation)
                continue

        logger.info(
            f"Analysis complete: {len(analyzed_posts)}/{len(posts)} posts have fallacies"
        )

        if not analyzed_posts:
            logger.info("No fallacies detected in this batch")
            return

        # Step 3: Save data
        logger.info("Step 3: Saving analyzed data...")
        data_manager = DataManager()
        data_manager.add_entries(analyzed_posts)
        logger.info("Data saved successfully")

        logger.info("=" * 60)
        logger.info("✅ Automation completed successfully")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error in automation: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
