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
from dotenv import load_dotenv

# Load environment variables from .env file for local testing
load_dotenv()

# Add scripts directory to path so we can import from it when run from root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

# Import client modules
try:
    from scripts.reddit_client import fetch_reddit_posts
    from scripts.hf_client import analyze_fallacy
    from scripts.data_manager import DataManager
    from scripts.image_generator import generate_card_for_fallacy
except ImportError as e:
    try:
        # Try local imports if running from inside scripts/
        from reddit_client import fetch_reddit_posts
        from hf_client import analyze_fallacy
        from data_manager import DataManager
        from image_generator import generate_card_for_fallacy
    except ImportError as e2:
        logger.error(f"Failed to import client modules: {e} / {e2}")
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
        posts = fetch_reddit_posts(limit=5)  # Canlı test için 5 gönderi çekiyoruz
        logger.info(f"Fetched {len(posts)} posts")
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
                    logger.info(
                        f"  → Detected: {analysis['fallacy_type']} (confidence: {analysis['confidence']:.2f})"
                    )

                    # Generate tarot card image
                    logger.info(
                        f"  → Generating tarot card image for {analysis['fallacy_type']}..."
                    )
                    image_path = generate_card_for_fallacy(analysis["fallacy_type"])

                    # Format entry according to AUTO-05 requirements
                    entry = {
                        "post_id": post["id"],
                        "title": post["title"],
                        "content": post["content"],
                        "source_url": post["url"],
                        "author": post["author"],
                        "reddit_score": post["score"],
                        "subreddit": post["subreddit"],
                        "fallacy_type": analysis["fallacy_type"],
                        "confidence_score": analysis["confidence"],
                        "confidence_level": analysis.get("confidence_level", "Medium"),
                        "explanation": analysis["explanation"],
                        "quote": analysis["quote"],
                        "image_url": image_path,
                        "timestamp": datetime.now().isoformat(),
                        "upvotes": 0,
                        "downvotes": 0,
                    }
                    analyzed_posts.append(entry)
                else:
                    logger.info(f"  → No fallacy detected")

            except Exception as e:
                logger.error(f"Error analyzing post {post['id']}: {e}", exc_info=True)
                # Continue with next post (graceful degradation)
                continue

        logger.info(
            f"Analysis complete: {len(analyzed_posts)}/{len(posts)} posts have fallacies"
        )

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
    # Ensure data directory exists for logs
    os.makedirs("data", exist_ok=True)
    main()
