# Technology Stack

**Project:** Fallacy Tarot - Automated Reddit Logical Fallacy Detection
**Researched:** 2025-03-14
**Overall confidence:** HIGH

## Recommended Stack

### Core Framework
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Python** | 3.11+ | Backend automation and AI integration | Mature ecosystem, excellent AI library support, GitHub Actions native support |
| **Vanilla JavaScript** | ES2024 | Frontend interactivity | Zero framework overhead, fast page loads, meets zero-cost requirement |

### Data Acquisition
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **requests** | 2.31.0+ | HTTP requests to Reddit API | Simpler than PRAW for read-only access, lower overhead, sufficient for public endpoints |
| **PRAW** (alternative) | 7.7.1 | Reddit API wrapper (optional) | Only needed if authentication becomes necessary; current public access doesn't require it |

### AI/ML Integration
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **huggingface_hub** | 0.23.0+ | Hugging Face Inference API client | Official HF client, automatic provider selection, OpenAI-compatible API support |
| **google/gemma-3-4b-it** | Latest | Fallacy detection LLM | High-quality instruction following, efficient 4B parameter model (faster than 7B), excellent reasoning capabilities, zero-cost via Hugging Face free tier |
| **Stable Diffusion XL** | Latest | Tarot card image generation | State-of-the-art image generation, mystical/symbolic style suitable for tarot cards |
| **Pillow** | 10.0.0+ | Image processing | Save and manipulate generated images |

### Infrastructure
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **GitHub Actions** | Latest | CI/CD automation | Free for public repos, cron scheduling, secrets management, automatic Pages deployment |
| **GitHub Pages** | Static hosting | Web interface deployment | Zero cost, automatic HTTPS, global CDN, perfect for static sites |

### Data Storage
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **JSON files** | - | Data persistence | No database needed, simple to read/write, GitHub Pages compatible, version controlled |
| **localStorage** | HTML5 | Temporary voting storage | Client-side persistence without backend, sufficient for demo use case |

### Supporting Libraries
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **python-dotenv** | 1.0.0+ | Environment variable management | Local development with HF_TOKEN; GitHub Actions uses Secrets directly |
| **datetime** | Built-in | Timestamp handling | Standard Python library for time operations |
| **json** | Built-in | JSON serialization | Standard Python library for data persistence |

## Installation

```bash
# Core Python dependencies
pip install requests huggingface_hub python-dotenv pillow

# Or use requirements.txt
pip install -r requirements.txt
```

**requirements.txt:**
```
requests==2.31.0
huggingface_hub==0.23.0
python-dotenv==1.0.0
Pillow==10.2.0
```

## Reddit API Integration

### Configuration (HIGH confidence)

**Authentication:**
- **Public access (current approach):** No OAuth required for read-only listing endpoints (`/r/{subreddit}/hot.json`, `/top.json`, `/new.json`)
- **Authenticated access (if needed):** OAuth2 with script app type, up to 60 requests/minute

**User-Agent Requirement:**
```python
# Must be unique and descriptive
USER_AGENT = "FallacyTarotBot/1.0 (by /u/fallacy_tarot)"
```

Format: `<platform>:<app ID>:<version string> (by /u/<reddit username>)`

**Rate Limits:**
- Public endpoints: No documented hard limit, but practice rate limiting
- OAuth2 authenticated: 60 requests/minute
- Monitor headers: `X-Ratelimit-Used`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset`

**Endpoints Used:**
```python
# Public listing endpoints (no auth required)
"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit=50"
"https://www.reddit.com/r/all/hot.json?limit=100"
```

### When to Switch to PRAW

**Stay with `requests`:**
- Read-only access to public posts
- Simple listing operations (hot, top, new)
- No user account actions needed

**Switch to PRAW 7.7.1:**
- Need authenticated requests
- Posting comments/moderation actions
- More complex API interactions
- Better rate limit handling needed

## Hugging Face Inference API

### Authentication (HIGH confidence)

**Token Setup:**
1. Create token at https://huggingface.co/settings/tokens
2. Select "fine-grained" token type
3. Enable "Make calls to Inference Providers" permission
4. Add to GitHub Secrets as `HF_TOKEN`

**Environment:**
```python
import os
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
```

### LLM Model: Mistral-7B-Instruct-v0.3 (HIGH confidence)

**Why This Model:**
- 7B parameters - efficient for inference
- Instruction fine-tuned - excellent for structured analysis
- Function calling support - useful for JSON output
- High reasoning quality - perfect for fallacy detection
- Apache 2.0 license - commercial-friendly

**API Usage:**
```python
# Using huggingface_hub InferenceClient
from huggingface_hub import InferenceClient

