---
phase: 01-automation-foundation
plan: 02
type: execute
wave: 1
depends_on: []
files_modified: [scripts/reddit_client.py, scripts/fallacy_types.py]
autonomous: true
requirements: [AUTO-01, AUTO-02, SEC-01]

must_haves:
  truths:
    - "Reddit posts are fetched from r/all and specified subreddits"
    - "Rate limits are handled gracefully with exponential backoff (up to 600s delay)"
    - "Posts with < 50 characters of content are filtered out"
    - "NSFW, quarantined, or deleted posts are filtered before analysis"
    - "Only free Reddit API public endpoints are used (no OAuth cost)"
  artifacts:
    - path: "scripts/reddit_client.py"
      provides: "Reddit API client with rate limiting and content validation"
      exports: ["fetch_reddit_posts()"]
    - path: "scripts/fallacy_types.py"
      provides: "Fallacy type definitions for validation"
      exports: ["FALLACY_TYPES", "is_valid_fallacy_type()"]
  key_links:
    - from: "scripts/reddit_client.py"
      to: "https://www.reddit.com/r/*/hot.json"
      via: "HTTP GET requests with User-Agent header"
      pattern: "requests.get.*reddit.com"
    - from: "scripts/reddit_client.py"
      to: "scripts/fallacy_types.py"
      via: "Import for content validation"
      pattern: "from fallacy_types import"
---

<objective>
Create robust Reddit API client with exponential backoff rate limiting and comprehensive content validation.

Purpose: Reliable Reddit post fetching that respects API rate limits and filters out inappropriate content before LLM analysis. Zero-cost operation using public endpoints.
Output: Production-ready Reddit client module.
</objective>

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
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create fallacy types definition module</name>
  <files>scripts/fallacy_types.py</files>
  <action>
Create scripts/fallacy_types.py with the 10 fallacy types:

```python
#!/usr/bin/env python3
"""
Fallacy type definitions for validation and analysis.
Based on REQUIREMENTS.md AUTO-04: System detects all 10 specific fallacy types.
"""

from typing import List

# The 10 fallacy types the system must detect
FALLACY_TYPES = [
    "Ad Hominem",
    "Straw Man",
    "Appeal to Authority",
    "False Dilemma",
    "Slippery Slope",
    "Circular Reasoning",
    "Hasty Generalization",
    "Red Herring",
    "Tu Quoque",
    "Appeal to Emotion"
]

def is_valid_fallacy_type(fallacy_type: str) -> bool:
    """
    Check if a fallacy type is one of the 10 valid types.

    Args:
        fallacy_type: The fallacy type string to validate

    Returns:
        True if valid, False otherwise
    """
    return fallacy_type in FALLACY_TYPES

def get_fallacy_types() -> List[str]:
    """Return list of valid fallacy types"""
    return FALLACY_TYPES.copy()

if __name__ == "__main__":
    # Test validation
    print("Valid fallacy types:")
    for ft in FALLACY_TYPES:
        print(f"  - {ft}")

    # Test validation function
    assert is_valid_fallacy_type("Ad Hominem") == True
    assert is_valid_fallacy_type("Invalid Type") == False
    print("\n✅ Fallacy types validation working correctly")
```
  </action>
  <verify>
python3 scripts/fallacy_types.py
  </verify>
  <done>Fallacy types module created with 10 valid types and validation function</done>
</task>

<task type="auto">
  <name>Task 2: Create Reddit client with rate limiting and content validation</name>
  <files>scripts/reddit_client.py</files>
  <action>
Create scripts/reddit_client.py with robust rate limiting and content validation:

