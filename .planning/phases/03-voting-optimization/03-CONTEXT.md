# Phase 03: Voting & Optimization - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers the interactive voting system and performance optimization for the Fallacy Tarot application. It implements client-side upvote/downvote mechanics with sorting algorithms (Hot, Best, Newest) and optimizes the application to meet strict performance metrics (LCP < 2.5s, CLS < 0.1, Lighthouse 90+).
</domain>

<decisions>
## Implementation Decisions

### Voting Mechanics
- Voting is entirely client-side, persisting user interactions (upvotes/downvotes) to `localStorage` to prevent duplicate voting (VOTE-03).
- The base vote counts are initialized from the JSON data (VOTE-02), and the frontend visually increments them upon user interaction.
- Real-time global vote synchronization is explicitly out of scope (ADV-07) to maintain the zero-cost, no-backend constraint.

### Sorting Algorithms
- **Newest:** Standard descending chronological sort by timestamp (VOTE-06).
- **Best:** Simple net score sort (`upvotes - downvotes`) (VOTE-05).
- **Hot:** A simplified Wilson score interval implementation or a Reddit-style "Hot" algorithm (logarithmic scale of score + timestamp decay) to prioritize fresh, engaging content (VOTE-04).

### Performance Optimization
- Native browser lazy loading (`loading="lazy"`) and optimized image assets (from Phase 2) will be leveraged to meet the LCP < 2.5s target (PERF-01, PERF-04).
- The CSS layout will use explicit dimensions for images/containers to prevent Cumulative Layout Shift (CLS < 0.1) during dynamic sorting or slider navigation (PERF-02).
- Vanilla JavaScript event delegation will be used to keep Interaction to Next Paint (INP) under 200ms (PERF-03).

### Claude's Discretion
- The exact mathematical formula for the "Hot" sorting algorithm (balancing complexity vs. performance).
- The visual feedback mechanism for casting a vote (e.g., color change, subtle animation).
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docs/index.html` structure from Phase 2 provides the container and styling for the tarot cards where the voting UI will be injected.
- The vanilla JS data fetching and rendering logic established in Phase 2 can be extended to include sorting functions.

### Established Patterns
- Vanilla JS (no frameworks) and static JSON data.
- Strict zero-cost constraint limits voting to a localized experience.

### Integration Points
- Sorting controls (dropdown or buttons) must be added to the main UI.
- The voting state needs to hook into the JSON rendering loop to display correct active states for previously voted cards.
</code_context>

<specifics>
## Specific Ideas

- Ensure sorting transitions are smooth and don't cause jarring reflows (important for CLS).
- Use intuitive, recognizable icons for upvote/downvote (e.g., arrows or mystical symbols aligned with the tarot theme).
</specifics>

<deferred>
## Deferred Ideas

- Global/Real-time vote synchronization (ADV-07) — requires a backend/WebSocket, violates zero-cost constraint.
- User accounts for cross-device vote persistence (ADV-08).

</deferred>

---

*Phase: 03-voting-optimization*
*Context gathered: 2026-03-14*
