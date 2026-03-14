# Project Research Summary

**Project:** Know Your Fallacy - AI-Powered Logical Fallacy Detection
**Domain:** AI-powered web application with LLM integration
**Researched:** 2026-03-14
**Confidence:** HIGH

## Executive Summary

This is an AI-powered web application that analyzes text for logical fallacies using OpenAI's GPT-5.4 model. Experts build these applications with a React/Next.js frontend, Python/Flask backend for API proxying, and careful attention to async patterns, rate limiting, and caching to control LLM costs and provide responsive UX. The research strongly recommends using the existing Flask codebase as a foundation while adding async support, implementing backend OpenAI integration (never client-side), and adding rate limiting and caching from day one to prevent runaway costs.

The recommended approach prioritizes the tarot card visual theme as a core differentiator alongside standard text analysis features. Critical risks include exposing API keys, blocking the UI during LLM calls, insufficient error handling for API failures, and cost overruns from unbounded usage. These are mitigated by backend proxying, async/await patterns with loading states, comprehensive error handling, and strict rate limiting. The architecture follows clear separation between React components, API service layer, Flask API gateway, and AI integration layer, with well-defined boundaries and data flow patterns.

## Key Findings

### Recommended Stack

Research confirms a modern React + Python stack with OpenAI integration. For this project, migrate existing Flask codebase to Flask 3.1+ with async support, use Next.js 15.1 (App Router) for frontend with Tailwind CSS 4.2 for styling, and integrate OpenAI GPT-5.4 via Python SDK through backend proxy.

**Core technologies:**
- **React 18.3 + Next.js 15.1 (App Router)** — Frontend UI framework — Industry standard with Server Components, streaming AI responses, built-in TypeScript support
- **Python 3.14+ with Flask 3.1+** — Backend framework — Existing codebase foundation; add async support; Flask-Caching and Flask-Limiter essential for LLM apps
- **OpenAI GPT-5.4 + Responses API** — AI reasoning engine — Best reasoning capabilities for complex logical analysis; structured outputs ensure consistent fallacy classification
- **Tailwind CSS 4.2** — Styling — Utility-first CSS used by major platforms; v4 adds CSS variables and P3 colors
- **Vercel (frontend) + Railway/Docker (backend)** — Deployment — Native Next.js platform with built-in AI observability; Docker for reproducible Python builds

### Expected Features

Analysis of competitors (GPTZero, Kialo, Your Logical Fallacy Is) reveals standard expectations vs differentiation opportunities.

**Must have (table stakes):**
- **Text Input Methods** (paste box, character counter, clear button) — Users need to input text; standard UX pattern
- **Fallacy Detection** — Core value proposition; AI-dependent
- **Visual Results Display** (highlighted fallacies, color-coded) — Users expect to see where fallacies occur
- **Fallacy Explanations with Examples** — Educational value requires understanding
- **Searchable Fallacy Library with Categories** — Users want to learn about specific fallacies
- **Mobile-Responsive Design** — Required by PROJECT.md constraints
- **Accessibility Compliance (WCAG 2.1 AA)** — Required by PROJECT.md constraints
- **Loading Indicators & Error Handling** — AI analysis takes time; users need feedback

**Should have (competitive):**
- **Tarot Card Visual Theme** — Unique branding; memorable; explicit PROJECT.md requirement
- **Sentence-Level Highlights with Confidence Scores** — Transparency builds trust
- **Multi-Fallacy Detection** — Real-world arguments contain multiple errors
- **Context-Sensitive Explanations** — Personalized learning vs generic explanations
- **Export Results** — Useful for students, teachers, researchers
- **Practice Mode with Sample Texts** — Active learning is more effective

**Defer (v2+):**
- **User Accounts and Authentication** — Out of scope per PROJECT.md v1
- **Progress Tracking and Gamification** — Requires accounts; defer to v2
- **Social Features** — Defer to v2 per PROJECT.md
- **Real-Time Preview** — Complexity vs value tradeoff; defer post-v1
- **Multi-Language Support** — Defer to v2 per PROJECT.md

### Architecture Approach

Recommended architecture follows clear separation: React Components handle UI rendering and state, API Service Layer manages HTTP requests, Flask API Gateway handles CORS/rate limiting/validation, Routes organize endpoints in blueprints, and AI Integration Layer manages OpenAI calls with prompt engineering. Data flows from user input through Flask validation to OpenAI API and back through JSON responses. Key patterns include REST API design with Flask blueprints, React hooks for state management, centralized error handling, request validation decorators, and caching for cost optimization.

