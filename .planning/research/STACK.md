# Technology Stack

**Project:** Know Your Fallacy - AI-Powered Logical Fallacy Detection
**Researched:** March 14, 2026
**Confidence:** HIGH

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **React** | ^18.3 | Frontend UI library | Industry standard for component-based UIs, extensive ecosystem, strong TypeScript support |
| **Next.js (App Router)** | ^15.1 | React meta-framework | Recommended by React team as preferred full-stack framework. Built-in Server Components, streaming, and AI SDK integration optimized for real-time applications |
| **Python** | 3.14+ | Backend runtime | Latest stable with async/await improvements and better type hints. End of support for 3.14 is Oct 2030 |
| **Flask** | 3.1+ | Web framework | Lightweight, simple, integrates well with OpenAI API. Existing codebase uses it successfully |
| **FastAPI** | 0.115+ | Alternative for new projects | High-performance async framework (par with Node.js/Go), automatic OpenAPI docs, type validation with Pydantic. Better for real-time AI apps than Flask |
| **OpenAI SDK (Python)** | latest (via pip) | AI API integration | Official SDK with automatic retries, streaming support, and structured outputs |
| **Tailwind CSS** | 4.2+ | Styling framework | Utility-first CSS with automatic purging. Used by OpenAI, Reddit, Shopify, and major platforms. v4 adds CSS variables, P3 colors, and improved performance |
| **Node.js** | 24.14 LTS | Frontend runtime | Current Long Term Support with security patches until April 2027 |

### Database (if needed)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **SQLite** | built-in | Development/test | Zero-config, perfect for MVP. No additional infrastructure needed |
| **PostgreSQL** | 16+ | Production (when needed) | When user accounts/history required. Robust, ACID-compliant, excellent JSON support |
| **Prisma ORM** | 6.x+ | Database access | Type-safe queries, automatic migrations, works seamlessly with Next.js and Python backends via API |

### AI/ML Integration

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **OpenAI Responses API** | latest | Fallacy detection | GPT-5.4 provides best reasoning capabilities for complex logical analysis. Responses API unifies chat and completion endpoints |
| **Structured Outputs** | included | Reliable fallacy classification | JSON schema validation ensures consistent response format for fallacy types and explanations |
| **Prompt Caching** | included | Cost optimization | Reuse prompts for similar queries, reduces API costs by 50%+ |

### Deployment & Hosting

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **Vercel** | N/A | Frontend deployment | Native Next.js platform with zero-config deployment, edge caching, and built-in AI observability |
| **Vercel AI Gateway** | N/A | AI request management | Centralized API management, rate limiting, cost tracking, and fallback handling for OpenAI calls |
| **Railway** | N/A | Backend deployment (alternative) | Simple Python/FastAPI deployment with built-in PostgreSQL. Free tier available |
| **Docker** | 24+ | Containerization | Reproducible builds, easy deployment to any cloud. Required for Railway and many other providers |

### Testing

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **Jest** | 30.0 | React unit/integration tests | Standard for React testing. Zero-config, parallel execution, snapshot testing, mocking built-in |
| **React Testing Library** | ^16.1 | Component testing | Tests user behavior, not implementation details. Accessibility-first approach (queries by label/text) |
| **pytest** | 8.x+ | Python backend tests | Detailed assertion introspection, auto-discovery, modular fixtures. Supports async/await natively |
| **httpx** | 0.28+ | Python HTTP client tests | Async HTTP client for testing Flask/FastAPI endpoints. Compatible with both frameworks |

### Monitoring & Observability

| Tool | Purpose | Notes |
|------|---------|-------|
| **Vercel Observability** | Track latency, errors, AI API costs | Included with Pro/Enterprise plans. Provides insights into Vercel Functions, External APIs (OpenAI), and Edge Requests |
| **Sentry** | Error tracking | Frontend + Python error aggregation. Free tier for small projects |
| **OpenTelemetry** | Standardized metrics | Export traces/logs to multiple backends. Future-proof if switching observability providers |

## Installation

