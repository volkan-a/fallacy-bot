---
phase: 03
slug: voting-optimization
date: 2026-03-14
---

# Phase 03 Validation Strategy

## 1. Acceptance Criteria Checklist

| Requirement ID | Description | Validation Method |
| --- | --- | --- |
| VOTE-01 | Upvote/downvote buttons | Inspect UI for interactive voting buttons on each card. |
| VOTE-02 | Vote counts from JSON | Verify numbers displayed match `fallacies.json` initial values. |
| VOTE-03 | localStorage persistence | Vote on a card, refresh page, verify vote state remains. |
| VOTE-04 | "Hot" sorting algorithm | Select "Hot", verify cards reorder based on log(score)+time. |
| VOTE-05 | "Best" sorting algorithm | Select "Best", verify cards sort by net upvotes descending. |
| VOTE-06 | "Newest" sorting algorithm | Select "Newest", verify cards sort by timestamp descending. |
| PERF-01 | Page load < 3s (LCP < 2.5s) | Run Lighthouse / Chrome DevTools Performance tab. |
| PERF-02 | CLS < 0.1 | Run Lighthouse / Chrome DevTools Performance tab. |
| PERF-03 | INP < 200ms | Test interaction latency during sorting via DevTools. |
| PERF-04 | Lighthouse score 90+ | Run Lighthouse audit in Chrome. |

## 2. Testing Instructions

### Frontend Voting & Sorting
1. Open `docs/index.html` in a local browser.
2. Click upvote on the first card. Verify the count increments and the button shows active state.
3. Refresh the page. Verify the upvote remains active and the count includes your vote.
4. Try to upvote again. It should either remove the vote (toggle) or do nothing.
5. Use the sort dropdown to change from "Newest" to "Best". Verify the highest net score appears first.
6. Change to "Hot". Verify a mix of high scores and recent timestamps appear first.

### Performance
1. Run a Lighthouse audit on `docs/index.html` (served via local HTTP server).
2. Check that LCP is under 2.5s.
3. Rapidly change sorts and scroll; ensure no layout shifts occur (CLS < 0.1).

## 3. Key Risks & Mitigation

| Risk | Mitigation |
| --- | --- |
| Layout Shift during Sort | CSS grid with fixed aspect ratios for cards and images. |
| State desync | Rely on `localStorage` as source of truth for user's local votes, applied on top of JSON base. |