**Major components:**
1. **React Components** (Header, HeroSection, ResultsSection) — UI rendering, user interaction, state management with useState/useEffect
2. **API Service Layer** — HTTP requests, response parsing, error handling for Flask backend
3. **Flask API Gateway** — CORS, rate limiting, request validation, error handling
4. **Routes (Blueprints)** — Endpoint definitions (/api/analyze, /api/fallacy-types), business logic
5. **AI Integration Layer** — OpenAI API calls, prompt engineering, response parsing with structured outputs
6. **Caching Layer** — Flask-Caching to reduce LLM API costs (in-memory dev, Redis production)
7. **Rate Limiting** — Flask-Limiter to prevent API abuse (IP-based v1, user-based v2+)

### Critical Pitfalls

Research reveals 5 critical pitfalls that must be addressed immediately.

1. **Blocking LLM API calls on main thread** — Always use async/await with loading states; disable submit buttons; never make LLM calls directly from frontend; show "Analyzing..." immediately
2. **Exposing API keys and no rate limiting** — NEVER store API keys client-side; use environment variables on backend; implement per-IP rate limiting with Flask-Limiter; set explicit API usage quotas
3. **Naive caching leading to wrong results** — Use semantic hashing/normalization; include LLM model version in cache keys; set appropriate TTL (24 hours); allow cache invalidation; monitor hit rate
4. **Missing error handling for LLM failures** — Handle specific LLM API errors (429, 500/503) with user-friendly messages; implement exponential backoff; validate LLM responses before returning; add retry buttons
5. **Over-fetching large results and poor UX** — Use structured prompts specifying output format; implement progressive disclosure; limit results to top N by confidence; allow user preferences (brief vs detailed)

## Implications for Roadmap

Based on combined research, suggested phase structure follows dependency chains and risk mitigation:

### Phase 1: MVP Foundation
**Rationale:** Core value proposition (fallacy detection) must work before anything else. Tarot theme is explicit PROJECT.md requirement that defines brand. Critical pitfalls (API key security, blocking calls, error handling, rate limiting) are foundational and must be addressed immediately or the product is unusable or financially unsustainable.
**Delivers:** Working fallacy detection with tarot visual theme, basic frontend, backend API proxy with security controls
**Addresses:** Text Input Methods, Fallacy Detection, Visual Results Display (basic), Fallacy Explanations, Searchable Fallacy Library, Tarot Card Visual Theme, Mobile-Responsive Design, Accessibility Compliance, Loading Indicators, Error Handling
**Avoids:** Exposing API keys, blocking LLM calls on main thread, missing error handling, missing rate limiting
**Features:** All table stakes + tarot theme as core differentiator

### Phase 2: UX Enhancement & Optimization
**Rationale:** Once core detection works, user feedback and analytics will reveal UX issues. This phase adds advanced features (multi-fallacy detection, confidence scores) and optimizations (caching, async improvements) to improve user experience and reduce costs. Caching and advanced error recovery can only be added after understanding usage patterns.
**Delivers:** Enhanced results display, sentence-level highlights with confidence, context-sensitive explanations, export functionality, caching for cost reduction, practice mode with sample texts
**Uses:** Flask-Caching (Redis), Flask-Limiter (user-based if accounts added), Vercel AI SDK for streaming
**Implements:** Multi-Fallacy Detection, Sentence-Level Highlights with Confidence Scores, Context-Sensitive Explanations, Export Results, Practice Mode, Caching Strategy
**Avoids:** Naive caching, over-fetching results

### Phase 3: Advanced Features & Production Hardening
**Rationale:** After validating core concept and UX, add features requiring infrastructure (user accounts, progress tracking) and production-hardening (monitoring, observability, security audit). This phase prepares for scale and monetization.
**Delivers:** User accounts and authentication, progress tracking and gamification, real-time preview, advanced monitoring and observability, security audit and hardening, performance optimization at scale
**Uses:** PostgreSQL (upgrade from SQLite), Sentry for error tracking, OpenTelemetry for distributed tracing, Redis for distributed caching
**Implements:** User Accounts and Authentication, Progress Tracking, Real-Time Preview, Advanced Monitoring, Security Hardening

### Phase Ordering Rationale

