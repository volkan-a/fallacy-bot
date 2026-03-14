---
phase: 03-voting-optimization
plan: 02
type: execute
wave: 2
depends_on: [01]
files_modified: [docs/index.html, docs/app.js]
autonomous: true
requirements: [VOTE-04, VOTE-05, VOTE-06]

must_haves:
  truths:
    - "Cards can be sorted by 'Hot' algorithm prioritizing fresh content"
    - "Cards can be sorted by 'Best' algorithm sorting by net upvotes"
    - "Cards can be sorted by 'Newest' algorithm sorting by timestamp"
    - "Sorting updates the DOM efficiently without causing page reloads"
  artifacts:
    - path: "docs/app.js"
      provides: "Sorting logic and event handlers"
    - path: "docs/index.html"
      provides: "Sorting dropdown/buttons UI"
---

<objective>
Implement the three sorting algorithms (Hot, Best, Newest) to allow users to order the displayed tarot cards based on their preferences.

Purpose: Provide dynamic content discovery methods for the tarot cards.
Output: Updated `app.js` with array sorting algorithms and DOM update logic, and `index.html` with a sorting control interface.
</objective>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/phases/03-voting-optimization/03-CONTEXT.md
</context>
