---
phase: 03-voting-optimization
plan: 03
type: execute
wave: 3
depends_on: [02]
files_modified: [docs/index.html, docs/style.css, docs/app.js]
autonomous: true
requirements: [PERF-01, PERF-02, PERF-03, PERF-04]

must_haves:
  truths:
    - "Page load time < 3 seconds (LCP < 2.5s target)"
    - "Cumulative Layout Shift (CLS) < 0.1"
    - "Interaction to Next Paint (INP) < 200ms"
    - "Lighthouse performance score 90+"
  artifacts:
    - path: "docs/index.html"
      provides: "Lazy-loaded images, optimized DOM structure"
    - path: "docs/style.css"
      provides: "Fixed aspect ratios to prevent CLS"
    - path: "docs/app.js"
      provides: "Event delegation and optimized DOM updates"
---

<objective>
Optimize the web interface to achieve strict performance metrics (Lighthouse 90+, LCP < 2.5s, CLS < 0.1, INP < 200ms) while retaining full visual and interactive capabilities.

Purpose: Deliver a high-performance, responsive experience across all devices.
Output: Refactored `index.html`, `style.css`, and `app.js` with performance best practices (lazy loading, explicit image dimensions, event delegation, and reduced main-thread blocking logic).
</objective>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/phases/03-voting-optimization/03-CONTEXT.md
</context>