- **Why this order based on dependencies:** Fallacy detection is the core dependency (must exist before results display). User accounts depend on authentication infrastructure, which is unnecessary for MVP validation. Caching requires usage data to tune properly.
- **Why this grouping based on architecture patterns:** Phase 1 implements core architecture components (React components, Flask API gateway, AI integration layer). Phase 2 adds optimization layers (caching, streaming, advanced error handling). Phase 3 scales infrastructure (database migration, distributed systems, observability).
- **How this avoids pitfalls from research:** Phase 1 explicitly addresses critical pitfalls (security, blocking calls, error handling). Phase 2 addresses caching pitfalls after understanding usage. Phase 3 addresses scaling pitfalls only after validating the product.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1 (MVP Foundation):** Tarot card visual design system design mapping fallacies to mystical imagery — creative work, no clear patterns to follow
- **Phase 2 (UX Enhancement):** Prompt engineering for multi-fallacy detection — complex LLM task, may need experimentation with different approaches
- **Phase 3 (Advanced Features):** Real-time preview implementation — debouncing strategies, streaming implementation requires technical research

Phases with standard patterns (skip research-phase):
- **Phase 1 (MVP Foundation):** REST API with Flask, React state management, error handling, rate limiting — well-documented patterns in official docs
- **Phase 2 (UX Enhancement):** Caching with Flask-Caching, export functionality — standard web application patterns
- **Phase 3 (Advanced Features):** PostgreSQL migration, user authentication, monitoring integration — established patterns with extensive documentation

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All recommendations from official docs (React, Flask, OpenAI, Tailwind, Vercel); verified versions and compatibility |
| Features | MEDIUM | Table stakes from direct competitor observation; differentiators inferred from market patterns; no user studies available |
| Architecture | HIGH | Patterns from official React and Flask docs; component boundaries and data flow well-established; anti-patterns explicitly documented |
| Pitfalls | HIGH | Based on official documentation (Flask production warnings, React async patterns) and common LLM integration mistakes from community |

**Overall confidence:** HIGH

### Gaps to Address

- **Tarot visual design system:** PROJECT.md requires tarot theme but no clear patterns exist for mapping fallacies to mystical imagery — creative design work needed during Phase 1 planning
- **Multi-fallacy detection prompt engineering:** No specific research on optimal prompts for detecting multiple fallacies in single text — experimentation needed during Phase 2
- **Fallacy library content:** Need to curate explanations and examples for common fallacies — can use existing resources (Stanford Encyclopedia, etc.) as starting point
- **User behavior patterns:** No data on how users interact with fallacy detection tools — Phase 1 should include analytics to inform Phase 2 UX refinements
- **Cost projections:** OpenAI pricing documented but actual usage patterns unknown — Phase 1 should monitor usage to refine cost estimates for scaling

## Sources

### Primary (HIGH confidence)
- **React Docs** — Next.js App Router recommendation, useState/useEffect patterns, performance best practices
- **Flask Documentation** — Error handling, view decorators, production deployment warnings, ProxyFix security
- **OpenAI API Docs** — GPT-5.4 model, Responses API, structured outputs, pricing and rate limits
- **Tailwind CSS** — v4.2 features, major company users, utility-first styling
- **Vercel AI Templates** — AI chatbot patterns, AI SDK integration, streaming responses
- **PROJECT.md** — Explicit project constraints, tech stack, design requirements, tarot theme requirement

### Secondary (MEDIUM confidence)
- **GPTZero** — Direct observation of sentence-level highlights, color-coded results, export capabilities, educational resources
- **Your Logical Fallacy Is** — 24 fallacies with visual icons, linkable pages, downloadable resources
- **Kialo** — Structured debates, visual tree structure, pro/con organization, voting
- **Flask-Caching Documentation** — Caching strategies, Redis integration, cache invalidation
- **Flask-Limiter Documentation** — Rate limiting patterns, IP-based and user-based limits, distributed storage
- **web.dev Performance** — Long task optimization, third-party JavaScript best practices

### Tertiary (LOW confidence)
- **Logically Fallacious** — Searchable fallacy library, community archive (web-only observation)
- **Fallacy Files** — Fallacy blog format, glossary, taxonomy (web-only observation)
- **Your Bias Is** — Cognitive bias visual library (web-only observation, sister site to fallacy site)
- **Community patterns** — LLM integration best practices inferred from general AI application development (no specific studies on fallacy detection tools)

---
*Research completed: 2026-03-14*
*Ready for roadmap: yes*
