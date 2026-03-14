#!/usr/bin/env python3
"""
Reddit API client with rate limiting and content validation.
Implements AUTO-01 (6-hour schedule) and AUTO-02 (rate limit handling).
"""

import requests
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Reddit API configuration
# Daha agresif bir User-Agent ile engeli aşmayı deniyoruz
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
REQUEST_TIMEOUT = 15  # Süreyi biraz uzatıyoruz
MAX_RETRIES = 3  # Max retries with exponential backoff
BASE_DELAY = 2  # Base delay for exponential backoff (seconds)
MAX_DELAY = 600  # Max delay (10 minutes) - from AUTO-02

# Subreddits to fetch from
SUBREDDITS = [
    "worldnews",
    "fallacy",
    "philosophy",
    "funny",
    "science",
    "todayilearned",
    "changemyview",
    "all",  # Fallback to r/all for broader coverage
]


def fetch_with_retry(url: str, params: Optional[Dict] = None) -> Optional[Dict]:
    """
    Fetch URL with exponential backoff retry logic.

    Args:
        url: URL to fetch
        params: Query parameters

    Returns:
        JSON response dict or None if all retries fail
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

            # Check for rate limit
            if response.status_code == 429:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                logger.warning(
                    f"Rate limited. Waiting {delay}s before retry {attempt + 1}/{MAX_RETRIES}"
                )
                time.sleep(delay)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                time.sleep(delay)

    return None


def is_content_suitable(post: Dict) -> bool:
    """
    Filter out NSFW, quarantined, deleted, or very short posts.
    Implements AI-05: Content validation filters.

    Args:
        post: Reddit post data

    Returns:
        True if post is suitable for analysis
    """
    # Filter NSFW
    if post.get("over_18", False):
        return False

    # Filter quarantined subreddits
    if post.get("quarantine", False):
        return False

    # Filter deleted/removed posts
    if post.get("selftext") == "[deleted]" or post.get("selftext") == "[removed]":
        return False

    # Combine title and selftext for content
    title = post.get("title", "") or ""
    selftext = post.get("selftext") or ""
    content = f"{title}\n{selftext}".strip()

    # Filter very short content (less than 50 characters)
    if len(content) < 50:
        return False

    return True


def fetch_reddit_posts(limit: int = 10) -> List[Dict]:
    """
    Fetch popular posts from Reddit with rate limiting and content validation.

    Args:
        limit: Maximum number of posts to return (default 10 for efficiency)

    Returns:
        List of post dictionaries with id, title, content, url, author, score, created_utc
    """
    all_posts = []

    logger.info(f"Fetching Reddit posts from {len(SUBREDDITS)} subreddits")

    for i, subreddit in enumerate(SUBREDDITS):
        # Add delay between subreddit fetches to avoid rate limit
        if i > 0:
            time.sleep(2)

        # Fetch top posts from past week (t=week)
        url = f"https://www.reddit.com/r/{subreddit}/top.json"
        params = {"t": "week", "limit": "25"}

        logger.info(f"Fetching r/{subreddit}...")
        data = fetch_with_retry(url, params)

        if not data:
            logger.warning(f"Failed to fetch r/{subreddit}")
            continue

        # Parse posts
        try:
            children = data.get("data", {}).get("children", [])
            for child in children:
                post = child.get("data", {})

                # Validate content suitability
                if not is_content_suitable(post):
                    continue

                # Extract content
                title = post.get("title", "") or ""
                selftext = post.get("selftext") or ""
                content = f"{title}\n{selftext}".strip()

                all_posts.append(
                    {
                        "id": post.get("id"),
                        "title": title,
                        "content": content,
                        "url": f"https://reddit.com{post.get('permalink', '')}",
                        "author": post.get("author") or "anonymous",
                        "score": post.get("score", 0),
                        "created_utc": post.get("created_utc", 0),
                        "subreddit": subreddit,
                    }
                )

            logger.info(
                f"Fetched {len([p for p in all_posts if p.get('subreddit') == subreddit])} posts from r/{subreddit}"
            )

        except Exception as e:
            logger.error(f"Error parsing data from r/{subreddit}: {e}")
            continue

        # Early exit if we have enough posts
        if len(all_posts) >= limit * 2:  # Fetch 2x to allow filtering
            break

    # Sort by score and limit
    all_posts.sort(key=lambda x: x["score"], reverse=True)
    return all_posts[:limit]


if __name__ == "__main__":
    # Test the client
    logging.basicConfig(level=logging.INFO)
    posts = fetch_reddit_posts(limit=5)

    print(f"\nFetched {len(posts)} posts:")
    for post in posts:
        print(
            f"  - r/{post['subreddit']}: {post['title'][:50]}... (score: {post['score']})"
        )
