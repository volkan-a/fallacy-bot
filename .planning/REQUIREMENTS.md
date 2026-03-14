# Requirements: Fallacy Tarot

**Defined:** 2026-03-14
**Core Value:** Automatically discover and beautifully present logical fallacies from Reddit discussions to make critical thinking engaging and accessible.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Automation & Data Pipeline

- [ ] **AUTO-01**: System automatically scrapes popular Reddit posts every 6 hours via GitHub Actions cron schedule (00:00, 06:00, 12:00, 18:00 UTC)
- [ ] **AUTO-02**: Reddit API client handles rate limits gracefully (30 req/min public, 60 req/min OAuth with ratelimit_seconds config up to 600s)
- [ ] **AUTO-03**: Hugging Face Google Gemma-3-4b-it analyzes scraped posts for logical fallacies with confidence scores
- [ ] **AUTO-04**: System detects all 10 specific fallacy types (Ad Hominem, Straw Man, Appeal to Authority, False Dilemma, Slippery Slope, Circular Reasoning, Hasty Generalization, Red Herring, Tu Quoque, Appeal to Emotion)
- [ ] **AUTO-05**: JSON data structure stores detected fallacies with fields: post_id, title, content, fallacy_type, confidence_score, upvotes, downvotes, timestamp, image_url
- [ ] **AUTO-06**: Atomic JSON writes prevent data corruption during concurrent GitHub Actions runs
- [ ] **AUTO-07**: Fallback placeholder tarot cards used when image generation fails (don't block automation)

### AI Analysis & LLM Integration

- [ ] **AI-01**: Hugging Face Inference API integration with exponential backoff retry logic (up to 5 retries)
- [ ] **AI-02**: Google Gemma-3-4b-it text-classification pipeline returns format: `{'label': 'FALLACY_TYPE', 'score': 0.89}`
- [ ] **AI-03**: Confidence scores displayed to users (High/Medium/Low based on threshold: >0.8, 0.5-0.8, <0.5)
- [ ] **AI-04**: Graceful degradation when Hugging Face API unavailable (skip analysis, log error, continue with other posts)
- [ ] **AI-05**: Content validation filters out NSFW, quarantined, or deleted Reddit posts before analysis

### Image Generation

- [ ] **IMG-01**: Stable Diffusion XL generates unique tarot card images for each detected fallacy type
- [ ] **IMG-02**: Image generation prompts optimized for mystical tarot style (blues, purples, gold accents, symbolic metaphors per fallacy)
- [ ] **IMG-03**: Retry logic with exponential backoff for image generation failures (GPU contention, timeouts)
- [ ] **IMG-04**: Image compression reduces file size while maintaining visual quality (target < 500KB per card)
- [ ] **IMG-05**: Fallback placeholder images prevent broken UI when generation fails
- [ ] **IMG-06**: Images stored in docs/assets/ directory with naming convention: `fallacy_type_{timestamp}.png`

### Web Interface & Frontend

- [ ] **WEB-01**: Static HTML/CSS/JavaScript interface (no frameworks) served via GitHub Pages
- [ ] **WEB-02**: Tarot card display with mystical theme (color palette: blues, purples, gold accents)
- [ ] **WEB-03**: Slider navigation UI for browsing tarot cards (custom JavaScript slider with CSS transforms/transitions)
- [ ] **WEB-04**: Image lazy loading using browser-native `loading="lazy"` attribute or Intersection Observer
- [ ] **WEB-05**: Responsive design with mobile-first approach (mobile 1-column, tablet 2-column, desktop 3-column grid)
- [ ] **WEB-06**: Content validation handles missing JSON fields and displays user-friendly error messages
- [ ] **WEB-07**: "Last updated" timestamp displayed on website (6-hour update cycle)

### Voting System

- [ ] **VOTE-01**: Client-side upvote/downvote buttons on each tarot card
- [ ] **VOTE-02**: Vote counts tracked in JSON (upvotes, downvotes fields)
- [ ] **VOTE-03**: User vote state persisted in localStorage (prevents duplicate votes from same browser)
- [ ] **VOTE-04**: "Hot" sorting algorithm implemented (Wilson score interval or simplified version for user familiarity)
- [ ] **VOTE-05**: "Best" sorting by net upvotes (upvotes - downvotes)
- [ ] **VOTE-06**: "Newest" sorting by timestamp

### GitHub Actions Automation

- [ ] **GHA-01**: GitHub Actions workflow triggers on cron schedule (every 6 hours)
- [ ] **GHA-02**: Workflow concurrency groups prevent parallel runs (`concurrency: group: ${{ github.workflow }}`)
- [ ] **GHA-03**: GitHub Pages deployment triggered automatically when JSON files are committed
- [ ] **GHA-04**: HF_TOKEN secret securely accessed in workflow for Hugging Face API
- [ ] **GHA-05**: SD_TOKEN secret securely accessed in workflow for Stable Diffusion API
- [ ] **GHA-06**: Timeout handling prevents 6-hour GitHub Actions execution limit exceeded
- [ ] **GHA-07**: Git operations handle push conflicts with conflict resolution logic

### Performance & Reliability

- [ ] **PERF-01**: Page load time < 3 seconds (LCP < 2.5s target)
- [ ] **PERF-02**: Cumulative Layout Shift (CLS) < 0.1
- [ ] **PERF-03**: Interaction to Next Paint (INP) < 200ms
- [ ] **PERF-04**: Lighthouse performance score 90+
- [ ] **PERF-05**: Archive rotation policy prevents JSON files from exceeding 100 MB GitHub Pages limit
- [ ] **PERF-06**: Error logging captures all failures (Reddit API, Hugging Face, Stable Diffusion, JSON writes)

### Security & Constraints

- [ ] **SEC-01**: Zero-cost operation enforced (only free tiers: Reddit API public endpoints, Hugging Face free tier, Stable Diffusion free tier, GitHub Pages free tier)
- [ ] **SEC-02**: No backend server (static GitHub Pages hosting only)
- [ ] **SEC-03**: No databases (JSON file storage only)
- [ ] **SEC-04**: No frontend frameworks (vanilla JavaScript only)
- [ ] **SEC-05**: API tokens stored securely in GitHub Secrets (never committed to repo)

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advanced Features

- **ADV-01**: Archive browsing (historical fallacy detection results)
- **ADV-02**: Multi-language support (non-English UI and analysis)
- **ADV-03**: Reddit thread embedding (keep users on-site)
- **ADV-04**: User preferences and filters (customization)
- **ADV-05**: Advanced search across all historical fallacies
- **ADV-06**: Shareable individual tarot cards (social sharing)
- **ADV-07**: Real-time vote count updates (WebSocket server required - violates zero-cost constraint)
- **ADV-08**: User accounts and authentication (backend required - violates zero-cost constraint)
- **ADV-09**: Comment system on website (moderation required - violates zero-cost constraint)

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| User accounts and authentication | Adds backend complexity, violates zero-cost constraint, no user data collection needed for read-only site |
| Backend server | Requires hosting cost ($5-50/month), DevOps overhead, violates GitHub Pages constraint |
| Database (SQL/NoSQL) | Overkill for read-only content, requires managed service or self-hosting, operational complexity |
| Real-time Reddit scraping | Violates Reddit API rate limits, unpredictable cost, GitHub Actions timeout limits |
| Multi-language support (v1) | Increases LLM inference cost 4-10x, complicates UI, dilutes MVP focus |
| Paid LLM APIs (OpenAI, Anthropic) | Recurring costs ($10-100/month), budget anxiety, Hugging Face free tier sufficient |
| Comment system on website | Requires moderation (spam, toxicity), legal liability, duplicates Reddit discussions |
| Real-time voting updates | Requires WebSocket server, breaks static hosting constraint, complexity disproportionate to value |
| Advanced search/filtering | Increases JSON payload size, requires backend query logic, UI complexity |
| Native mobile apps | High development cost, violates zero-cost constraint, web-only responsive approach sufficient |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTO-01 | Phase 1 | Pending |
| AUTO-02 | Phase 1 | Pending |
| AUTO-03 | Phase 1 | Pending |
| AUTO-04 | Phase 1 | Pending |
| AUTO-05 | Phase 1 | Pending |
| AUTO-06 | Phase 1 | Pending |
| AUTO-07 | Phase 1 | Pending |
| AI-01 | Phase 1 | Pending |
| AI-02 | Phase 1 | Pending |
| AI-03 | Phase 1 | Pending |
| AI-04 | Phase 1 | Pending |
| AI-05 | Phase 1 | Pending |
| IMG-01 | Phase 2 | Pending |
| IMG-02 | Phase 2 | Pending |
| IMG-03 | Phase 2 | Pending |
| IMG-04 | Phase 2 | Pending |
| IMG-05 | Phase 2 | Pending |
| IMG-06 | Phase 2 | Pending |
| WEB-01 | Phase 2 | Pending |
| WEB-02 | Phase 2 | Pending |
| WEB-03 | Phase 2 | Pending |
| WEB-04 | Phase 2 | Pending |
| WEB-05 | Phase 2 | Pending |
| WEB-06 | Phase 2 | Pending |
| WEB-07 | Phase 2 | Pending |
| VOTE-01 | Phase 3 | Pending |
| VOTE-02 | Phase 3 | Pending |
| VOTE-03 | Phase 3 | Pending |
| VOTE-04 | Phase 3 | Pending |
| VOTE-05 | Phase 3 | Pending |
| VOTE-06 | Phase 3 | Pending |
| GHA-01 | Phase 1 | Pending |
| GHA-02 | Phase 1 | Pending |
| GHA-03 | Phase 1 | Pending |
| GHA-04 | Phase 1 | Pending |
| GHA-05 | Phase 2 | Pending |
| GHA-06 | Phase 1 | Pending |
| GHA-07 | Phase 1 | Pending |
| PERF-01 | Phase 3 | Pending |
| PERF-02 | Phase 3 | Pending |
| PERF-03 | Phase 3 | Pending |
| PERF-04 | Phase 3 | Pending |
| PERF-05 | Phase 1 | Pending |
| PERF-06 | Phase 1 | Pending |
| SEC-01 | Phase 1 | Pending |
| SEC-02 | Phase 1 | Pending |
| SEC-03 | Phase 1 | Pending |
| SEC-04 | Phase 2 | Pending |
| SEC-05 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 49 total
- Mapped to phases: 49 ✓
- Unmapped: 0
- Orphaned requirements: None

**Phase breakdown:**
- Phase 1 (Automation Foundation): 24 requirements
- Phase 2 (Visual Generation & Frontend): 15 requirements
- Phase 3 (Voting & Optimization): 10 requirements

---
*Requirements defined: 2026-03-14*
*Last updated: 2026-03-14 after initial definition*
