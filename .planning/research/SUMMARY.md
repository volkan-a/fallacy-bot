# Project Research Summary

**Project:** Fallacy Tarot - Automated Reddit Logical Fallacy Detection with Tarot Card Visualization
**Domain:** Automated content scraping with AI analysis and static web hosting
**Researched:** 2026-03-14
**Confidence:** HIGH

## Executive Summary

Fallacy Tarot is an automated Reddit scraping system that detects logical fallacies in popular posts, classifies them using AI, and presents results through a tarot card metaphor on a zero-cost static website. Research shows this is best built as a scheduled GitHub Actions workflow that fetches Reddit posts every 6 hours, analyzes them with Hugging Face's Mistral-7B-Instruct LLM, generates tarot card imagery with Stable Diffusion XL, and deploys to GitHub Pages via JSON data persistence. The entire stack leverages free tiers (Reddit API public endpoints, Hugging Face Inference API, GitHub Actions/Pages) enabling sustainable zero-cost operation with no infrastructure overhead.

The recommended approach prioritizes reliability and graceful degradation over feature completeness. Key risks include API rate limits (Reddit 30-60 req/min, Hugging Face unspecified free tier limits), GitHub Actions 6-hour timeout constraints, and concurrent workflow execution conflicts. Research identifies critical mitigation strategies: exponential backoff retry logic, atomic JSON writes with file locking, aggressive per-operation timeouts (10s Reddit, 30s LLM, 90s image generation), limiting to 5-10 posts per run, and implementing fallback mechanisms (placeholder images when generation fails). The architecture must be modular from the start—separate client modules for each API, checkpoint-based pipeline processing, and comprehensive error handling with logging—to prevent technical debt and enable incremental iteration.

## Key Findings

### Recommended Stack

Zero-cost architecture using free tiers of cloud services. Python 3.11+ for automation (excellent AI library support, GitHub Actions native), Vanilla JavaScript ES2024 for frontend (no framework overhead, meets zero-cost requirement). All external APIs have official Python clients and well-documented free tiers.

**Core technologies:**
- **Python 3.11+** — Backend automation and AI integration — Mature ecosystem, excellent AI library support, GitHub Actions native support
- **requests library** — Reddit API data acquisition — Simpler than PRAW for read-only access, sufficient for public endpoints, lower overhead
- **huggingface_hub** — Hugging Face Inference API client — Official HF client, automatic provider selection, OpenAI-compatible API support
- **Mistral-7B-Instruct-v0.3** — Fallacy detection LLM — High-quality instruction following, efficient 7B parameter model, Apache 2.0 license
- **Stable Diffusion XL** — Tarot card image generation — State-of-the-art image generation, mystical/symbolic style suitable for tarot cards
- **GitHub Actions** — CI/CD automation — Free for public repos, cron scheduling, secrets management, automatic Pages deployment
- **GitHub Pages** — Static hosting — Zero cost, automatic HTTPS, global CDN, perfect for static sites
- **JSON files** — Data persistence — No database needed, simple to read/write, GitHub Pages compatible, version controlled

### Expected Features

**Must have (table stakes):**
- Automated content fetching — Users expect fresh content regularly; stale data = dead site
- Error handling & fallbacks — Bots fail; users expect graceful degradation, not broken pages
- Content display interface — Can't have analysis without visualization; core value delivery mechanism
- Basic sorting (Hot/Newest) — Reddit users expect familiar content ordering patterns
- Responsive design — Mobile traffic dominates; non-responsive = 50%+ users bounce
- Image lazy loading — Large card images kill page load speeds; users abandon slow pages

**Should have (competitive):**
- Tarot card visual generation — Unique metaphor transforms dry logic analysis into engaging mystical experience
- AI fallacy detection with confidence scores — Transparent AI builds trust; users see "how sure" the analysis is
- Slider navigation for card browsing — Novel UX pattern aligns with tarot theme; encourages exploration
- Reddit-style voting system — Familiar interaction pattern for Reddit audience; gamification increases engagement
- Mystical-themed UI design — Strong visual differentiation; creates emotional connection to topic
- 10 specific fallacy types — Comprehensive coverage vs competitors that focus on 1-2 fallacies

**Defer (v2+):**
- Archive browsing — Only if users want historical fallacy detection; currently focuses on fresh content
- Multi-language support — Increases LLM inference cost 4-10x; evaluate demand post-launch
- User accounts & authentication — Adds backend complexity, requires database, violates zero-cost constraint
- Real-time Reddit scraping — Violates Reddit API rate limits; scheduled 6-hour batch processing sufficient

### Architecture Approach

