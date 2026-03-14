# Architecture Research

**Domain:** Automated Reddit Scraping System with GitHub Actions
**Researched:** 2026-03-14
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions Scheduler                        │
│                    (Cron: 0 */6 * * * - every 6 hours)              │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │   Schedule   │  │   Manual     │  │   Push to docs/             │  │
│  │   Trigger    │  │   Trigger    │  │   (workflow_dispatch)        │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┬───────────────┘  │
│         │                  │                        │                     │
│         └──────────────────┴────────────────────────┘                     │
│                            ↓                                             │
│         ┌──────────────────────────────┐                                 │
│         │  Workflow Orchestration      │                                 │
│         │  (Checkout → Setup → Run)    │                                 │
│         └──────────────┬───────────────┘                                 │
│                        ↓                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                        Python Automation Script                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │  Reddit      │  │  Hugging     │  │  Stable      │                │
│  │  API Client  │  │  Face LLM    │  │  Diffusion   │                │
│  │  (PRAW or    │  │  (Mistral-   │  │  XL Image    │                │
│  │   requests)  │  │   7B)        │  │  Generation) │                │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                │
│         │                  │                  │                          │
│         └──────────────────┴──────────────────┘                          │
│                            ↓                                             │
│              ┌────────────────────────┐                                  │
│              │  Data Processing &     │                                  │
│              │  Validation Pipeline  │                                  │
│              └──────────────┬─────────┘                                  │
│                         ↓                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                      JSON Data Storage Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │  docs/data/  │  │  docs/data/  │  │  docs/       │                │
│  │  fallacies.  │  │  archive.    │  │  assets/     │                │
│  │  json        │  │  json        │  │  *.png       │                │
│  └──────────────┘  └──────────────┘  └──────────────┘                │
├─────────────────────────────────────────────────────────────────────────┤
│                   GitHub Pages Static Site                               │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  docs/index.html (Static HTML/CSS/JavaScript)                │       │
│  │  ↓                                                            │       │
│  │  Load data/fallacies.json via fetch()                         │       │
│  │  ↓                                                            │       │
│  │  Render tarot cards with slider navigation                      │       │
│  └──────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| **GitHub Actions Scheduler** | Triggers workflow on schedule (every 6 hours) or manually via workflow_dispatch | `on: schedule: cron: '0 */6 * * *'` and `on: workflow_dispatch` |
| **Reddit API Client** | Fetches popular posts from subreddits, handles rate limiting, parses response data | PRAW library or direct `requests` to Reddit JSON API |
| **Hugging Face LLM Client** | Sends text to Mistral-7B-Instruct for fallacy detection, parses JSON response, handles API errors | `requests.post()` to Inference API with retry logic |
| **Stable Diffusion Client** | Generates tarot card images based on fallacy type, handles timeouts, implements fallback strategies | `requests.post()` to Diffusers API with 60s timeout |
| **Data Processing Pipeline** | Validates API responses, filters for high-confidence fallacies, constructs unified data structure | Python functions with error handling and logging |
| **JSON Data Manager** | Loads existing archive, merges new entries, handles file I/O, ensures data consistency | Python JSON module with atomic write patterns |
| **GitHub Actions Commit/Push** | Commits generated JSON and images to repository, triggers Pages deployment | Git commands with `[skip ci]` annotation |
| **Static Frontend** | Loads JSON data via fetch, renders tarot cards, handles user interactions (voting, navigation) | Vanilla JavaScript with localStorage for votes |

## Recommended Project Structure