```bash
# Frontend (Next.js with TypeScript)
npx create-next-app@latest --typescript --tailwind --eslint

# Core dependencies
npm install ai@latest  # Vercel AI SDK
npm install @vercel/ai-sdk
npm install openai  # If making direct OpenAI calls from frontend (not recommended)

# Testing
npm install -D jest @testing-library/react @testing-library/jest-dom
npm install -D @testing-library/user-event  # For simulating user interactions

# Backend (Python)
python3.14 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Core
pip install "fastapi[standard]"  # Includes uvicorn, jinja2, etc.
pip install "flask[async]"  # If staying with Flask

# AI SDK
pip install openai

# Testing
pip install pytest pytest-asyncio pytest-cov httpx

# Deployment (Docker)
# Create Dockerfile in backend root
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **Next.js (App Router)** | React Router + Vite | When you need complete control over build pipeline or want a simpler SPA without server features |
| **FastAPI** | Flask | For new AI projects: FastAPI is faster (async), has auto-generated OpenAPI docs, and better type safety |
| **Tailwind CSS** | CSS Modules | When you prefer scoped CSS with utility-free approach. More setup required, no design system constraints |
| **Vercel** | Netlify | When you prefer Netlify's workflow or have existing projects there. Both support Next.js equally well |
| **OpenAI** | Anthropic Claude | When you need specific model capabilities or better pricing for high-volume applications |
| **Jest** | Vitest | When using Vite exclusively. Vitest is faster but requires Vite setup |
| **PostgreSQL** | MongoDB | When your data is document-heavy and schema flexibility is more important than ACID compliance |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **Create React App (CRA)** | Deprecated by React team. No updates since 2022 | Next.js or Vite |
| **Flask** (for new AI apps) | Synchronous by default, slower than FastAPI, no automatic API docs | FastAPI |
| **Express.js** | TypeScript support requires extra setup, less opinionated | Next.js API routes or FastAPI |
| **Custom CSS without framework** | Maintenance nightmare, inconsistent design system | Tailwind CSS |
| **Mocha/Chai** | Requires more configuration than Jest | Jest or Vitest |
| **Unittest** (Python) | Verbose, less powerful than pytest | pytest |
| **Direct OpenAI calls from frontend** | Exposes API keys, no rate limiting control | Backend proxy with OpenAI SDK |
| **SQLite in production** | Not designed for concurrent writes | PostgreSQL |
| **Legacy APIs (Completions API)** | OpenAI is migrating to Responses API | OpenAI Responses API |
| **GPT-3.5** | Less accurate reasoning, more hallucinations | GPT-5.4 |

## Stack Patterns by Variant

**If building from scratch (greenfield):**
- Use **Next.js (App Router)** + **FastAPI** + **PostgreSQL**
- Because: FastAPI's async performance and automatic OpenAPI docs save hours. Next.js's Server Components reduce client bundle size and enable streaming AI responses.

**If migrating existing Flask app:**
- Keep **Flask** but add async support (`pip install "flask[async]"`)
- Because: Faster than full rewrite. Can migrate API endpoints to FastAPI incrementally.

**If budget-constrained MVP:**
- Use **Next.js** + **Flask** + **SQLite**
- Because: Zero database cost, Flask is free, Vercel has generous free tier. Scale to PostgreSQL/FastAPI when user accounts added.

**If real-time streaming responses required:**
- Use **Vercel AI SDK** with `streamText` in Next.js
- Because: Built-in streaming support for OpenAI. No need to handle SSE/WebSocket manually.

**If deploying to existing infrastructure:**
- Use **Docker** containers for both frontend and backend
- Because: Reproducible across any cloud provider (AWS, GCP, Azure, Railway, Render, etc.)

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Python 3.14 | Flask 3.1+, FastAPI 0.115+ | Full async/await support in all frameworks |
| React 18.3 | Next.js 15.1+ | Required for Server Components |
| Tailwind 4.2 | Next.js 15.1+ | v4 requires PostCSS 8+ |
| Jest 30.0 | React 18.3+ | Older Jest versions (29.x) work but lack latest features |
| OpenAI SDK latest | GPT-5.4, GPT-4.1 | SDK auto-updates, supports all current models |
| pytest 8.x | Python 3.10+ | Python 3.10 is minimum for async fixtures |

## Confidence Assessment

| Area | Confidence | Reason |
|------|------------|-------|
| Frontend Frameworks | HIGH | Recommendations from official React docs (Next.js as preferred), verified with current versions |
| Backend Frameworks | HIGH | Flask docs (3.1x) and FastAPI docs (current) reviewed. FastAPI performance benchmarks from official site |
| AI Integration | HIGH | OpenAI API docs verified (GPT-5.4, Responses API). SDK installation commands from quickstart |
| Styling | HIGH | Tailwind CSS v4.2 verified on official site. Major company users listed (OpenAI, Reddit, Shopify) |
| Deployment | HIGH | Vercel's AI templates and observability docs confirm strong AI app support |
| Testing | HIGH | Jest 30.0 and React Testing Library are de facto standards. pytest is dominant Python test framework |
| Monitoring | HIGH | Vercel Observability docs reviewed. OpenTelemetry is industry standard |

## Sources

- **React Docs** — "If you want to build a new app or website with React, we recommend starting with a framework. Next.js's App Router is a React framework that takes full advantage of React's architecture" (HIGH confidence)
- **Node.js** — Latest LTS v24.14.0 (verified from nodejs.org)
- **Python Downloads** — Python 3.14.3 is latest stable release (verified from python.org)
- **OpenAI API Docs** — GPT-5.4 model, Responses API, Python SDK installation commands (HIGH confidence)
- **FastAPI Docs** — Performance benchmarks, async support, automatic OpenAPI docs, Pydantic integration (HIGH confidence)
- **Flask Docs** — 3.1.x version, async support features (HIGH confidence)
- **Tailwind CSS** — v4.2 release, major users list (OpenAI, Reddit, Shopify, etc.), features documentation (HIGH confidence)
- **Jest Docs** — v30.0 release, features (zero-config, snapshots, parallel execution) (HIGH confidence)
- **React Testing Library** — Guiding principle, installation, testing best practices (HIGH confidence)
- **pytest Docs** — Features (assertion introspection, auto-discovery, fixtures), plugin ecosystem (HIGH confidence)
- **Vercel AI Templates** — AI chatbot, RAG templates, AI SDK integration patterns (HIGH confidence)
- **Vercel Observability Docs** — Tracking Vercel Functions, External APIs, AI Gateway requests (HIGH confidence)

---
*Stack research for: AI-Powered Logical Fallacy Detection System*
*Researched: March 14, 2026*
