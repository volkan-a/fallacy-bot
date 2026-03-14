---
phase: 02
slug: visual-generation-frontend
date: 2026-03-14
---

# Phase 02 Validation Strategy

## 1. Acceptance Criteria Checklist

| Requirement ID | Description | Validation Method |
| --- | --- | --- |
| IMG-01 | SDXL unique tarot card images | Inspect `docs/assets` generated images. |
| IMG-02 | Mystical tarot style prompts | Review `image_generator.py` prompt templates. |
| IMG-03 | Retry logic with backoff | Force API timeout in tests to verify backoff logs. |
| IMG-04 | Image compression < 500KB | Check file sizes in `docs/assets`. |
| IMG-05 | Fallback placeholder images | Delete network during generation, verify `placeholder.png` usage. |
| IMG-06 | Images stored correctly | Verify path `/docs/assets/fallacy_type_timestamp.png`. |
| WEB-01 | Static HTML/CSS/JS (no fw) | Audit `docs/` dir for any node_modules/react code. |
| WEB-02 | Tarot card display (mystical) | Visually inspect tarot card elements and color vars. |
| WEB-03 | Slider navigation UI | Test card slider on horizontal scroll in browser. |
| WEB-04 | Image lazy loading | Inspect DOM for `loading="lazy"`. |
| WEB-05 | Responsive design (1/2/3 cols) | Resize viewport and check breakpoints (mobile/tablet/desktop). |
| WEB-06 | Content validation/missing fields | Provide incomplete JSON, ensure UI renders gracefully without crash. |
| WEB-07 | "Last updated" timestamp | Check for timestamp element matching JSON metadata. |
| GHA-05 | SD_TOKEN securely accessed | Review workflow YAML for `${{ secrets.SD_TOKEN }}`. |
| SEC-04 | Vanilla JavaScript only | Read `docs/app.js` to confirm vanilla implementation. |

## 2. Testing Instructions

### Backend (Image Generation)
1. Provide a dummy `fallacies.json` with detected fallacies.
2. Run `python scripts/image_generator.py`.
3. Verify `docs/assets/` contains optimized `.png` files under 500KB.
4. Temporarily set an invalid SD_TOKEN and verify it falls back to `placeholder.png`.

### Frontend
1. Open `docs/index.html` in a local browser (or run `python -m http.server -d docs`).
2. Verify English language UI.
3. Verify mystical color theme is applied correctly.
4. Scale window down to <768px to ensure 1-column layout, and test horizontal slider mechanics.
5. Emulate slow 3G to watch for lazy loading.

## 3. Key Risks & Mitigation

| Risk | Mitigation |
| --- | --- |
| Image Generation Timeout | Aggressive retry logic (IMG-03) and robust fallback handling (IMG-05). |
| Heavy Initial Payload | Lazy loading implemented (WEB-04) and image compression downscaled <500KB (IMG-04). |
| JavaScript Crash on Missing Data | Content validation added (WEB-06). |