```
fallacy-bot/
├── .github/
│   └── workflows/
│       └── fallacy_automation.yml    # GitHub Actions workflow definition
├── scripts/
│   ├── __init__.py                   # Package initialization
│   ├── reddit_client.py               # Reddit API wrapper (PRAW or requests)
│   ├── huggingface_client.py         # Hugging Face API wrapper
│   ├── stable_diffusion_client.py    # Stable Diffusion API wrapper
│   ├── data_processor.py             # Data validation and pipeline logic
│   ├── data_manager.py               # JSON I/O and archive management
│   ├── retry_handler.py              # Retry logic with exponential backoff
│   └── main.py                       # Orchestration script (entry point)
├── docs/
│   ├── index.html                     # Static frontend
│   ├── data/
│   │   ├── fallacies.json            # Current fallacy data
│   │   └── archive.json              # Historical archive
│   └── assets/
│       ├── fallback_card.svg          # Fallback image
│       └── *.png                     # Generated tarot cards
└── tests/
    ├── test_reddit_client.py
    ├── test_huggingface_client.py
    └── test_data_processor.py
```

### Structure Rationale

- **`scripts/`**: Separates concerns into dedicated modules for each API client, making testing and maintenance easier
- **`docs/`**: GitHub Pages publishing source, contains both frontend and data
- **`.github/workflows/`**: Standard location for GitHub Actions definitions
- **`tests/`**: Unit tests for each module, critical for reliability in automated systems
- **Modular client modules**: Each external API has its own wrapper, allowing independent testing and easier API migration

## Architectural Patterns

### Pattern 1: Retry with Exponential Backoff

**What:** API requests fail intermittently due to rate limits, network issues, or service availability. Implement retry logic with increasing delays between attempts.

**When to use:** All external API calls (Reddit, Hugging Face, Stable Diffusion)

**Trade-offs:**
- **Pros:** Improves reliability, handles transient failures gracefully
- **Cons:** Increases execution time, may exceed GitHub Actions timeout limits if too aggressive

**Example:**
```python
import time
from functools import wraps
import logging

def retry_with_backoff(max_retries=3, base_delay=1, backoff_factor=2):
    """Decorator for retrying failed API calls with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (backoff_factor ** attempt)
                    logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, base_delay=1, backoff_factor=2)
def fetch_huggingface_response(prompt, model):
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model}/v1/chat/completions",
        headers=HEADERS,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.3
        }
    )
    response.raise_for_status()
    return response.json()
```

### Pattern 2: Graceful Degradation with Fallbacks

**What:** When an optional component fails, continue execution with reduced functionality rather than failing completely.

**When to use:** Image generation (can use placeholder), LLM analysis (can use cached results), Reddit fetch (can use backup subreddits).

**Trade-offs:**
- **Pros:** System remains operational even when parts fail, better user experience
- **Cons:** Reduced functionality, may miss fallacy detections or generate generic images

**Example:**
```python
def generate_fallacy_card(fallacy_type, explanation):
    """Generate tarot card with fallback to placeholder."""
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}/diffusers",
            headers=HEADERS,
            json={"prompt": prompt},
            timeout=60
        )
        response.raise_for_status()

        # Save generated image
        filename = f"assets/{fallacy_type.replace(' ', '_').lower()}_{timestamp}.png"
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename

    except Exception as e:
        logging.warning(f"Image generation failed: {e}. Using fallback.")
        # Return placeholder path
        return "assets/fallback_card.svg"
```

### Pattern 3: Atomic Data Updates

**What:** Write data to temporary file first, then rename to target path to prevent partial writes.

**When to use:** All JSON file writes (fallacies.json, archive.json)

**Trade-offs:**
- **Pros:** Prevents data corruption from interrupted writes, ensures readers always see valid JSON
- **Cons:** Requires temporary file cleanup, slightly more complex

**Example:**
```python
import os
import json
import tempfile

def atomic_json_write(filepath, data):
    """Write JSON data atomically to prevent partial writes."""
    try:
        # Create temporary file in same directory
        dir_path = os.path.dirname(filepath)
        with tempfile.NamedTemporaryFile(
            mode='w',
            dir=dir_path,
            prefix='.tmp_',
            suffix='.json',
            encoding='utf-8',
            delete=False
        ) as tmp_file:
            json.dump(data, tmp_file, indent=2, ensure_ascii=False)
            tmp_path = tmp_file.name

        # Atomic rename (overwrites target if exists)
        os.replace(tmp_path, filepath)

    except Exception as e:
        # Clean up temp file if write failed
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

# Usage
atomic_json_write('docs/data/fallacies.json', new_data)
```