client = InferenceClient(token=HF_TOKEN)

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=500,
    temperature=0.3
)
```

**Free Tier Limits:**
- Rate limited based on model popularity
- Typical limit: ~10-50 requests/minute
- Queue time may increase during peak usage
- No explicit token limit documented

### Image Generation: Stable Diffusion XL (HIGH confidence)

**Why SDXL:**
- State-of-the-art image quality
- Excellent for detailed, mystical imagery
- Multiple providers available via Inference API
- Good understanding of complex prompts

**API Usage:**
```python
# Using huggingface_hub InferenceClient
client = InferenceClient(token=HF_TOKEN)

image = client.text_to_image(
    prompt="Mystical tarot card representing Ad Hominem fallacy...",
    model="stabilityai/stable-diffusion-xl-base-1.0"
)

# Save the image
image.save("assets/tarot_card.png")
```

**Image Generation Tips:**
- Include artistic style keywords: "Art Nouveau", "Alphonse Mucha inspired", "mystical"
- Specify color palette: "deep purples, gold, midnight blue"
- Request border/text: "gold borders", "intricate details"
- Prompt length: 50-150 words optimal
- Generation time: 10-30 seconds per image

### Inference Providers (MEDIUM confidence)

**How It Works:**
- Hugging Face routes requests to multiple providers (Cerebras, Groq, Fireworks, Together AI, etc.)
- Automatic failover if primary provider unavailable
- OpenAI-compatible API for drop-in replacement

**Provider Selection:**
```python
# Default: auto-select fastest provider
model = "mistralai/Mistral-7B-Instruct-v0.3"

# Cheapest option
model = "mistralai/Mistral-7B-Instruct-v0.3:cheapest"

# Specific provider
model = "mistralai/Mistral-7B-Instruct-v0.3:groq"
```

**Free Tier Considerations:**
- Each provider has different free tier policies
- HF aggregates limits across providers
- May experience queue times during peak usage
- Monitor response times and switch providers if slow

## GitHub Actions Automation

### Workflow Configuration (HIGH confidence)

**Schedule:**
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:          # Manual trigger
```

**Job Setup:**
```yaml
jobs:
  fetch-and-analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests huggingface_hub pillow
```

### Secrets Management (HIGH confidence)

**Required Secrets:**
- `HF_TOKEN` - Hugging Face API token with inference permissions

**Accessing Secrets:**
```yaml
env:
  HF_TOKEN: ${{ secrets.HF_TOKEN }}
```

**Best Practices:**
- Never commit secrets to repository
- Use fine-grained tokens with minimal permissions
- Rotate tokens periodically
- Monitor usage logs

### Deployment to GitHub Pages (HIGH confidence)

**Commit Strategy:**
```yaml
- name: Commit and push results
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add data/ assets/ docs/
    git diff --staged --quiet || git commit -m "Auto-update: New fallacy cards [skip ci]"
    git push
```

**Key Points:**
- Use `[skip ci]` to prevent infinite loops
- Only commit changed files (git diff --staged --quiet)
- GitHub Pages auto-deploys from `docs/` folder

**GitHub Pages Limits:**
- 100 MB total repository size
- 10 MB file size limit
- Unlimited bandwidth for public repos
- Build time: ~1-3 minutes for static sites

## GitHub Pages Static Hosting

### Deployment Strategy (HIGH confidence)

**Source Directory:** `docs/`

**File Structure:**
```
docs/
├── index.html          # Main page
├── data/
│   ├── fallacies.json  # Current fallacies
│   └── archive.json   # Historical data
└── assets/
    ├── card_1.png     # Generated images
    ├── card_2.png
    └── fallback.svg   # Default image
```

**Configuration:**
- Settings → Pages → Source: "Deploy from a branch"
- Branch: `main` → `/docs`
- Custom domain: Optional (default: `username.github.io/repo-name`)

### Performance Optimization (HIGH confidence)

**Image Optimization:**
```python
from PIL import Image
import io

def optimize_image(image, max_size=(800, 800), quality=85):
    """Resize and compress for web"""
    image.thumbnail(max_size)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG', optimize=True, quality=quality)
    return buffer.getvalue()
```

**Recommendations:**
- Keep images under 500KB each
- Use PNG for tarot cards (sharp details)
- Lazy load images in JavaScript
- Add responsive `srcset` attributes

**Caching:**
- GitHub Pages caches assets with 1-hour TTL
- Use cache-busting filenames for updates (e.g., `card_20250314_123456.png`)
- JSON data changes trigger immediate re-fetch