Scheduled GitHub Actions workflow triggers every 6 hours → Python automation script fetches Reddit posts → Hugging Face LLM analyzes for fallacies → Stable Diffusion generates tarot card images → Data pipeline merges results into JSON → Git commits to repository → GitHub Pages auto-deploys static site. Frontend uses vanilla JavaScript to fetch JSON data and render tarot cards with slider navigation.

**Major components:**
1. **GitHub Actions Scheduler** — Triggers workflow every 6 hours via cron, manual trigger via workflow_dispatch
2. **Reddit API Client** — Fetches popular posts, handles rate limiting, parses response data (requests or PRAW)
3. **Hugging Face LLM Client** — Sends text to Mistral-7B-Instruct for fallacy detection, parses JSON response
4. **Stable Diffusion Client** — Generates tarot card images based on fallacy type, implements fallback strategies
5. **Data Processing Pipeline** — Validates API responses, filters for high-confidence fallacies, constructs unified data structure
6. **JSON Data Manager** — Loads existing archive, merges new entries, handles file I/O, ensures data consistency
7. **Static Frontend** — Loads JSON data via fetch, renders tarot cards, handles user interactions (voting, navigation)

**Key patterns to follow:**
- **Retry with exponential backoff** — For all external API calls (Reddit, Hugging Face, Stable Diffusion)
- **Graceful degradation with fallbacks** — When optional components fail, continue with reduced functionality
- **Atomic data updates** — Write to temp file first, then rename to prevent partial writes
- **Pipeline with checkpoints** — Save progress incrementally to enable resume on failure

### Critical Pitfalls

**Top 5 pitfalls from research:**

1. **Reddit API rate limit exceeded** — Implement exponential backoff with jitter, add delays between subreddit fetches, monitor remaining quota via headers, never exceed 30 req/min (unauthenticated) or 60 req/min (OAuth)
2. **Hugging Face free tier quota exhaustion** — Implement graceful degradation (continue with existing data or skip iteration), add retry logic with exponential backoff, cache analysis results, monitor API response headers
3. **GitHub Actions 6-hour job timeout** — Set aggressive timeouts per operation (10s Reddit, 30s LLM, 90s image), process fewer posts per run (5-10 max), implement parallel processing where possible, add checkpointing
4. **JSON file corruption during concurrent writes** — Implement file locking (.lock file), use atomic writes (temp file + os.replace), add workflow concurrency limits in YAML, validate JSON syntax before committing
5. **Stable Diffusion image generation failures** — Implement fallback (use pre-generated placeholder card), validate generated image (file size > 0, valid PNG), simplify prompts, set aggressive timeouts (60-90s), log failures but don't abort workflow

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Automation Foundation
**Rationale:** GitHub Actions workflow and data persistence are foundational; without reliable automation, nothing else works. All external API integrations (Reddit, Hugging Face) depend on this foundation being stable.
**Delivers:** Scheduled GitHub Actions workflow, Reddit API integration, Hugging Face LLM integration, JSON data persistence with atomic writes
**Addresses:** Automated Reddit scraping (P1), AI fallacy detection (P1), basic web interface (P1), error handling & fallbacks (P1)
**Avoids:** Reddit API rate limits (with retry logic), Hugging Face quota exhaustion (with graceful degradation), JSON corruption (with atomic writes), Git push conflicts (with concurrency control)

### Phase 2: Visual Generation & Frontend
**Rationale:** Image generation is the slowest component and has most fallback logic. Implement after analysis pipeline is stable. Frontend depends on data structure being finalized.
**Delivers:** Stable Diffusion image generation with fallbacks, tarot card visual generation (P2), slider navigation UI (P2), responsive static site with lazy loading
**Uses:** Stable Diffusion XL via huggingface_hub, Vanilla JavaScript for frontend interactivity
**Implements:** Data Manager Module, Static HTML Structure, JavaScript Data Loading, Interactive Features
**Addresses:** Placeholder tarot cards (P1), slider navigation UI (P2), client-side voting (P2), "Hot" sorting algorithm (P2)

### Phase 3: Polish & Optimization
**Rationale:** Only after core is working reliably should we invest in polish and performance optimization. Mystical theme and responsive design are nice-to-haves that enhance experience but aren't essential for launch.
**Delivers:** Mystical theme polish (P3), responsive design optimization (P3), performance monitoring (P3), "Best" and "Newest" sorting (P2)
**Addresses:** Full sorting algorithms, performance metrics monitoring, archive browsing (optional)
**Avoids:** Repository bloat from images (plan migration to S3/CDN if needed)

### Phase Ordering Rationale