### Pattern 4: Pipeline with Checkpoints

**What:** Process data in stages with intermediate saves, allowing resume from checkpoints if workflow fails mid-execution.

**When to use:** Long-running workflows (6+ hours), processes prone to timeouts (image generation, LLM analysis).

**Trade-offs:**
- **Pros:** Can resume from last successful stage, saves time on re-runs, better debugging
- **Cons:** More complex code, requires checkpoint state management

**Example:**
```python
import json
from pathlib import Path

class Pipeline:
    def __init__(self, checkpoint_file='scripts/checkpoint.json'):
        self.checkpoint_file = checkpoint_file
        self.state = self._load_checkpoint()

    def _load_checkpoint(self):
        if Path(self.checkpoint_file).exists():
            with open(self.checkpoint_file) as f:
                return json.load(f)
        return {'stage': 'init', 'data': {}}

    def _save_checkpoint(self, stage, data):
        self.state = {'stage': stage, 'data': data}
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def run(self):
        # Stage 1: Fetch Reddit data
        if self.state['stage'] in ['init', 'stage1']:
            reddit_data = fetch_reddit_posts()
            self._save_checkpoint('stage1', {'reddit_data': reddit_data})

        # Stage 2: Analyze with LLM
        if self.state['stage'] in ['stage1', 'stage2']:
            analyzed = analyze_fallacies(self.state['data']['reddit_data'])
            self._save_checkpoint('stage2', {'analyzed': analyzed})

        # Stage 3: Generate images
        if self.state['stage'] in ['stage2', 'stage3']:
            images = generate_images(self.state['data']['analyzed'])
            self._save_checkpoint('stage3', {'images': images})

        # Clean up checkpoint on success
        Path(self.checkpoint_file).unlink()
```

## Data Flow

### Automation Pipeline Flow

```
[GitHub Actions Trigger]
    ↓
[Checkout Code]
    ↓
[Setup Python Environment]
    ↓
[Run Main Script]
    ↓
[Reddit Client] → Fetch Posts → [Reddit API]
    ↓
[Data Processor] → Validate & Filter
    ↓
[Hugging Face Client] → Analyze Fallacies → [Hugging Face API]
    ↓
[Data Processor] → Select Best Match (highest confidence)
    ↓
[Stable Diffusion Client] → Generate Image → [Hugging Face API]
    ↓
[Data Manager] → Merge with Archive → JSON Files
    ↓
[Git Commit & Push] → Update Repository
    ↓
[GitHub Pages] → Deploy Static Site
```

### Frontend Data Flow

```
[User Browser]
    ↓
[Load index.html]
    ↓
[JavaScript: fetch('data/fallacies.json')]
    ↓
[Parse JSON Response]
    ↓
[Render Tarot Card Display]
    ↓
[User Interaction]
    ├─→ [Next/Prev Button] → Update currentIndex → Re-render
    ├─→ [Filter Tab] → Filter array → Re-render
    └─→ [Vote Button] → Update votes object → Save to localStorage → Re-render
```

### Key Data Flows

1. **Reddit → LLM:** Raw Reddit post text sent to Mistral-7B, returns JSON with fallacy detection
2. **LLM → Stable Diffusion:** Fallacy type and explanation used as prompt for image generation
3. **All APIs → JSON Manager:** Results from all APIs merged into unified entry structure
4. **JSON Manager → Git:** Updated fallacies.json and images committed to repository
5. **Git → GitHub Pages:** Push triggers Pages deployment, serves updated static files
6. **Pages → Browser:** Frontend fetches latest JSON, renders new content

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1K users | Current architecture is optimal. Single GitHub Actions job runs every 6 hours, handles ~20-50 posts per run. JSON file size remains small (<1MB). |
| 1K-100K users | Consider: (1) Parallel processing of Reddit posts (async/concurrent LLM calls), (2) Image caching for repeated fallacy types, (3) Split archive into multiple JSON files by month, (4) Add pagination to frontend for large datasets. |
| 100K+ users | Consider: (1) Migrate to real backend with database (PostgreSQL + Redis), (2) Implement queue system for async image generation (Celery + RabbitMQ), (3) Use CDN for image assets, (4) Move from GitHub Actions to dedicated CI/CD with longer timeouts. |

