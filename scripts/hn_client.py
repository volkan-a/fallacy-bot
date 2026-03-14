#!/usr/bin/env python3
"""
Hacker News client using official HN API (no auth required).
"""

import requests
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

HN_API_URL = "https://hacker-news.firebaseio.com/v0"


def get_item(item_id: int) -> Dict:
    """Fetch a single item (story/comment) from HN API."""
    try:
        response = requests.get(f"{HN_API_URL}/item/{item_id}.json", timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching HN item {item_id}: {e}")
        return {}


def fetch_reddit_posts(limit: int = 10) -> List[Dict]:
    """Fetch stories from HN (replacing Reddit client)."""
    all_posts = []

    try:
        # Get top stories IDs
        top_stories = requests.get(f"{HN_API_URL}/topstories.json", timeout=10).json()

        for story_id in top_stories[: limit * 2]:  # Buffer
            story = get_item(story_id)

            # Filter: must be a story and have text/title
            if (
                story
                and story.get("type") == "story"
                and (story.get("text") or story.get("title"))
            ):
                all_posts.append(
                    {
                        "id": str(story.get("id")),
                        "title": story.get("title", ""),
                        "content": f"{story.get('title', '')}\n{story.get('text', '')}",
                        "url": f"https://news.ycombinator.com/item?id={story.get('id')}",
                        "author": story.get("by", "anonymous"),
                        "score": story.get("score", 0),
                        "created_utc": story.get("time", 0),
                        "subreddit": "HackerNews",
                    }
                )

            if len(all_posts) >= limit:
                break

    except Exception as e:
        logger.error(f"Error fetching HN posts: {e}")

    return all_posts
