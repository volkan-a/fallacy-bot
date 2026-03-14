# Feature Research

**Domain:** Automated Reddit logical fallacy detection with tarot card visualization
**Researched:** 2026-03-14
**Confidence:** HIGH (official documentation sources: PRAW, Reddit API, Hugging Face Transformers, web.dev, MDN)

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Automated content fetching | Users expect fresh content regularly; stale data = dead site | Low | Reddit API rate limiting requires careful scheduling (PRAW ratelimits: 600s max wait) |
| Error handling & fallbacks | Bots fail; users expect graceful degradation, not broken pages | Medium | PRAW automatically retries within `ratelimit_seconds` config; implement explicit exception handlers |
| Content display interface | Can't have analysis without visualization; core value delivery mechanism | Medium | Static HTML/CSS/JS as specified (no frameworks) |
| Basic sorting (Hot/Newest) | Reddit users expect familiar content ordering patterns | Low | Implement client-side JavaScript sorting from JSON data |
| Responsive design | Mobile traffic dominates; non-responsive = 50%+ users bounce | Medium | Use CSS flexbox/grid; mobile-first approach (MDN web.dev patterns) |
| Image lazy loading | Large card images kill page load speeds; users abandon slow pages (web.dev: <3s critical) | Low | Browser-native `loading="lazy"` attribute or Intersection Observer |
| Performance metrics | Page load speed directly impacts user engagement (web.dev Core Web Vitals) | Medium | Monitor LCP < 2.5s, CLS < 0.1, INP < 200ms |
| Content validation | Garbage in = garbage out; broken Reddit posts break UX | Medium | Validate JSON structure, handle missing fields, filter NSFW/quarantined content |

### Differentiators (Competitive Advantage)

Features that set product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Tarot card visual generation | Unique metaphor transforms dry logic analysis into engaging mystical experience; memorable brand identity | High | Stable Diffusion XL via free tier; generate distinctive card imagery per fallacy type |
| AI fallacy detection with confidence scores | Transparent AI builds trust; users see "how sure" the analysis is (Hugging Face pipelines output scores) | Medium | Text-classification pipeline returns `{'label': 'AD_HOMINEM', 'score': 0.89}` |
| Slider navigation for card browsing | Novel UX pattern aligns with tarot theme; encourages exploration vs list scrolling | Medium | Custom JavaScript slider; CSS transforms for card flip/transition effects |
| Reddit-style voting system | Familiar interaction pattern for Reddit audience; gamification increases engagement | Low | Client-side vote storage in localStorage or track votes via JSON |
| Mystical-themed UI design | Strong visual differentiation; creates emotional connection to topic | Medium | Blues, purples, gold accents; consistent typography and iconography |
| 10 specific fallacy types | Comprehensive coverage vs competitors that focus on 1-2 fallacies | Low | Ad Hominem, Straw Man, Appeal to Authority, False Dilemma, Slippery Slope, Circular Reasoning, Hasty Generalization, Red Herring, Tu Quoque, Appeal to Emotion |
| Zero-cost operation | Sustainable long-term; accessible to hobbyists; no VC pressure | High | GitHub Actions automation + free tiers (Reddit API, Hugging Face, GitHub Pages) |
| Scheduled 6-hour updates | Balance between freshness and rate limits; predictable content cadence | Low | GitHub Actions cron schedule; respects Reddit API limits |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| User accounts & authentication | "Track user progress," "save favorites" | Adds backend complexity, requires database, violates zero-cost constraint, increases attack surface | LocalStorage for preferences/favorites; no login needed for read-only experience |
| Real-time Reddit scraping | "Live updates," "immediate results" | Violates Reddit API rate limits (brand new accounts get blocked), unpredictable cost, GitHub Actions timeout limits | Scheduled 6-hour batch processing; sufficient for discovery platform use case |
| Backend server | "Persistent data storage," "websockets for live voting" | Requires hosting cost ($5-50/month), DevOps overhead, violates GitHub Pages constraint | JSON file storage served via GitHub Pages; client-side state management |
| Database (SQL/NoSQL) | "Reliable data storage," "query capabilities" | Overkill for read-only content; requires managed service or self-hosting; operational complexity | JSON files (fallacies.json, archive.json) committed to git; simple and sufficient |
| Multi-language support | "International users," "broader audience" | Increases LLM inference cost 4-10x, complicates UI, translation quality varies, dilutes MVP focus | English-only for v1; evaluate demand post-launch |
| Paid LLM APIs (OpenAI, Anthropic) | "Better accuracy," "faster inference" | Recurring costs ($10-100/month), budget anxiety as user count grows, pricing changes | Hugging Face free tier Mistral-7B-Instruct; sufficient for fallacy classification task |
| Comment system on website | "User discussions," "community building" | Requires moderation (spam, toxicity), legal liability, duplicates Reddit discussions | Link to original Reddit thread; let Reddit handle comments |
| Real-time voting updates | "Live vote counts," "social proof" | Requires WebSocket server, breaks static hosting constraint, complexity disproportionate to value | Vote counts update on next 6-hour refresh; show "last updated" timestamp |
| Advanced search/filtering | "Find specific fallacies," "filter by subreddit" | Increases JSON payload size, requires backend query logic, UI complexity | Simple client-side filter by fallacy type; basic search across titles |