### Scaling Priorities

1. **First bottleneck:** GitHub Actions execution timeout (35 minutes default, 6 hours max). Image generation is the slowest component (10-30s per image).
   - **Mitigation:** Limit to 1 image per run (highest confidence fallacy), use aggressive caching, implement timeout handling

2. **Second bottleneck:** Reddit API rate limits (60 requests/minute).
   - **Mitigation:** Use PRAW's built-in rate limit handling, cache subreddit data, batch fetch requests

3. **Third bottleneck:** Hugging Face API limits (depends on tier, free tier has daily/monthly limits).
   - **Mitigation:** Batch multiple posts into single LLM call where possible, cache fallacy analysis for repeated patterns

## Anti-Patterns

### Anti-Pattern 1: Monolithic Script Without Modularization

**What people do:** Put all logic (Reddit fetch, LLM analysis, image generation, data management) in a single 500+ line Python script.

**Why it's wrong:**
- Impossible to test individual components
- Difficult to debug failures
- Can't reuse API clients across different workflows
- Hard to maintain when APIs change

**Do this instead:** Create separate modules for each API client (reddit_client.py, huggingface_client.py, stable_diffusion_client.py) with clear interfaces.

### Anti-Pattern 2: Blocking Sequential API Calls

**What people do:** Call LLM API for each post sequentially, waiting for each to complete before starting the next.

**Why it's wrong:**
- Extremely slow (if 20 posts × 10s per call = 200s just for LLM)
- Wastes time waiting for network I/O
- May exceed GitHub Actions timeout

**Do this instead:** Use concurrent.futures ThreadPoolExecutor or asyncio to make parallel LLM calls:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def analyze_posts_parallel(posts, max_workers=5):
    """Analyze multiple posts concurrently."""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_post = {
            executor.submit(analyze_fallacy, post): post
            for post in posts
        }

        for future in as_completed(future_to_post):
            post = future_to_post[future]
            try:
                result = future.result()
                if result:
                    results.append((post, result))
            except Exception as e:
                logging.error(f"Analysis failed for post {post['id']}: {e}")

    return results
```

### Anti-Pattern 3: No Error Recovery for Git Operations

**What people do:** Run `git push` without handling merge conflicts, authentication failures, or network issues.

**Why it's wrong:**
- Workflow fails silently or fails entire automation
- Leaves repository in inconsistent state
- Requires manual intervention to fix

**Do this instead:** Implement retry logic for git operations, check for conflicts before pushing, use force-with-lease cautiously:

```python
import subprocess
import time

def git_push_with_retry(max_retries=3, delay=5):
    """Push changes to git with retry logic."""
    for attempt in range(max_retries):
        try:
            # Pull latest changes first to avoid conflicts
            subprocess.run(['git', 'pull', '--rebase'], check=True)

            # Commit if there are changes
            result = subprocess.run(
                ['git', 'diff', '--staged', '--quiet'],
                capture_output=True
            )
            if result.returncode != 0:
                subprocess.run(
                    ['git', 'commit', '-m', 'Auto-update: New fallacy cards [skip ci]'],
                    check=True
                )

            # Push changes
            subprocess.run(['git', 'push'], check=True)
            return True

        except subprocess.CalledProcessError as e:
            if attempt == max_retries - 1:
                raise
            logging.warning(f"Git push failed (attempt {attempt + 1}): {e}")
            time.sleep(delay)

    return False
