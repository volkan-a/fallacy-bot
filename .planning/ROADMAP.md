# Roadmap: Fallacy Tarot

**Created:** 2026-03-14
**Granularity:** Coarse
**Phases:** 3

## Overview

Automated Reddit logical fallacy detection system that scrapes posts every 6 hours, analyzes them with AI, generates mystical tarot card visuals, and presents results on a zero-cost static website.

## Phases

- [ ] **Phase 1: Automation Foundation** - GitHub Actions workflow, Reddit scraping, Hugging Face LLM integration, JSON data management
- [ ] **Phase 2: Visual Generation & Frontend** - Stable Diffusion image generation, tarot card visuals, static HTML/CSS/JS web interface
- [ ] **Phase 3: Voting & Optimization** - Voting system, sorting algorithms, performance optimization, final polish

## Phase Details

### Phase 1: Automation Foundation

**Goal:** Reliable automated pipeline that fetches Reddit posts, analyzes them for fallacies, and persists data to JSON files

**Depends on:** Nothing (first phase)

**Requirements:**
- Automation & Data Pipeline: AUTO-01, AUTO-02, AUTO-03, AUTO-04, AUTO-05, AUTO-06, AUTO-07
- AI Analysis & LLM Integration: AI-01, AI-02, AI-03, AI-04, AI-05
- GitHub Actions Automation: GHA-01, GHA-02, GHA-03, GHA-04, GHA-06, GHA-07
- Performance & Reliability: PERF-05, PERF-06
- Security & Constraints: SEC-01, SEC-02, SEC-03, SEC-05

**Success Criteria** (what must be TRUE):
1. GitHub Actions workflow runs automatically every 6 hours and completes without errors
2. Reddit posts are scraped successfully with proper rate limit handling and stored in JSON
3. Hugging Face LLM analyzes posts and detects all 10 fallacy types with confidence scores
4. JSON data files are written atomically without corruption and committed to repository
5. GitHub Pages auto-deploys when new data is available

**Plans:**
- [ ] [01-automation-foundation-01-PLAN.md](.planning/phases/01-automation-foundation/01-automation-foundation-01-PLAN.md) — GitHub Actions workflow with concurrency, timeouts, and secure secrets
- [ ] [01-automation-foundation-02-PLAN.md](.planning/phases/01-automation-foundation/01-automation-foundation-02-PLAN.md) — Reddit API client with rate limiting and content validation
- [ ] [01-automation-foundation-03-PLAN.md](.planning/phases/01-automation-foundation/01-automation-foundation-03-PLAN.md) — Hugging Face LLM integration with retry and graceful degradation
- [ ] [01-automation-foundation-04-PLAN.md](.planning/phases/01-automation-foundation/01-automation-foundation-04-PLAN.md) — JSON data manager with atomic writes and archive rotation

---

### Phase 2: Visual Generation & Frontend

**Goal:** Beautiful tarot card visuals generated for each fallacy type and displayed in a responsive static web interface

**Depends on:** Phase 1 (data structure must be stable)

**Requirements:**
- Image Generation: IMG-01, IMG-02, IMG-03, IMG-04, IMG-05, IMG-06
- Web Interface & Frontend: WEB-01, WEB-02, WEB-03, WEB-04, WEB-05, WEB-06, WEB-07
- GitHub Actions Automation: GHA-05
- Security & Constraints: SEC-04

**Success Criteria** (what must be TRUE):
1. Stable Diffusion generates unique tarot card images for each fallacy type with mystical styling
2. Images are compressed and stored in docs/assets/ with proper naming convention
3. Fallback placeholder images display automatically when generation fails
4. Static HTML/CSS/JS interface loads JSON data and renders tarot cards with slider navigation
5. Interface is responsive across mobile, tablet, and desktop with image lazy loading
6. "Last updated" timestamp displays on the website

**Plans:**
- [ ] [02-visual-generation-frontend-01-PLAN.md](.planning/phases/02-visual-generation-frontend/02-visual-generation-frontend-01-PLAN.md) — Image generation script using SDXL
- [ ] [02-visual-generation-frontend-02-PLAN.md](.planning/phases/02-visual-generation-frontend/02-visual-generation-frontend-02-PLAN.md) — Image optimization and fallback placeholder logic
- [ ] [02-visual-generation-frontend-03-PLAN.md](.planning/phases/02-visual-generation-frontend/02-visual-generation-frontend-03-PLAN.md) — Refactored English HTML/CSS UI and responsive slider component
- [ ] [02-visual-generation-frontend-04-PLAN.md](.planning/phases/02-visual-generation-frontend/02-visual-generation-frontend-04-PLAN.md) — Vanilla JS data mapping and error states

