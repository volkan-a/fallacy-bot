# Requirements: Know Your Fallacy

**Defined:** 2026-03-14
**Core Value:** Accurate and accessible detection of logical fallacies to improve critical thinking skills.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Core Detection

- [ ] **DETECT-01**: User can input text (up to 10,000 characters) via paste or text box
- [ ] **DETECT-02**: System detects common logical fallacies in user-provided text using OpenAI API
- [ ] **DETECT-03**: System provides sentence-level highlighting for detected fallacies
- [ ] **DETECT-04**: System displays confidence scores (High/Medium/Low) for each detected fallacy
- [ ] **DETECT-05**: System can identify multiple fallacies in a single text
- [ ] **DETECT-06**: Clear loading/processing indicators during AI analysis
- [ ] **DETECT-07**: Robust error handling for API failures, rate limits, and network errors

### Visual Results

- [ ] **VISUAL-01**: Color-coded display of fallacy detection results in text
- [ ] **VISUAL-02**: Tarot card visual theme for each detected fallacy
- [ ] **VISUAL-03**: Detailed explanation of what each fallacy is and why it's incorrect
- [ ] **VISUAL-04**: Real-world examples for each detected fallacy
- [ ] **VISUAL-05**: Fallacy severity rating (minor issue vs major logical flaw)
- [ ] **VISUAL-06**: Context-sensitive explanations based on user's specific text
- [ ] **VISUAL-07**: Citation of detected fallacy locations (line numbers, highlighted passages)

### Fallacy Library

- [ ] **LIBRARY-01**: Searchable library of common logical fallacies
- [ ] **LIBRARY-02**: Fallacy categorization (formal, informal, relevance, ambiguity, etc.)
- [ ] **LIBRARY-03**: Browsing by category with tarot card visual design
- [ ] **LIBRARY-04**: Detailed explanations, examples, and related fallacies for each fallacy
- [ ] **LIBRARY-05**: Related fallacy suggestions (if X is present, check for Y)

### Tarot Theme & Design

- [ ] **TAROT-01**: Mystical tarot card visual design system for all fallacy displays
- [ ] **TAROT-02**: Visual metaphors that relate fallacy meaning to tarot imagery
- [ ] **TAROT-03**: Consistent tarot-themed design across all components
- [ ] **TAROT-04**: Brand-appropriate color palette (#4A90A4 main blue, #2C5F7A dark blue)

### Accessibility & Performance

- [ ] **ACCESS-01**: Mobile-responsive design (desktop 3-column, tablet 2-column, mobile 1-column)
- [ ] **ACCESS-02**: WCAG 2.1 AA compliance (keyboard navigation, screen reader compatibility, sufficient color contrast)
- [ ] **ACCESS-03**: Page load time < 3 seconds, First Contentful Paint < 1.5 seconds
- [ ] **ACCESS-04**: Lighthouse performance score 90+
- [ ] **ACCESS-05**: Inter font family with responsive typography
- [ ] **ACCESS-06**: Clear call-to-action buttons (analyze, learn more, clear)
- [ ] **ACCESS-07**: Character counter for text input field

### Backend & Infrastructure

- [ ] **BACKEND-01**: Flask backend API routes for fallacy detection
- [ ] **BACKEND-02**: OpenAI API integration with GPT-5.4 model
- [ ] **BACKEND-03**: Rate limiting to control OpenAI API costs and prevent abuse
- [ ] **BACKEND-04**: Caching strategy for fallacy analysis results
- [ ] **BACKEND-05**: Error handling and logging for API failures
- [ ] **BACKEND-06**: CORS configuration for React frontend communication

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### User Accounts & Tracking

- **USER-01**: User account creation with email/password
- **USER-02**: User profiles with fallacy analysis history
- **USER-03**: Progress tracking (fallacies learned, improvement over time)
- **USER-04**: Personalized learning recommendations

### Advanced Features

- **ADV-01**: Export results (PDF, shareable link, copy formatted text)
- **ADV-02**: Practice mode with sample texts
- **ADV-03**: Real-time analysis preview with debounce
- **ADV-04**: Difficulty levels (beginner, intermediate, advanced)
- **ADV-05**: Visual fallacy relationships (interactive graph or tree)

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Social features (voting, sharing, comments) | Out of scope per PROJECT.md v1; adds complexity; privacy concerns |
| User accounts and authentication | Out of scope per PROJECT.md v1; adds infrastructure complexity; anonymous usage for v1 |
| Multi-language support | Out of scope per PROJECT.md v1; requires translation resources; English-only for v1 |
| Real-time Reddit/forum scraping | Out of scope per PROJECT.md v1; legal and technical challenges |
| Grammar/spelling correction | Not core value; partner with or recommend grammar tools |
| AI detection (detect if text is AI-generated) | Different product category; dilutes focus on logical fallacies |
| Debate platform (structured arguments, pro/con) | Different product category; complex moderation required |
| Paid subscriptions/monetization | V1 is validation phase; monetization premature |
| Native mobile apps (iOS/Android) | Out of scope per PROJECT.md (web-only); expensive development |
| Advanced AI model training (custom ML) | High complexity; time/resource intensive; OpenAI API sufficient |
| Community forums or Q&A | Requires moderation; out of scope per PROJECT.md v1 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DETECT-01 | Phase 1 | Pending |
| DETECT-02 | Phase 1 | Pending |
| DETECT-03 | Phase 1 | Pending |
| DETECT-04 | Phase 1 | Pending |
| DETECT-05 | Phase 2 | Pending |
| DETECT-06 | Phase 1 | Pending |
| DETECT-07 | Phase 1 | Pending |
| VISUAL-01 | Phase 2 | Pending |
| VISUAL-02 | Phase 2 | Pending |
| VISUAL-03 | Phase 2 | Pending |
| VISUAL-04 | Phase 2 | Pending |
| VISUAL-05 | Phase 2 | Pending |
| VISUAL-06 | Phase 2 | Pending |
| VISUAL-07 | Phase 2 | Pending |
| LIBRARY-01 | Phase 2 | Pending |
| LIBRARY-02 | Phase 2 | Pending |
| LIBRARY-03 | Phase 2 | Pending |
| LIBRARY-04 | Phase 2 | Pending |
| LIBRARY-05 | Phase 2 | Pending |
| TAROT-01 | Phase 2 | Pending |
| TAROT-02 | Phase 2 | Pending |
| TAROT-03 | Phase 2 | Pending |
| TAROT-04 | Phase 1 | Pending |
| ACCESS-01 | Phase 1 | Pending |
| ACCESS-02 | Phase 1 | Pending |
| ACCESS-03 | Phase 2 | Pending |
| ACCESS-04 | Phase 2 | Pending |
| ACCESS-05 | Phase 1 | Pending |
| ACCESS-06 | Phase 1 | Pending |
| ACCESS-07 | Phase 1 | Pending |
| BACKEND-01 | Phase 1 | Pending |
| BACKEND-02 | Phase 1 | Pending |
| BACKEND-03 | Phase 1 | Pending |
| BACKEND-04 | Phase 1 | Pending |
| BACKEND-05 | Phase 1 | Pending |
| BACKEND-06 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 38 total
- Mapped to phases: 0
- Unmapped: 38 ⚠️

---
*Requirements defined: 2026-03-14*
*Last updated: 2026-03-14 after initial definition*