## Feature Dependencies

```
Reddit Scraping (PRAW)
    └──requires──> Reddit API credentials
                  └──requires──> Rate limit handling (ratelimit_seconds config)
                  └──requires──> JSON data structure definition
                              └──requires──> Fallback/error handling

AI Fallacy Detection (Hugging Face)
    └──requires──> Reddit post content (title + body)
    └──requires──> Mistral-7B-Instruct model loading
                  └──requires──> Confidence score extraction
                              └──requires──> Fallacy type classification (10 types)
                              └──enhances──> UI display (show confidence to users)

Tarot Card Generation (Stable Diffusion XL)
    └──requires──> Fallacy type detected
                  └──requires──> Image generation prompts per fallacy
                  └──requires──> Image storage in docs/assets/
                              └──requires──> Placeholder cards for generation failures

Slider Navigation UI
    └──requires──> Image assets available
    └──requires──> JSON data with image paths
    └──requires──> CSS transforms/transitions
                  └──enhances──> Mystical theme immersion

Voting System
    └──requires──> JSON data structure (upvote/downvote fields)
    └──requires──> LocalStorage for vote tracking
                  └──requires──> "Hot", "Best", "Newest" sorting algorithms
                              └──enhances──> Reddit-like UX familiarity

GitHub Actions Automation
    └──requires──> All Python scripts functional
    └──requires──> JSON file generation
                  └──requires──> Git commit/push workflow
                              └──requires──> GitHub Pages deployment trigger

Performance Optimization
    └──requires──> Image lazy loading
    └──requires──> Image compression
    └──requires──> CSS minification (optional)
                  └──enhances──> User retention (Core Web Vitals)
```

### Dependency Notes

- **Reddit Scraping requires Rate Limit Handling:** PRAW automatically respects X-Ratelimit-* headers; but unknown limits require additional wait time (up to 600s). Configure `ratelimit_seconds=300` (5 minutes) to prevent RedditAPIException. Source: PRAW ratelimits docs.

- **AI Detection enhances UI Display:** Confidence scores from Hugging Face text-classification pipeline (`{'label': 'FALLACY_TYPE', 'score': 0.89}`) should be displayed to build trust. Users prefer transparent AI. Source: Hugging Face Transformers pipeline docs.

- **Tarot Card Generation requires Fallback Handling:** Stable Diffusion XL free tier has rate limits and occasional failures. Must implement placeholder card images for when generation fails. Don't block automation on image generation.