## Vanilla JavaScript Frontend

### Why No Frameworks (HIGH confidence)

**Advantages:**
- Zero build step required
- Faster page load (no bundle overhead)
- Simpler deployment (no npm/build process)
- Lower learning curve for maintenance
- Perfect for this use case (simple data display)

**When You'd Need a Framework:**
- Complex state management (>50 UI components)
- Real-time data synchronization
- Advanced routing (multiple pages)
- Large team collaboration

### Recommended Patterns (HIGH confidence)

**State Management:**
```javascript
// Global state object
const state = {
    fallacies: [],
    currentIndex: 0,
    currentFilter: 'new'
};

// Local storage for persistence
function saveState() {
    localStorage.setItem('fallacyState', JSON.stringify(state));
}

function loadState() {
    const saved = localStorage.getItem('fallacyState');
    return saved ? JSON.parse(saved) : state;
}
```

**Data Fetching:**
```javascript
async function fetchFallacies() {
    try {
        const response = await fetch('data/fallacies.json');
        if (!response.ok) throw new Error('Failed to fetch');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}
```

**Error Handling:**
```javascript
function displayError(message) {
    const container = document.getElementById('content');
    container.innerHTML = `
        <div class="error">
            <p>⚠️ ${message}</p>
            <button onclick="location.reload()">Retry</button>
        </div>
    `;
}
```

### Accessibility Best Practices (MEDIUM confidence)

**Semantic HTML:**
```html
<nav aria-label="Filter navigation">
    <button aria-pressed="true">New</button>
    <button aria-pressed="false">Hot</button>
</nav>

<article aria-label="Fallacy card">
    <h2 id="fallacy-title">${fallacy.type}</h2>
    <img alt="${fallacy.type} tarot card illustration" src="...">
</article>
```

**Keyboard Navigation:**
```javascript
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') prevCard();
    if (e.key === 'ArrowRight') nextCard();
});
```

## JSON File Storage Strategy

### Data Structure (HIGH confidence)

**fallacies.json (current):**
```json
{
  "entries": [
    {
      "id": "20250314_120000",
      "timestamp": "2025-03-14T12:00:00Z",
      "fallacy": {
        "type": "Ad Hominem",
        "confidence": 0.85,
        "explanation": "Attacking the person...",
        "quote": "You're just an idiot..."
      },
      "original_post": {
        "title": "Why climate change is a hoax",
        "text": "...",
        "author": "reddit_user",
        "score": 1423,
        "url": "https://reddit.com/r/..."
      },
      "image": "assets/ad_hominem_20250314.png",
      "votes": {"up": 42, "down": 8},
      "category": "new"
    }
  ]
}
```

**archive.json (historical):**
```json
{
  "entries": [
    // Same structure as fallacies.json
    // Contains all historical entries
  ],
  "metadata": {
    "total_entries": 156,
    "last_updated": "2025-03-14T12:00:00Z",
    "categories": {
      "ad_hominem": 45,
      "straw_man": 32,
      // ... other fallacy types
    }
  }
}
```

### GitHub Actions File Handling (HIGH confidence)

**Reading Existing Data:**
```python
def load_existing_data():
    try:
        with open('docs/data/fallacies.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"entries": []}
```

**Writing New Data:**
```python
def save_data(data, filename='docs/data/fallacies.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

**File Size Management:**
- Limit archive.json to ~1000 entries (~2-3 MB)
- Rotate old entries to separate files if needed
- Use compression if file grows beyond 10 MB

### Version Control Considerations (HIGH confidence)

**Gitignore Patterns:**
```
# Don't commit these
.env
__pycache__/
*.pyc
.DS_Store