```

### Anti-Pattern 4: Hardcoded Secrets in Workflow Files

**What people do:** Put API tokens directly in YAML workflow files or commit them to the repository.

**Why it's wrong:**
- Security vulnerability - tokens exposed in public repository
- Cannot rotate secrets without redeploying workflow
- Violates GitHub security best practices

**Do this instead:** Use GitHub Secrets and reference them in workflow:

```yaml
# CORRECT: Use GitHub Secrets
- name: Run Fallacy Analysis
  env:
    HF_TOKEN: ${{ secrets.HF_TOKEN }}  # Stored in repo settings
  run: python scripts/main.py

# WRONG: Never do this
- name: Run Fallacy Analysis
  env:
    HF_TOKEN: "hf_xxxxxxxxxxxxxxxx"  # Exposed in repository!
  run: python scripts/main.py
```

### Anti-Pattern 5: Generating Images for All Detected Fallacies

**What people do:** Generate tarot card images for every fallacy detected in a run (could be 10-20 images).

**Why it's wrong:**
- Image generation is slow (10-30s each)
- 20 images × 20s = 400s = 6.7 minutes just for images
- Exceeds GitHub Actions timeout when combined with LLM calls
- Users only see one card at a time anyway

**Do this instead:** Generate only for the highest-confidence fallacy, cache images by fallacy type:

```python
def select_best_fallacy(analyzed_posts):
    """Select the post with highest confidence score."""
    if not analyzed_posts:
        return None

    # Sort by confidence
    sorted_posts = sorted(
        analyzed_posts,
        key=lambda x: x['analysis'].get('confidence', 0),
        reverse=True
    )

    # Return only the best one
    return sorted_posts[0]

# Only generate 1 image per run, not 20
best_post = select_best_fallacy(analyzed_posts)
if best_post:
    image_path = generate_tarot_card(
        best_post['analysis']['fallacy_type'],
        best_post['analysis']['explanation']
    )
```

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **Reddit API** | PRAW library with rate limit handling OR direct requests to JSON endpoints | PRAW handles rate limits automatically. Direct requests require manual backoff. User-Agent header required. |
| **Hugging Face LLM** | POST to Inference API with Bearer token in Authorization header | Use chat completions endpoint. JSON response parsing required. Model: mistralai/Mistral-7B-Instruct-v0.3 |
| **Stable Diffusion** | POST to diffusers endpoint with prompt, 60s timeout | Image generation is slow. Implement retry logic. Use fallback placeholder on failure. |
| **GitHub Actions** | Scheduled cron trigger + workflow_dispatch for manual runs | Use `contents: write` permission. Add `[skip ci]` to commit messages to avoid recursion. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **Reddit Client ↔ Data Processor** | Function call with Reddit post list | Client returns list of dicts with standardized fields (id, content, author, score, url) |
| **Data Processor ↔ Hugging Face Client** | Function call with text, returns analysis dict | LLM client handles retry logic, returns None on failure |
| **Data Processor ↔ Stable Diffusion Client** | Function call with prompt, returns image path | Image generation is synchronous, blocks pipeline. Should be last step. |
| **All Clients ↔ Data Manager** | Data dict passed to manager for merge and save | Manager validates schema before writing, maintains archive structure |
| **Data Manager ↔ Git** | File I/O to JSON files, then subprocess to git commit | Atomic write pattern ensures data consistency |

## GitHub Actions Workflow Structure

### Workflow Phases

```yaml
name: Fallacy Tarot Automation

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours at minute 0
  workflow_dispatch:          # Manual trigger

permissions:
  contents: write  # Required for committing changes

jobs:
  automate:
    runs-on: ubuntu-latest
    timeout-minutes: 330  # 5.5 hours (less than 6h max)

    steps:
      # Phase 1: Setup
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'  # Cache dependencies for faster runs

      - name: Install dependencies
        run: |
          pip install praw requests pillow huggingface_hub python-dotenv

      # Phase 2: Execution
      - name: Run automation pipeline
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          REDDIT_CLIENT_ID: ${{ secrets.REDDIT_CLIENT_ID }}
          REDDIT_CLIENT_SECRET: ${{ secrets.REDDIT_CLIENT_SECRET }}
        run: |
          python scripts/main.py

      # Phase 3: Commit & Deploy
      - name: Commit and push results
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/data/ docs/assets/
          git diff --staged --quiet || git commit -m "Auto-update: New fallacy cards [skip ci]"
          git push
