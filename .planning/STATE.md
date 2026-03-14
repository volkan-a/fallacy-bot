# Project State: Know Your Fallacy

**Last updated:** 2026-03-14

---

## Project Reference

**Core Value:** Accurate and accessible detection of logical fallacies to improve critical thinking skills

**What This Is:** An AI-powered logical fallacy detection system that analyzes text input to identify common reasoning errors and provide visual explanations using a mystical tarot card theme.

**Tech Stack:** React.js, Flask, Python, Tailwind CSS, OpenAI API

**Constraints:**
- Performance: Page load <3s, FCP <1.5s, Lighthouse 90+
- Accessibility: WCAG 2.1 AA
- Design: Tarot theme, #4A90A4 main blue, Inter font
- Browser: Modern browsers only (Chrome, Firefox, Safari, Edge recent)

---

## Current Position

**Phase:** 1 - Core Detection & Foundation

**Plan:** TBD (awaiting planning)

**Status:** Not started

**Progress:** 0/0 plans complete

---

## Performance Metrics

No metrics yet - project in planning phase

---

## Accumulated Context

### Key Decisions Made

| Decision | Rationale |
|----------|-----------|
| React.js + Flask stack | Existing codebase foundation, industry standard |
| OpenAI GPT-5.4 API | Best reasoning capabilities for complex logical analysis |
| Tarot card visual theme | Unique brand differentiator, explicit PROJECT.md requirement |
| Tailwind CSS for styling | Rapid UI development, responsive design, existing implementation |
| Coarse granularity | Balance between speed and deliverable scope |

### Out of Scope (v1)

- User accounts and authentication → v2
- Social features (voting, sharing) → v2
- Multi-language support → v2+
- Real-time Reddit/forum scraping → v2
- Export results → v2 (ADV-01)
- Practice mode → v2 (ADV-02)
- Real-time preview → v2 (ADV-03)

### Known Blockers

None - project ready to begin Phase 1 planning

### Todos

- Plan Phase 1: Core Detection & Foundation
- Execute Phase 1 plans
- Plan Phase 2: Visual Results & Library
- Execute Phase 2 plans

---

## Session Continuity

**Last Action:** Roadmap created with 2 phases covering all 38 v1 requirements

**Next Actions:**
1. Review and approve roadmap
2. Begin Phase 1 planning with `/gsd-plan-phase 1`

---

## Context Notes

### Current Implementation Status

From PROJECT.md:
- Initial development phase complete (React frontend, Flask backend, OpenAI API integration)
- Components implemented: Header, HeroSection, ResultsSection, FallacyCategories, Footer
- Responsive design implemented with Tailwind CSS
- Production deployed

This suggests Phase 1 may build upon existing components rather than starting from scratch.

### Research Insights

Research Summary identifies critical pitfalls to avoid in Phase 1:
1. Blocking LLM API calls on main thread → Use async/await with loading states
2. Exposing API keys → NEVER store client-side, use environment variables on backend
3. Missing error handling for LLM failures → Handle specific errors (429, 500/503) with user-friendly messages
4. Missing rate limiting → Implement per-IP rate limiting with Flask-Limiter

Phase 1 will need to address these foundational concerns.

---

*State initialized: 2026-03-14*
