# Fallacy Tarot

## What This Is

Fully automated logical fallacy detection system that scrapes popular posts from Reddit, analyzes them for logical fallacies using Hugging Face LLM, generates mystical tarot card visuals with Stable Diffusion XL, and presents results in a beautiful web interface updated every 6 hours via GitHub Actions. Completely free technologies hosted on GitHub Pages.

## Core Value

Automatically discover and beautifully present logical fallacies from Reddit discussions to make critical thinking engaging and accessible.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Automated Reddit scraping of popular posts
- [ ] Hugging Face Mistral-7B-Instruct for fallacy detection
- [ ] Stable Diffusion XL for tarot card visual generation
- [ ] Tarot-themed web interface with slider navigation
- [ ] Voting system (upvote/downvote) with "Hot", "Best", "Newest" sorting
- [ ] GitHub Actions automation running every 6 hours
- [ ] Zero-cost deployment (free technologies only)
- [ ] GitHub Pages hosting for static web interface
- [ ] Detect all 10 fallacy types (Ad Hominem, Straw Man, Appeal to Authority, False Dilemma, Slippery Slope, Circular Reasoning, Hasty Generalization, Red Herring, Tu Quoque, Appeal to Emotion)
- [ ] Data persistence via JSON files (fallacies.json, archive.json)
- [ ] Placeholder tarot cards when image generation fails

### Out of Scope

- [User accounts and authentication] — Public read-only site, no user data collection needed
- [Backend server] — Static GitHub Pages hosting only
- [Database] — JSON file-based data storage sufficient
- [Real-time Reddit scraping] — Scheduled batch processing every 6 hours
- [Paid APIs or services] — Zero-cost requirement enforced
- [Mobile apps] — Web-only responsive interface
- [Multi-language support] — English-only for v1

## Context

**Current State:**
- GitHub Actions workflow exists (.github/workflows/fallacy_automation.yml)
- Fallacy analyzer script exists (scripts/fallacy_analyzer.py)
- Static HTML interface exists (docs/index.html)
- Data directories prepared (docs/data/, docs/assets/)
- Design assets available (logo_design.png, website_wireframe.png)

**Technical Foundation:**
- Data source: Reddit API (free)
- LLM analysis: Hugging Face Mistral-7B-Instruct
- Visual generation: Stable Diffusion XL
- Automation: GitHub Actions (runs every 6 hours: 00:00, 06:00, 12:00, 18:00 UTC)
- Hosting: GitHub Pages
- Frontend: Vanilla HTML/CSS/JavaScript (no frameworks)
- Data storage: JSON files (fallacies.json, archive.json)

**Design System:**
- Tarot-themed mystical visual design
- Slider navigation for browsing results
- Reddit-style upvote/downvote voting
- Sorting: "Hot", "Best", "Newest"
- Color palette: Mystical blues, purples, gold accents (from logo_design.png)

## Constraints

- **Cost**: Zero-cost requirement — use only free technologies (Reddit API, Hugging Face free tier, Stable Diffusion free tier, GitHub Pages free tier)
- **Automation**: Must run automatically every 6 hours via GitHub Actions
- **Hosting**: GitHub Pages only (static HTML, no backend server)
- **Frontend**: Vanilla JavaScript only (no frameworks like React)
- **Data**: JSON file-based storage (no databases)
- **LLM**: Hugging Face Mistral-7B-Instruct (free tier)
- **Image Generation**: Stable Diffusion XL (free tier)
- **Fallacy Types**: Must detect all 10 specific fallacy types listed in README

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Scheduled 6-hour automation | Reddit API rate limits, avoid spamming, balance freshness with cost | — Pending |
| Hugging Face over OpenAI | Zero-cost requirement, Mistral-7B-Instruct sufficient for fallacy detection | — Pending |
| Stable Diffusion XL | Free tier available, high-quality image generation suitable for tarot card visuals | — Pending |
| GitHub Pages static hosting | Zero-cost, automatic deployment, integrates with GitHub Actions workflow | — Pending |
| Vanilla JavaScript over frameworks | Simpler maintenance, faster page loads, meets zero-cost requirement | — Pending |
| JSON file storage | No database needed, simple data persistence, GitHub Pages compatible | — Pending |
| Slider navigation | Unique UX for browsing tarot cards, aligns with mystical theme | — Pending |

---
*Last updated: 2026-03-14 after initialization*