- **Foundation before features** — Phase 1 establishes the automation pipeline, data persistence, and error handling. All subsequent phases depend on this foundation working reliably. Research shows API integrations fail frequently without proper error handling.
- **Core value before polish** — Phase 2 delivers the core differentiator (tarot card visuals) and user-facing interface. This validates whether the concept resonates before investing in polish.
- **Optimization last** — Phase 3 focuses on performance, responsiveness, and theme polish. These are improvements, not blockers. Research shows 50%+ traffic comes from mobile, but responsive design can be refined after core works.

**Grouping based on architecture patterns:**
- Phase 1 groups backend infrastructure (GitHub Actions, API clients, data pipeline)
- Phase 2 groups frontend and visualization (static site, image generation, user interaction)
- Phase 3 groups optimization and enhancements (performance, responsiveness, sorting)

**How this avoids pitfalls from research:**
- Phase 1 addresses 6 of 8 critical pitfalls upfront (rate limits, quota exhaustion, timeout, JSON corruption, Git conflicts, token exposure)
- Phase 2 addresses the 2 remaining pitfalls (image generation failures, deployment lag)
- Phase 3 addresses technical debt patterns identified in research (performance traps, UX pitfalls)

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1 (Reddit Integration):** Current implementation uses `wget`; research recommends `requests` library for better error handling. Need to validate public Reddit API endpoint stability without OAuth authentication.
- **Phase 2 (Stable Diffusion):** Image generation has highest failure rate on free tier. Need to research optimal prompt engineering for tarot card style and validate placeholder card strategy.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Hugging Face LLM):** Text classification with Mistral-7B-Instruct is well-documented. Standard patterns apply.
- **Phase 2 (Static Frontend):** Vanilla JavaScript with JSON data loading is standard practice. No complex state management needed.
- **Phase 3 (GitHub Actions):** Scheduling and secrets management are standard patterns. Well-documented.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All technologies verified against official documentation (Reddit API, Hugging Face, GitHub Actions/ Pages) |
| Features | HIGH | Feature priorities based on web performance research (web.dev Core Web Vitals) and Reddit user expectations |
| Architecture | HIGH | Architecture patterns verified against PRAW, Hugging Face, GitHub Actions best practices |
| Pitfalls | HIGH | All pitfalls documented with official source links; mitigation strategies tested in similar projects |

**Overall confidence:** HIGH

### Gaps to Address

- **Reddit API authentication strategy** — Research recommends `requests` library for public endpoints, but unclear if unauthenticated access is sustainable long-term. During Phase 1 planning, validate whether OAuth (PRAW) is needed for higher rate limits (60 vs 30 req/min).
- **Hugging Face free tier limits** — Unspecified daily/monthly quotas on Inference API. During Phase 1 implementation, monitor usage closely and document actual limits encountered.
- **Stable Diffusion prompt engineering** — Current prompt is detailed but may cause timeouts. During Phase 2, test simplified prompts and validate placeholder card strategy.
- **Image caching strategy** — Research recommends caching by fallacy type, but implementation details not specified. During Phase 2, design cache invalidation strategy.

## Sources

### Primary (HIGH confidence)
- **Reddit API Documentation** — https://www.reddit.com/dev/api/ (Rate limits, endpoint structure)
- **Hugging Face Inference API** — https://huggingface.co/docs/api-inference/index (Mistral-7B-Instruct, Stable Diffusion XL, free tier)
- **GitHub Actions** — https://docs.github.com/en/actions (Scheduling, limits, secrets management, deployment)
- **GitHub Pages** — https://docs.github.com/en/pages (Static hosting, deployment lag)
- **PRAW Documentation** — https://praw.readthedocs.io/en/stable/ (Rate limit handling, streaming)
- **Web.dev Performance** — https://web.dev/fast/ (Core Web Vitals, image optimization thresholds)

### Secondary (MEDIUM confidence)
- **MDN Web Performance** — https://developer.mozilla.org/en-US/docs/Web/Performance (Lazy loading, performance fundamentals)
- **Python Requests Library** — https://requests.readthedocs.io/en/latest/ (HTTP client patterns, retry logic)
- **Pillow Documentation** — https://pypi.org/project/Pillow/ (Image processing, optimization)

### Tertiary (LOW confidence)
- **Hugging Face Spaces Specs** — https://huggingface.co/docs/hub/spaces-overview (Hardware specs, pricing - verified for inference but not Spaces)
- **Reddit API Community Wiki** — https://github.com/reddit-archive/reddit/wiki/API (Unofficial but commonly referenced)

---
*Research completed: 2026-03-14*
*Ready for roadmap: yes*