```python
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
USER_AGENT = "FallacyTarotBot/1.0 (by /u/fallacy_tarot)"
REQUEST_TIMEOUT = 10  # 10 second timeout per request
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
    "all"  # Fallback to r/all for broader coverage
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
                headers={'User-Agent': USER_AGENT},
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            # Check for rate limit
            if response.status_code == 429:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                logger.warning(f"Rate limited. Waiting {delay}s before retry {attempt + 1}/{MAX_RETRIES}")
                time.sleep(delay)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
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
    if post.get('over_18', False):
        return False

    # Filter quarantined subreddits
    if post.get('quarantine', False):
        return False

    # Filter deleted/removed posts
    if post.get('selftext') == '[deleted]' or post.get('selftext') == '[removed]':
        return False

    # Combine title and selftext for content
    title = post.get('title', '') or ''
    selftext = post.get('selftext') or ''
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
        params = {'t': 'week', 'limit': '25'}

        logger.info(f"Fetching r/{subreddit}...")

        data = fetch_with_retry(url, params)

        if not data:
            logger.warning(f"Failed to fetch r/{subreddit}")
            continue

        # Parse posts
        try:
            children = data.get('data', {}).get('children', [])
            for child in children:
                post = child.get('data', {})

                # Validate content suitability
                if not is_content_suitable(post):
                    continue

                # Extract content
                title = post.get('title', '') or ''
                selftext = post.get('selftext') or ''
                content = f"{title}\n{selftext}".strip()

                all_posts.append({
                    'id': post.get('id'),
                    'title': title,
                    'content': content,
                    'url': f"https://reddit.com{post.get('permalink', '')}",
                    'author': post.get('author') or 'anonymous',
                    'score': post.get('score', 0),
                    'created_utc': post.get('created_utc', 0),
                    'subreddit': subreddit
                })

            logger.info(f"Fetched {len([p for p in all_posts if p.get('subreddit') == subreddit])} posts from r/{subreddit}")

        except Exception as e:
            logger.error(f"Error parsing data from r/{subreddit}: {e}")
            continue

        # Early exit if we have enough posts
        if len(all_posts) >= limit * 2:  # Fetch 2x to allow filtering
            break

    # Sort by score and limit
    all_posts.sort(key=lambda x: x['score'], reverse=True)
    return all_posts[:limit]

if __name__ == "__main__":
    # Test the client
    logging.basicConfig(level=logging.INFO)
    posts = fetch_reddit_posts(limit=5)

    print(f"\nFetched {len(posts)} posts:")
    for post in posts:
        print(f"  - r/{post['subreddit']}: {post['title'][:50]}... (score: {post['score']})")
```

This implementation:
- Uses public Reddit API endpoints (free, no OAuth required - SEC-01)
- Implements exponential backoff with max 600s delay (AUTO-02)
- Filters NSFW, quarantined, deleted, and short posts (AI-05)
- Adds delays between subreddit fetches to avoid rate limits
  </action>
  <verify>
python3 -c "from scripts.reddit_client import fetch_reddit_posts; posts = fetch_reddit_posts(limit=2); print(f'Fetched {len(posts)} posts'); assert len(posts) <= 2, 'Should limit to requested number'"
  </verify>
  <done>Reddit client created with rate limiting, content validation, and logging</done>
</task>

</tasks>

<verification>
Verify Reddit client functionality:
- [ ] Exponential backoff implemented with max 600s delay
- [ ] NSFW/quarantined/deleted posts filtered
- [ ] Posts with < 50 characters filtered
- [ ] Uses public endpoints (no OAuth)
- [ ] Adds delays between subreddit fetches
- [ ] Logs all operations for debugging

Test rate limiting (mock):
```python
# Test that retry logic works
# In production, this will trigger real rate limits
from scripts.reddit_client import fetch_with_retry
```
</verification>

<success_criteria>
Reddit API client that:
- Fetches posts from multiple subreddits
- Handles rate limits with exponential backoff (max 600s)
- Filters inappropriate content (NSFW, quarantined, deleted, short)
- Returns structured post data for LLM analysis
- Logs all operations for debugging
- Uses zero-cost public API endpoints
</success_criteria>

<output>
After completion, create `.planning/phases/01-automation-foundation/01-automation-foundation-02-SUMMARY.md`
</output>
