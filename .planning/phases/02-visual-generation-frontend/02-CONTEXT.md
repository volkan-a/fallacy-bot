# Phase 02: Visual Generation & Frontend - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers the visual and frontend components of the Fallacy Tarot application. It involves integrating Stable Diffusion XL to generate mystical tarot card images for each detected fallacy, and building a responsive, zero-cost static web interface (HTML/CSS/JS) to beautifully display the analyzed Reddit posts.
</domain>

<decisions>
## Implementation Decisions

### UI Layout & Navigation
- A custom JavaScript slider component will be built to allow browsing the tarot cards (WEB-03).
- To balance the slider requirement with the responsive grid (WEB-05), the UI will feature a grid layout on desktop (3-column) and tablet (2-column), while acting as a horizontal slider/carousel on mobile (1-column).
- The visual theme will strictly use the defined color palette: mystical blues, purples, and gold accents (var(--bg-dark), var(--bg-card), var(--gold), etc. as already started in `index.html`).

### Image Generation
- Use Stable Diffusion XL via Hugging Face Inference API for image generation.
- Prompting Strategy: Hardcode base mystical tarot style prompts for each of the 10 fallacy types to ensure consistency (e.g., specific symbolic metaphors per fallacy type).
- Fallbacks (IMG-05): A default set of pre-generated "mystical generic" placeholder tarot cards will be used when the SDXL API fails or times out.

### Language & Content
- Current `index.html` is in Turkish, but project requirements specify English-only for v1. The interface must be updated to English to align with the roadmap and requirements.
- Missing JSON fields will be gracefully handled with user-friendly error messages (WEB-06).

### Claude's Discretion
- Exact implementation details of the custom JS slider.
- The specific visual metaphors in the Stable Diffusion prompts for each fallacy type (provided they fit the mystical tarot theme).
- Method of image lazy loading (Intersection Observer preferred for robust vanilla JS implementation).
</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docs/index.html` already contains basic CSS custom properties (colors like `--bg-dark`, `--gold`, `--purple`) and some layout structure. This will be refactored and built upon.
- `scripts/main.py` and `scripts/data_manager.py` from Phase 1 establish the JSON data structure and the execution flow, which the image generation script will need to hook into.

### Established Patterns
- Vanilla JS only (no React/Vue).
- Static file serving via GitHub Pages.
- Python scripts for automation pipeline steps.

### Integration Points
- Image generation script must run after `fallacy_analyzer.py` in the GitHub Actions pipeline, reading the JSON, generating missing images, and saving them to `docs/assets/`.
- Frontend JS will fetch the static `data/fallacies.json` file on load.
</code_context>

<specifics>
## Specific Ideas

- Ensure tarot cards have a mystical, elegant look.
- Use `loading="lazy"` or a lightweight Intersection Observer script for images to meet performance targets (LCP < 2.5s).
- Display a clear "Last updated" timestamp on the site (WEB-07).
</specifics>

<deferred>
## Deferred Ideas

- Voting System (upvote/downvote) and Sorting algorithms ("Hot", "Best", "Newest") are explicitly deferred to Phase 3.
</deferred>

---

*Phase: 02-visual-generation-frontend*
*Context gathered: 2026-03-14*