```

### Critical GitHub Actions Constraints

1. **Execution Time Limits:**
   - Free tier: 6 hours per job
   - Default: 35 minutes per job
   - **Impact:** Must optimize image generation and LLM calls to fit within limits

2. **Rate Limits:**
   - No explicit limit documented, but excessive use may be throttled
   - **Impact:** Implement caching and minimize redundant operations

3. **Storage Limits:**
   - Repository size: 1GB (soft), 100GB (hard)
   - GitHub Pages: 1GB per site
   - **Impact:** Must archive old entries periodically, limit image storage

4. **Permissions:**
   - Must have `contents: write` to commit changes
   - **Impact:** Workflow must be configured with proper permissions

5. **Cron Timing:**
   - Minimum interval: 5 minutes
   - **Impact:** Can run every 6 hours as planned, but may have delays due to queue

## Error Handling and Reliability

### Retry Strategy

| Component | Max Retries | Base Delay | Backoff Factor | Timeout |
|------------|--------------|-------------|-----------------|----------|
| Reddit API | 3 | 1s | 2 | 30s |
| Hugging Face LLM | 3 | 2s | 2 | 60s |
| Stable Diffusion | 2 | 5s | 2 | 90s |
| Git Push | 3 | 5s | 1 | 60s |

### Error Categories and Handling

```python
class AutomationError(Exception):
    """Base class for automation errors."""
    pass

class RedditFetchError(AutomationError):
    """Raised when Reddit API fetch fails after retries."""
    pass

class LLMAnalysisError(AutomationError):
    """Raised when LLM analysis fails."""
    pass

class ImageGenerationError(AutomationError):
    """Raised when image generation fails."""
    pass

class DataValidationError(AutomationError):
    """Raised when data validation fails."""
    pass

def handle_error(error, context=""):
    """Centralized error handler with logging."""
    logging.error(f"Error in {context}: {error}")

    # Don't fail entire pipeline for non-critical errors
    if isinstance(error, ImageGenerationError):
        # Use fallback image
        return "assets/fallback_card.svg"
    elif isinstance(error, (RedditFetchError, LLMAnalysisError)):
        # Skip this run, don't update data
        raise
    else:
        # Unknown error, fail pipeline
        raise
```

### Monitoring and Logging

```python
import logging
from datetime import datetime

