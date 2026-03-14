#!/usr/bin/env python3
"""
Reddit client using PRAW (OAuth) to bypass datacenter IP blocks.
"""

import os
import praw
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Reddit API configuration via PRAW (OAuth)
# Use GitHub Actions Secrets for authentication
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="FallacyTarotBot/1.0 (by /u/fallacy_tarot)",
)

SUBREDDITS = [
    "worldnews",
    "fallacy",
    "philosophy",
    "funny",
    "science",
    "todayilearned",
    "changemyview",
]


def fetch_reddit_posts(limit: int = 10) -> List[Dict]:
    """Fetch posts using PRAW."""
    all_posts = []

    for subreddit_name in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for submission in subreddit.top(time_filter="week", limit=limit):
                # Content validation
                if len(submission.selftext) < 50 and len(submission.title) < 50:
                    continue

                all_posts.append(
                    {
                        "id": submission.id,
                        "title": submission.title,
                        "content": f"{submission.title}\n{submission.selftext}",
                        "url": submission.url,
                        "author": str(submission.author),
                        "score": submission.score,
                        "created_utc": submission.created_utc,
                        "subreddit": subreddit_name,
                    }
                )
        except Exception as e:
            logger.error(f"Error fetching r/{subreddit_name}: {e}")

    return all_posts[:limit]