# But DO commit these
docs/data/*.json
docs/assets/*.png
```

**Conflict Resolution:**
```python
# Use timestamp-based IDs to avoid conflicts
entry_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

# Atomic write pattern
temp_file = f"{filename}.tmp"
with open(temp_file, 'w') as f:
    json.dump(data, f)
os.replace(temp_file, filename)
```

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Reddit API | `requests` (public) | PRAW | PRAW adds complexity; public access sufficient for read-only |
| LLM | Mistral-7B-Instruct-v0.3 | GPT-3.5/4 | Requires paid API, zero-cost constraint |
| Image Generation | Stable Diffusion XL | Midjourney DALL-E 3 | Not free, zero-cost constraint |
| Hosting | GitHub Pages | Vercel Netlify | GitHub Pages integrated with Actions, zero cost |
| Frontend | Vanilla JS | React Vue | Framework overhead unnecessary for simple display |
| Storage | JSON files | SQLite PostgreSQL | Database adds complexity, no scaling needed |
| LLM Client | `huggingface_hub` | OpenAI SDK | HF has free tier, OpenAI does not |

## Free Tier Limitations & Constraints

### Reddit API (HIGH confidence)
- **Public access:** No authentication needed for listing endpoints
- **Rate limits:** Not documented for public, but practice 1 request/second
- **User-Agent:** Required and must be unique
- **CORS:** Some endpoints may block browser requests; use backend proxy

### Hugging Face Inference API (MEDIUM confidence)
- **Rate limits:** ~10-50 requests/minute depending on model
- **Queue times:** 5-30 seconds during peak usage
- **Token limits:** Not publicly documented
- **Model availability:** Popular models may have queues
- **Image generation:** Longer wait times (10-30s) vs text (~5-10s)

### GitHub Actions (HIGH confidence)
- **Execution time:** 6 hours per job (standard)
- **Public repos:** Unlimited free minutes
- **Private repos:** 2,000 minutes/month
- **Job concurrency:** 20 concurrent jobs
- **Artifacts:** 90-day retention, 500 MB per workflow

### GitHub Pages (HIGH confidence)
- **Storage:** 100 MB soft limit, 1 GB hard limit
- **Bandwidth:** Unlimited for public repos
- **Build time:** 10 minutes per deployment
- **Custom domains:** Free HTTPS via Let's Encrypt
- **Jekyll:** Optional but not required for static HTML

### JSON File Storage (HIGH confidence)
- **Read/write:** Unlimited for GitHub Actions
- **File size:** 10 MB per file limit
- **Total size:** 100 MB repo limit
- **Concurrency:** Git locks prevent simultaneous writes
- **Backup:** Automatic via git history

## Development Workflow

### Local Development (HIGH confidence)
```bash
# 1. Create .env file
echo "HF_TOKEN=your_token_here" > .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analysis manually
python scripts/fallacy_analyzer.py

# 4. Preview locally
python -m http.server 8000 --directory docs
# Visit http://localhost:8000
```

### Testing (HIGH confidence)
```python
# Test Reddit fetching
def test_reddit_fetch():
    posts = fetch_reddit_posts()
    assert len(posts) > 0
    assert 'content' in posts[0]

# Mock HF API responses
import unittest
from unittest.mock import patch

class TestFallacyAnalysis(unittest.TestCase):
    @patch('requests.post')
    def test_analyze_fallacy(self, mock_post):
        mock_post.return_value.json.return_value = {
            'choices': [{'message': {'content': '{"has_fallacy": true, ...}'}}
        }
        result = analyze_fallacy("test text")
        self.assertIsNotNone(result)
```

### Monitoring (MEDIUM confidence)
```python
# Add logging to track performance
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

start_time = time.time()
result = analyze_fallacy(text)
duration = time.time() - start_time
logger.info(f"Analysis completed in {duration:.2f}s")
```

**GitHub Actions Logs:**
- Check workflow run logs for errors
- Monitor HF API response times
- Track Reddit fetch success rates
- Watch for rate limit errors

## Sources

### Reddit API
- https://www.reddit.com/dev/api/ - Official API documentation (HIGH confidence)
- https://github.com/reddit-archive/reddit/wiki/API - Reddit API Wiki (HIGH confidence)
- https://praw.readthedocs.io/en/stable/ - PRAW documentation (HIGH confidence)

### Hugging Face
- https://huggingface.co/docs/api-inference - Inference API docs (HIGH confidence)
- https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3 - Model card (HIGH confidence)
- https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 - SDXL model card (HIGH confidence)
- https://huggingface.co/docs/huggingface_hub - Hub client library (HIGH confidence)

### GitHub Actions
- https://docs.github.com/en/actions - Official documentation (HIGH confidence)
- https://docs.github.com/en/actions/using-workflows - Workflow syntax (HIGH confidence)

### GitHub Pages
- https://docs.github.com/en/pages - Official documentation (HIGH confidence)
- https://docs.github.com/en/pages/getting-started-with-github-pages - Getting started (HIGH confidence)

### Python Libraries
- https://requests.readthedocs.io/en/latest/ - Requests library (HIGH confidence)
- https://pypi.org/project/Pillow/ - Pillow documentation (HIGH confidence)
- https://pypi.org/project/python-dotenv/ - dotenv library (HIGH confidence)

### Frontend
- https://developer.mozilla.org/en-US/docs/Web/JavaScript - MDN JavaScript Guide (HIGH confidence)
- https://developer.mozilla.org/en-US/docs/Learn/Accessibility - Web accessibility (HIGH confidence)