def setup_logging():
    """Configure structured logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output (GitHub Actions logs)
        ]
    )

def log_pipeline_summary(stats):
    """Log summary statistics for monitoring."""
    logging.info("=" * 50)
    logging.info("Pipeline Summary")
    logging.info("=" * 50)
    logging.info(f"Reddit posts fetched: {stats['reddit_fetched']}")
    logging.info(f"Posts analyzed: {stats['analyzed']}")
    logging.info(f"Fallacies detected: {stats['fallacies_detected']}")
    logging.info(f"Images generated: {stats['images_generated']}")
    logging.info(f"Execution time: {stats['execution_time']}s")
    logging.info("=" * 50)

# Usage in main()
stats = {
    'reddit_fetched': len(posts),
    'analyzed': len(analyzed_posts),
    'fallacies_detected': len(analyzed_posts),
    'images_generated': 1 if best_post else 0,
    'execution_time': execution_time
}
log_pipeline_summary(stats)
```

## JSON Data Management

### Data Schema

```json
{
  "id": "string (unique identifier)",
  "timestamp": 1234567890,
  "date": "2025-01-01 12:00",
  "original_post": {
    "title": "string",
    "text": "string",
    "url": "string (Reddit permalink)",
    "author": "string",
    "score": 123
  },
  "fallacy": {
    "type": "string (Ad Hominem, Straw Man, etc.)",
    "confidence": 0.85,
    "explanation": "string",
    "quote": "string (specific text containing fallacy)"
  },
  "image": "string (path to image in assets/)",
  "votes": {
    "up": 10,
    "down": 2
  },
  "category": "string (new, hot, best)"
}
```

### Archive Management

```python
def manage_archive(new_entry, max_entries=1000):
    """Manage archive size by removing oldest entries."""
    archive = load_existing_data()

    # Add new entry at beginning
    archive['entries'].insert(0, new_entry)

    # Trim if too large
    if len(archive['entries']) > max_entries:
        # Move trimmed entries to separate file
        old_entries = archive['entries'][max_entries:]
        archive['entries'] = archive['entries'][:max_entries]

        # Save to archive_old.json
        atomic_json_write('docs/data/archive_old.json', old_entries)

    # Save updated archive
    atomic_json_write('docs/data/archive.json', archive)

    return archive
```

### Data Validation

```python
from jsonschema import validate, ValidationError

ENTRY_SCHEMA = {
    "type": "object",
    "required": ["id", "timestamp", "original_post", "fallacy", "image", "votes"],
    "properties": {
        "id": {"type": "string"},
        "timestamp": {"type": "number"},
        "original_post": {
            "type": "object",
            "required": ["title", "text", "url", "author", "score"]
        },
        "fallacy": {
            "type": "object",
            "required": ["type", "confidence", "explanation"],
            "properties": {
                "confidence": {"type": "number", "minimum": 0, "maximum": 1}
            }
        },
        "votes": {
            "type": "object",
            "required": ["up", "down"],
            "properties": {
                "up": {"type": "number", "minimum": 0},
                "down": {"type": "number", "minimum": 0}
            }
        }
    }
}

def validate_entry(entry):
    """Validate entry against schema."""
    try:
        validate(instance=entry, schema=ENTRY_SCHEMA)
        return True
    except ValidationError as e:
        logging.error(f"Validation error: {e.message}")
        return False
```

## Static Site Generation

### Frontend Architecture

```
[HTML Structure]
├── Header (Title, Subtitle)
├── Navigation Tabs (New, Hot, Best)
├── Slider Container
│   └── Tarot Card Display
│       ├── Image Column
│       └── Info Column
│           ├── Fallacy Type
│           ├── Original Post
│           ├── Explanation
│           └── Voting Section
└── Arrow Controls (Prev, Next)
```

### JavaScript Data Loading

```javascript
// Async load with error handling
async function loadFallacies() {
    try {
        const response = await fetch('data/fallacies.json');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        fallacies = data;
        filterBy('new');
    } catch (error) {
        document.getElementById('content').innerHTML =
            '<div class="error">Failed to load data. Please try again later.</div>';
        console.error('Load error:', error);
    }
}

// Filter and sort
function filterBy(category) {
    switch (category) {
        case 'new':
            filteredFallacies = [...fallacies].sort((a, b) => b.timestamp - a.timestamp);
            break;
        case 'hot':
            filteredFallacies = fallacies.filter(f => f.category === 'hot');
            break;
        case 'best':
            filteredFallacies = fallacies
                .filter(f => f.category === 'best')
                .sort((a, b) => (b.votes.up - b.votes.down) - (a.votes.up - a.votes.down));
            break;
    }
    currentIndex = 0;
    renderCard();
}

// Vote with localStorage persistence
function vote(id, type) {
    const item = fallacies.find(f => f.id === id);
    if (!item) return;

    // Update votes
    if (type === 'up') item.votes.up++;
    else item.votes.down++;

    // Update category based on score and age
    const score = item.votes.up - item.votes.down;
    const ageHours = (Date.now() / 1000 - item.timestamp) / 3600;

    if (ageHours < 24 && score > 2) item.category = 'hot';
    else if (score > 5) item.category = 'best';

    // Persist to localStorage (client-side only)
    localStorage.setItem('fallacies', JSON.stringify(fallacies));

    renderCard();
}
```

### Performance Optimization

1. **Image Lazy Loading:**
   ```html
   <img src="placeholder.jpg"
        data-src="${imageUrl}"
        loading="lazy"
        onload="this.src=this.dataset.src">
   ```

2. **JSON Caching:**
   ```javascript
   // Cache JSON response for 5 minutes
   async function loadWithCache() {
       const cached = localStorage.getItem('fallacies_cache');
       const cachedTime = localStorage.getItem('fallacies_cache_time');

       if (cached && cachedTime && (Date.now() - cachedTime < 300000)) {
           fallacies = JSON.parse(cached);
           return;
       }

       const response = await fetch('data/fallacies.json');
       fallacies = await response.json();
       localStorage.setItem('fallacies_cache', JSON.stringify(fallacies));
       localStorage.setItem('fallacies_cache_time', Date.now());
   }
   ```

3. **Debounce Slider Navigation:**
   ```javascript
   let debounceTimer;
   function debounceNav(direction) {
       clearTimeout(debounceTimer);
       debounceTimer = setTimeout(() => {
           if (direction === 'next') nextCard();
           else prevCard();
       }, 100);
   }
   ```

## Build Order Implications

Based on component dependencies, recommended build order:

### Phase 1: Foundation (Week 1-2)
1. **GitHub Actions Setup** - Create workflow file with basic structure
2. **Project Structure** - Create modular directory layout
3. **Reddit Client Module** - Implement PRAW or requests wrapper
4. **Basic Data Model** - Define JSON schema and validation

**Rationale:** These components are independent and form the foundation. Workflow must exist before adding automation steps. Reddit client is the data source, so implement first.

### Phase 2: Analysis Pipeline (Week 2-3)
5. **Hugging Face Client Module** - Implement LLM API wrapper
6. **Data Processor** - Implement analysis logic and filtering
7. **Error Handling Framework** - Implement retry decorators and error handlers
8. **Integration Tests** - Test Reddit → LLM pipeline end-to-end

**Rationale:** LLM client depends on Reddit client (provides input). Data processor depends on both. Error handling framework should be in place before testing.

### Phase 3: Image Generation (Week 3-4)
9. **Stable Diffusion Client Module** - Implement image generation API wrapper
10. **Graceful Degradation** - Implement fallback image logic
11. **Image Optimization** - Caching by fallacy type, placeholder handling
12. **Integration Tests** - Test full pipeline: Reddit → LLM → Image

**Rationale:** Image generation is the slowest component and has most fallback logic. Implement after analysis pipeline is stable.

### Phase 4: Data Management (Week 4-5)
13. **Data Manager Module** - Implement JSON I/O with atomic writes
14. **Archive Management** - Implement entry rotation and old data archival
15. **Git Automation** - Implement commit/push logic with retry
16. **Full Pipeline Test** - Test entire automation from start to finish

**Rationale:** Data management depends on all previous components producing output. Git automation is final step that persists results.

### Phase 5: Frontend (Week 5-6)
17. **Static HTML Structure** - Create responsive layout with tarot card design
18. **JavaScript Data Loading** - Implement fetch, parse, render logic
19. **Interactive Features** - Implement slider, tabs, voting
20. **Deployment Test** - Verify GitHub Pages serves content correctly

**Rationale:** Frontend depends on data structure being finalized. Can be developed in parallel with backend but tested after.

## Sources

- **PRAW Documentation:** https://praw.readthedocs.io/en/stable/ (HIGH confidence)
- **Hugging Face Inference API:** https://huggingface.co/docs/api-inference/index (HIGH confidence)
- **GitHub Actions Schedule Triggers:** https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule (HIGH confidence)
- **GitHub Actions Workflow Syntax:** https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions (HIGH confidence)
- **PRAW Rate Limits:** https://praw.readthedocs.io/en/stable/getting_started/ratelimits.html (HIGH confidence)
- **Project Context:** /Users/volkanakkaya/fallacy-bot/.planning/PROJECT.md (HIGH confidence)
- **Current Implementation:** .github/workflows/fallacy_automation.yml, scripts/fallacy_analyzer.py (HIGH confidence)

---
*Architecture research for: Automated Reddit Scraping System with GitHub Actions*
*Researched: 2026-03-14*
