---
phase: 02-visual-generation-frontend
plan: 04
type: execute
wave: 3
depends_on: [03]
files_modified: [docs/app.js, docs/index.html]
autonomous: true
requirements: [WEB-04, WEB-06, WEB-07]

must_haves:
  truths:
    - "Image lazy loading is implemented via intersection observer or loading='lazy'"
    - "Content validation handles missing JSON fields gracefully with error UI"
    - "Last updated timestamp displays correctly on the website"
  artifacts:
    - path: "docs/app.js"
      provides: "Data fetching from fallacies.json, mapping to HTML cards, and updating timestamp"
    - path: "docs/index.html"
      provides: "Timestamp container (#last-updated)"
---

<objective>
Connect the vanilla JavaScript UI to the generated `fallacies.json` payload, map data into the tarot cards, handle errors, lazy-load images, and show the last update timestamp.

Purpose: Dynamically load content into the web interface from the data files generated in Phase 1 and images from Phase 2.
Output: Data integration logic in `app.js` with lazy-loading and resilient field parsing.
</objective>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/phases/02-visual-generation-frontend/02-CONTEXT.md
</context>
