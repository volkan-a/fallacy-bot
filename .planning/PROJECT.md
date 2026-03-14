# Know Your Fallacy

## What This Is

An AI-powered logical fallacy detection system that analyzes text input to identify common reasoning errors and provide visual explanations. Users can paste any text and receive detailed analysis of fallacies detected, with educational explanations and visual representations using a mystical tarot card theme.

## Core Value

Accurate and accessible detection of logical fallacies to improve critical thinking skills.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] User can input text for analysis
- [ ] System can detect logical fallacies using AI
- [ ] Results displayed in modern, responsive web interface
- [ ] Visual representations (tarot card theme) for each fallacy
- [ ] Educational explanations for each detected fallacy
- [ ] Category-based browsing of fallacies
- [ ] Mobile-responsive design
- [ ] Fast and intuitive user experience

### Out of Scope

- [Real-time Reddit analysis] — Initial focus on user-provided text input, automated Reddit scraping deferred to v2
- [User accounts and authentication] — Anonymous usage for v1, personal accounts and history deferred
- [Social features (voting, sharing)] — Core detection functionality prioritized, social engagement deferred
- [Multi-language support] — English-only for v1, internationalization in v2+

## Context

**Current State:**
- Initial development phase complete (React frontend, Flask backend, OpenAI API integration)
- Components implemented: Header, HeroSection, ResultsSection, FallacyCategories, Footer
- Responsive design implemented with Tailwind CSS
- Production deployed

**Technical Foundation:**
- Backend: Flask with Python, OpenAI API integration for fallacy detection
- Frontend: React.js with vanilla JavaScript components
- Design: Inter font, tarot-themed mystical visual design
- Performance targets: Page load <3s, FCP <1.5s, Lighthouse 90+
- Accessibility: WCAG 2.1 AA compliant

**Design System:**
- Color palette: Main Blue (#4A90A4), Dark Blue (#2C5F7A), Light Gray (#F8F9FA), White (#FFFFFF)
- Typography: Inter sans-serif, responsive sizing
- Layout: 3-column desktop, 2-column tablet, 1-column mobile

## Constraints

- **Tech Stack**: React.js, Flask, Python, Tailwind CSS, OpenAI API — existing codebase uses these
- **Performance**: Page load <3 seconds, FCP <1.5 seconds, Lighthouse 90+ score
- **Accessibility**: WCAG 2.1 AA standards, keyboard navigation, screen reader compatibility
- **Design**: Must use established color palette (#4A90A4 main), Inter font, tarot theme
- **Browser Support**: Modern browsers only (Chrome, Firefox, Safari, Edge recent versions)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| React.js frontend | Modern component-based architecture, existing codebase built with it | ✓ Good |
| Flask backend with Python | Simple, lightweight, integrates well with AI APIs | ✓ Good |
| OpenAI API for fallacy detection | Most accurate and comprehensive fallacy detection capabilities | — Pending |
| Tarot card visual theme | Unique, engaging user experience that differentiates from plain text tools | — Pending |
| Tailwind CSS for styling | Rapid UI development, responsive design, existing implementation | ✓ Good |

---
*Last updated: 2026-03-14 after initialization*
