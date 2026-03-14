# Roadmap: Know Your Fallacy

**Created:** 2026-03-14
**Granularity:** Coarse (aggressive combination, critical path only)
**Coverage:** 38/38 v1 requirements mapped ✓

---

## Phases

- [ ] **Phase 1: Core Detection & Foundation** - Working fallacy detection with tarot visual theme, responsive design, and secure backend API
- [ ] **Phase 2: Visual Results & Library** - Enhanced results display with tarot cards, searchable fallacy library, and performance optimizations

---

## Phase Details

### Phase 1: Core Detection & Foundation

**Goal**: Users can input text and receive accurate logical fallacy detection with tarot-themed visual presentation

**Depends on**: Nothing (first phase)

**Requirements**: DETECT-01, DETECT-02, DETECT-03, DETECT-04, DETECT-06, DETECT-07, TAROT-01, TAROT-02, TAROT-03, TAROT-04, ACCESS-01, ACCESS-02, ACCESS-05, ACCESS-06, ACCESS-07, BACKEND-01, BACKEND-02, BACKEND-03, BACKEND-04, BACKEND-05, BACKEND-06 (21 requirements)

**Success Criteria** (what must be TRUE):
1. User can paste text (up to 10,000 characters) and see clear loading indicators while AI analyzes
2. System detects common logical fallacies and displays them with sentence-level highlighting and confidence scores
3. All components (text input, results display, tarot cards) render correctly on mobile (1-column), tablet (2-column), and desktop (3-column) layouts
4. User can navigate and interact with all interface elements using only keyboard controls, and screen readers announce all important content
5. All API calls are proxied through secure Flask backend with rate limiting, error handling, and no exposed API keys

**Plans**: TBD

---

### Phase 2: Visual Results & Library

**Goal**: Users can explore detected fallacies with rich tarot card visuals, detailed explanations, and browse a comprehensive fallacy library

**Depends on**: Phase 1 (Core Detection & Foundation)

**Requirements**: DETECT-05, VISUAL-01, VISUAL-02, VISUAL-03, VISUAL-04, VISUAL-05, VISUAL-06, VISUAL-07, LIBRARY-01, LIBRARY-02, LIBRARY-03, LIBRARY-04, LIBRARY-05, ACCESS-03, ACCESS-04 (17 requirements)

**Success Criteria** (what must be TRUE):
1. System identifies multiple fallacies in a single text and presents each with unique tarot card visuals, severity ratings, and context-sensitive explanations
2. User can search for specific fallacies and browse by category, with each fallacy displaying detailed explanations, real-world examples, and related fallacies suggestions
3. Fallacy results include color-coded highlights, severity ratings (minor vs major flaw), and citations showing exact line numbers and passages
4. Page loads in under 3 seconds with First Contentful Paint under 1.5 seconds, achieving Lighthouse score 90+
5. Caching reduces repeat analysis costs while maintaining accurate results, and all error scenarios provide clear user feedback

**Plans**: TBD

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Detection & Foundation | 0/0 | Not started | - |
| 2. Visual Results & Library | 0/0 | Not started | - |

---

## Coverage Map

| Requirement | Phase | Description |
|-------------|-------|-------------|
| DETECT-01 | Phase 1 | Text input up to 10,000 characters |
| DETECT-02 | Phase 1 | Fallacy detection via OpenAI API |
| DETECT-03 | Phase 1 | Sentence-level highlighting |
| DETECT-04 | Phase 1 | Confidence scores (High/Medium/Low) |
| DETECT-05 | Phase 2 | Multiple fallacies in single text |
| DETECT-06 | Phase 1 | Loading/processing indicators |
| DETECT-07 | Phase 1 | Error handling for API failures |
| VISUAL-01 | Phase 2 | Color-coded results display |
| VISUAL-02 | Phase 2 | Tarot card visual theme |
| VISUAL-03 | Phase 2 | Detailed fallacy explanations |
| VISUAL-04 | Phase 2 | Real-world examples |
| VISUAL-05 | Phase 2 | Fallacy severity ratings |
| VISUAL-06 | Phase 2 | Context-sensitive explanations |
| VISUAL-07 | Phase 2 | Citations of fallacy locations |
| LIBRARY-01 | Phase 2 | Searchable fallacy library |
| LIBRARY-02 | Phase 2 | Fallacy categorization |
| LIBRARY-03 | Phase 2 | Browsing by category with tarot design |
| LIBRARY-04 | Phase 2 | Detailed explanations and examples |
| LIBRARY-05 | Phase 2 | Related fallacy suggestions |
| TAROT-01 | Phase 1 | Mystical tarot card design system |
| TAROT-02 | Phase 1 | Visual metaphors for fallacies |
| TAROT-03 | Phase 1 | Consistent tarot-themed design |
| TAROT-04 | Phase 1 | Brand-appropriate color palette |
| ACCESS-01 | Phase 1 | Mobile-responsive design |
| ACCESS-02 | Phase 1 | WCAG 2.1 AA compliance |
| ACCESS-03 | Phase 2 | Performance targets (page load <3s, FCP <1.5s) |
| ACCESS-04 | Phase 2 | Lighthouse 90+ score |
| ACCESS-05 | Phase 1 | Inter font with responsive typography |
| ACCESS-06 | Phase 1 | Clear call-to-action buttons |
| ACCESS-07 | Phase 1 | Character counter for text input |
| BACKEND-01 | Phase 1 | Flask API routes |
| BACKEND-02 | Phase 1 | OpenAI API integration |
| BACKEND-03 | Phase 1 | Rate limiting |
| BACKEND-04 | Phase 1 | Caching strategy |
| BACKEND-05 | Phase 1 | Error handling and logging |
| BACKEND-06 | Phase 1 | CORS configuration |

**Total v1 requirements mapped:** 38/38 ✓

---

## Notes

### Phase 1 Research Flag
**Tarot visual design system** - Requires creative design work to map fallacy meanings to mystical tarot imagery. No clear patterns exist; this will be a design exploration during planning.

### Phase 2 Research Flags
- **Multi-fallacy detection prompt engineering** - Complex LLM task, may need experimentation with different prompt approaches during planning
- **Performance optimization** - May require tuning based on Phase 1 usage patterns

---

*Last updated: 2026-03-14*