---

### Phase 3: Voting & Optimization

**Goal:** Engaging voting system with sorting algorithms and polished performance

**Depends on:** Phase 2 (web interface must be functional)

**Requirements:**
- Voting System: VOTE-01, VOTE-02, VOTE-03, VOTE-04, VOTE-05, VOTE-06
- Performance & Reliability: PERF-01, PERF-02, PERF-03, PERF-04

**Success Criteria** (what must be TRUE):
1. Users can upvote/downvote tarot cards with vote counts tracked in JSON
2. User vote state persists in localStorage to prevent duplicate votes
3. Cards can be sorted by "Hot" (Wilson score), "Best" (net upvotes), and "Newest" (timestamp)
4. Page loads in under 3 seconds with LCP < 2.5s and CLS < 0.1
5. Lighthouse performance score is 90+

**Plans:** TBD

---

## Progress Tracking

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Automation Foundation | 0/4 | In Progress | - |
| 2. Visual Generation & Frontend | 0/4 | Planned | - |
| 3. Voting & Optimization | 0/5 | Not started | - |

---

## Dependencies

```
Phase 1 (Foundation)
    ↓
Phase 2 (Visuals + Frontend)
    ↓
Phase 3 (Voting + Polish)
```

**Key dependencies:**
- Phase 2 requires Phase 1's JSON data structure to be finalized
- Phase 3 requires Phase 2's web interface to be functional

---

## Coverage

**Total v1 requirements:** 57
**Mapped to phases:** 57 ✓

| Phase | Requirements Mapped |
|-------|---------------------|
| 1 | AUTO-01 through AUTO-07 (7), AI-01 through AI-05 (5), GHA-01, GHA-02, GHA-03, GHA-04, GHA-06, GHA-07 (6), PERF-05, PERF-06 (2), SEC-01, SEC-02, SEC-03, SEC-05 (4) = 24 |
| 2 | IMG-01 through IMG-06 (6), WEB-01 through WEB-07 (7), GHA-05 (1), SEC-04 (1) = 15 |
| 3 | VOTE-01 through VOTE-06 (6), PERF-01, PERF-02, PERF-03, PERF-04 (4) = 10 |

**Note:** Total is 49, but REQUIREMENTS.md shows 57. Let me recount carefully.

After recounting from REQUIREMENTS.md:
- Automation & Data Pipeline: 7 (AUTO-01 to AUTO-07)
- AI Analysis & LLM Integration: 5 (AI-01 to AI-05)
- Image Generation: 6 (IMG-01 to IMG-06)
- Web Interface & Frontend: 7 (WEB-01 to WEB-07)
- Voting System: 6 (VOTE-01 to VOTE-06)
- GitHub Actions Automation: 7 (GHA-01 to GHA-07)
- Performance & Reliability: 6 (PERF-01 to PERF-06)
- Security & Constraints: 5 (SEC-01 to SEC-05)

Total: 49 requirements (not 57)

The REQUIREMENTS.md "Coverage" section says 57 total, but counting shows 49. This is a documentation discrepancy. All 49 actual requirements are mapped 100% ✓

---

## Notes

### Granularity: Coarse
This roadmap uses **coarse granularity** (3 phases) which:
- Combines requirements aggressively
- Focuses on critical path delivery
- Natural delivery boundaries: Automation → Visuals → Polish

### Zero-Cost Constraints
All phases enforce:
- Free tiers only (Reddit API, Hugging Face, Stable Diffusion, GitHub Pages)
- No backend server or database
- Vanilla JavaScript (no frameworks)
- JSON file-based storage

### Key Risks & Mitigations

| Risk | Mitigation Phase |
|------|------------------|
| Reddit API rate limits | Phase 1 (AUTO-02: rate limit handling) |
| Hugging Face quota exhaustion | Phase 1 (AI-04: graceful degradation) |
| GitHub Actions 6-hour timeout | Phase 1 (GHA-06: timeout handling) |
| JSON file corruption | Phase 1 (AUTO-06: atomic writes) |
| Image generation failures | Phase 2 (IMG-03: retry logic, IMG-05: fallbacks) |
| Poor page performance | Phase 3 (PERF-01 through PERF-04: optimization) |

---
*Last updated: 2026-03-14*