- **Voting System enhances Sorting:** "Hot" algorithm (like Reddit's Wilson score interval) requires vote data. "Best" uses net upvotes. "Newest" uses timestamp. These sorting methods depend on vote data structure.

- **GitHub Actions Automation triggers GitHub Pages:** When automation commits JSON files to docs/data/, GitHub Pages automatically deploys. No separate deployment step needed if configured correctly.

- **Performance Optimization enhances User Retention:** Web.dev research shows pages >3s load time lose 50%+ traffic. Image lazy loading, compression, and Core Web Vitals monitoring (LCP, CLS, INP) are critical for this content-heavy site with many card images.

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate concept.

- [x] **Automated Reddit scraping** — Core data pipeline; fetch popular posts every 6 hours via GitHub Actions
- [x] **AI fallacy detection** — Core value proposition; classify posts into 10 fallacy types with confidence scores using Hugging Face Mistral-7B-Instruct
- [x] **Basic web interface** — Content delivery; static HTML/CSS/JS displaying detected fallacies
- [x] **Error handling & fallbacks** — Reliability; handle Reddit API rate limits, LLM failures, image generation failures gracefully
- [x] **Placeholder tarot cards** — Visual baseline; use pre-designed placeholder images if SD XL fails (don't block on image gen)
- [ ] **Slider navigation UI** — Differentiator; custom slider for browsing cards (can launch with list view first if needed)
- [ ] **Client-side voting** — Engagement; basic upvote/downvote with localStorage tracking
- [ ] **"Hot" sorting algorithm** — Familiar UX; implement Wilson score interval or simplified version

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] **Tarot card image generation** — After verifying detection accuracy works; integrate Stable Diffusion XL for unique visuals per fallacy
- [ ] **Full "Hot", "Best", "Newest" sorting** — After voting system is stable; refine algorithms based on user behavior
- [ ] **Mystical theme polish** — After basic UI works; add advanced CSS animations, particle effects, audio (optional)
- [ ] **Responsive design optimization** — After desktop version works; mobile-first refinement
- [ ] **Performance monitoring** — After users are engaging; add Lighthouse CI, track Core Web Vitals

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] **Archive browsing** — Only if users want historical fallacy detection; currently focuses on fresh content
- [ ] **Multi-language support** — Only if non-English user demand is demonstrated; requires LLM translation
- [ ] **Reddit thread embedding** — Only if engagement metrics show value in keeping users on-site vs linking out
- [ ] **User preferences/filters** — Only if users request customization; currently curatorial approach is intentional
- [ ] **Advanced search** — Only if volume of fallacies makes browsing difficult; currently limited to 6-hour batches
- [ ] **Shareable cards** — Only if social sharing metrics show demand; currently read-only discovery platform

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Automated Reddit scraping | HIGH | MEDIUM | P1 |
| AI fallacy detection (10 types) | HIGH | MEDIUM | P1 |
| Basic web interface (list view) | HIGH | LOW | P1 |
| Error handling & fallbacks | HIGH | MEDIUM | P1 |
| Placeholder tarot cards | MEDIUM | LOW | P1 |
| Slider navigation UI | HIGH | MEDIUM | P2 |
| Client-side voting system | MEDIUM | MEDIUM | P2 |
| "Hot" sorting algorithm | MEDIUM | LOW | P2 |
| Tarot card image generation (SD XL) | HIGH | HIGH | P2 |
| "Best" and "Newest" sorting | MEDIUM | LOW | P2 |
| Mystical theme polish | MEDIUM | MEDIUM | P3 |
| Responsive design optimization | HIGH | MEDIUM | P3 |
| Performance monitoring | MEDIUM | LOW | P3 |
| Archive browsing | LOW | MEDIUM | P3 |
| Multi-language support | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

**Rationale:**
- P1 features enable the core value proposition: detect and display fallacies from Reddit
- P2 features enhance engagement and differentiator (tarot visuals, voting)
- P3 features polish experience and expand reach (responsiveness, international)

## Competitor Feature Analysis

| Feature | Competitor A (Reddit bots like RemindMeBot) | Competitor B (Content analysis bots) | Our Approach |
|---------|--------------|--------------|--------------|
| Content scraping | ✓ Real-time comment monitoring | ✓ Batch content analysis | ✓ Scheduled 6-hour scraping (balance of rate limits and freshness) |
| AI/ML analysis | ✗ Rule-based or manual | ✓ Sentiment analysis, toxicity detection | ✓ Logical fallacy detection (10 specific types) with confidence scores |
| Visual presentation | ✗ Text-only comments | ✓ Dashboards, charts | ✓ Tarot card visualization with mystical theme (unique) |
| User interaction | ✓ Reply to comments | ✓ Upvote/downvote results | ✓ Slider navigation + Reddit-style voting (novel UX) |
| Automation | ✓ Continuous streaming | ✓ Scheduled batch jobs | ✓ GitHub Actions scheduled automation (zero-cost) |
| Cost | Low (cloud) | High (ML infrastructure) | ✓ Zero-cost (free tiers: Reddit API, Hugging Face, GitHub Pages) |
| Reliability | ✓ Well-tested | Varies | ✓ Comprehensive error handling + fallbacks (placeholder cards) |

**Key differentiators:**
1. **Visual metaphor:** Tarot cards transform dry logic analysis into engaging experience (no competitor does this)
2. **Specific fallacy focus:** 10 logical fallacies vs general sentiment/toxicity (more targeted and educational)
3. **Zero-cost sustainability:** All free tiers; competitors often require cloud infrastructure costs
4. **Novel UX pattern:** Slider navigation aligns with tarot theme; most bots use list/grid views

## Sources

- **PRAW Documentation:** https://praw.readthedocs.io/en/stable/ (Reddit API wrapper, rate limiting, streaming submissions)
- **Reddit API Documentation:** https://www.reddit.com/dev/api/ (Official API endpoints, rate limit rules)
- **Hugging Face Transformers:** https://github.com/huggingface/transformers (Pipeline API, text-classification, confidence scores)
- **Hugging Face Pipelines:** https://huggingface.co/docs/transformers/main_classes/pipelines (text-classification pipeline usage, batch processing)
- **Web.dev Performance:** https://web.dev/fast/ (Core Web Vitals, LCP, CLS, INP thresholds, image optimization)
- **MDN Web Performance:** https://developer.mozilla.org/en-US/docs/Web/Performance (Performance fundamentals, lazy loading, critical rendering path)

---
*Feature research for: Automated Reddit logical fallacy detection with tarot card visualization*
*Researched: 2026-03-14*
