# Feature Landscape

**Domain:** Logical Fallacy Detection AI System
**Researched:** 2026-03-14

## Table Stakes

Features users expect. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Text Input Methods** (paste text box, character counter, clear button) | Users need to input text to analyze; standard UX pattern | Low | Must handle 10,000+ characters based on GPTZero patterns |
| **Fallacy Detection** (identify common fallacies in text) | Core value proposition - without detection, no product exists | High | AI-dependent; requires integration with OpenAI API or similar |
| **Visual Results Display** (highlighted fallacies, color-coded) | Users expect to see where fallacies occur in their text | Medium | Sentence-level highlighting is standard expectation (GPTZero pattern) |
| **Fallacy Explanations** (what is it, why it's a fallacy) | Educational value requires understanding, not just detection | Low | Essential for learning; can be pre-written content for common fallacies |
| **Examples for Each Fallacy** (real-world examples) | Helps users recognize fallacies in context | Low | Can use curated examples from existing databases |
| **Searchable Fallacy Library** (browse by category or name) | Users often want to learn about specific fallacies, not just analyze text | Medium | Category-based navigation is established pattern (Your Logical Fallacy Is, Kialo) |
| **Mobile-Responsive Design** (works on all devices) | Modern web app requirement per PROJECT.md constraints | Low | Required for accessibility; tablets and phones common usage |
| **Clear Loading/Processing Indicators** (spinners, progress) | AI analysis takes time; users need feedback about what's happening | Low | Standard UX pattern for async operations |
| **Error Handling** (invalid input, API failures) | Robust systems handle errors gracefully | Medium | Must handle network errors, rate limits, malformed input |
| **Accessibility Compliance** (WCAG 2.1 AA, keyboard nav, screen reader) | Required by PROJECT.md constraints; legal requirement for public web tools | Low | Keyboard navigation and ARIA labels essential |
| **Clear Call-to-Actions** (analyze button, learn more) | Users need to know what to do next | Low | Primary action must be visually prominent |

## Differentiators

Features that set product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Tarot Card Visual Theme** (mystical, engaging visual design for each fallacy) | Unique branding; memorable; differentiates from plain text competitors | Medium | Explicit PROJECT.md requirement; creates emotional connection |
| **Visual Metaphors** (tarot card imagery that relates to fallacy meaning) | Aids memory retention; makes abstract concepts concrete | High | Requires design work mapping fallacies to visual symbols |
| **Sentence-Level Highlights with Confidence Scores** (show exactly which text, how certain) | Transparency builds trust; helps users understand AI confidence | Medium | GPTZero pattern - color-coded by confidence level (High/Medium/Low) |
| **Multi-Fallacy Detection** (identify multiple fallacies in single text) | Real-world arguments contain multiple errors; users want complete analysis | High | Requires sophisticated AI to avoid false positives and overlapping detections |
| **Context-Sensitive Explanations** (explain in context of user's specific text) | More helpful than generic explanations; personalized learning | Medium | Requires AI to generate context-aware explanations, not just fetch pre-written content |
| **Fallacy Severity Rating** (minor issue vs major logical flaw) | Helps users prioritize what to address first | Medium | Useful for educational context and practical improvement |
| **Related Fallacy Suggestions** (if X is present, check for Y) | Fallacies often cluster; encourages deeper learning | Medium | Pattern-based recommendations (e.g., ad hominem often co-occurs with straw man) |
| **Export Results** (PDF, shareable link, copy formatted text) | Useful for students, teachers, researchers; enables sharing | Medium | GPTZero offers this; expected in educational tools |
| **Citation of Detected Fallacy Locations** (line numbers, highlighted passages) | Helps users return to specific parts of their text | Low | Standard feature in text analysis tools |
| **Visual Fallacy Relationships** (how fallacies relate to each other) | Helps users understand the taxonomy and connections | High | Could use interactive graph or tree structure |
| **Progress Tracking** (fallacies you've learned, improvement over time) | Gamification increases engagement; educational value | High | Requires user accounts (deferred to v2 per PROJECT.md) |
| **Practice Mode** (sample texts to test your detection skills) | Active learning is more effective than passive reading | Medium | Requires curated sample texts with known fallacies |
| **Difficulty Levels** (beginner, intermediate, advanced analysis) | Makes tool accessible to users with varying expertise | Medium | Affects depth of explanations and detection sensitivity |
| **Real-Time Analysis Preview** (show detection as you type, with debounce) | Immediate feedback improves UX; reduces wait time | Medium | Debouncing required to avoid excessive API calls |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Social Features** (voting, sharing to social media, comments) | Out of scope per PROJECT.md v1; adds complexity; privacy concerns | Focus on core detection; defer to v2+ |
| **User Accounts and Authentication** (login, profiles, history) | Out of scope per PROJECT.md v1; adds infrastructure complexity; anonymous usage for v1 | Browser-based session storage for temporary history; defer accounts to v2 |
| **Multi-Language Support** (non-English UI or analysis) | Out of scope per PROJECT.md v1; requires translation resources; English-only for v1 | Focus on English content quality; defer i18n to v2+ |
| **Real-Time Reddit/Forum Scraping** (automated analysis of external content) | Out of scope per PROJECT.md v1; legal and technical challenges | Manual text input only; defer automated scraping to v2 |
| **Grammar/Spelling Correction** (integrated grammar checker) | Not core value; GPTZero has this but it's secondary to fallacy detection | Focus on fallacies; partner with or recommend grammar tools |
| **AI Detection** (detect if text is AI-generated like GPTZero) | Different product category; dilutes focus on logical fallacies | Stick to fallacy detection; avoid feature creep |
| **Debate Platform** (structured arguments, pro/con like Kialo) | Different product category; complex moderation required | Focus on analysis, not facilitation of debates |
| **Paid Subscriptions/Monetization** (premium tiers, paywalls) | V1 is validation phase; monetization premature | Free access to gather usage data and feedback |
| **Native Mobile Apps** (iOS/Android applications) | Out of scope per PROJECT.md (web-only); expensive development | Progressive Web App (PWA) capabilities; defer native apps to v2+ |
| **Advanced AI Model Training** (custom ML models beyond OpenAI API) | High complexity; time/resource intensive; OpenAI API sufficient | Use OpenAI API for v1; evaluate custom models for v2+ |
| **Community Forums or Q&A** (like Logically Fallacious archive) | Requires moderation; out of scope per PROJECT.md v1 | Use existing resources (e.g., Stanford Encyclopedia of Philosophy) for deep dives |

## Feature Dependencies

```
Text Input → Fallacy Detection → Visual Results Display
                                                ↓
                           Fallacy Explanations ← Category Browsing

Fallacy Detection → Sentence-Level Highlights → Confidence Scores
                                                  ↓
                                    Context-Sensitive Explanations

Visual Results Display → Export Results
                         ↓
              Citation of Locations

Fallacy Library → Search → Browse by Category
                                    ↓
                       Related Fallacy Suggestions

Tarot Card Visual Design → All visual displays (results, library, examples)
```

**Critical Dependencies:**
1. **Fallacy Detection → Visual Results Display**: Can't show results without detection
2. **Fallacy Library → Search/Browse**: Library must exist before it can be searched
3. **OpenAI API Integration → Context-Sensitive Explanations**: Requires AI to generate context-aware content
4. **User Accounts (deferred) → Progress Tracking**: Can't track progress without user identity

**Independent Features (can be built in parallel):**
- Tarot visual design system
- Fallacy library content (explanations, examples)
- Mobile-responsive layout
- Accessibility features

## MVP Recommendation

Prioritize for v1:
1. **Text Input with character counter** (Table stakes - essential)
2. **Fallacy Detection using OpenAI API** (Table stakes - core product)
3. **Visual Results Display with sentence-level highlights** (Table stakes - expected UX)
4. **Fallacy Explanations with examples** (Table stakes - educational value)
5. **Searchable Fallacy Library with categories** (Table stakes - learning resource)
6. **Tarot Card Visual Theme for fallacies** (Differentiator - core brand)
7. **Mobile-responsive design** (Table stakes - required by PROJECT.md)
8. **Accessibility compliance (WCAG 2.1 AA)** (Table stakes - required by PROJECT.md)

**One Differentiator in MVP:**
- **Tarot Card Visual Theme** (unique branding; memorable; PROJECT.md requirement)

Defer:
- **User accounts and history** (deferred to v2 per PROJECT.md)
- **Progress tracking and gamification** (requires accounts; defer to v2)
- **Export features** (nice to have; can add after core works)
- **Real-time preview** (complexity vs value tradeoff; defer post-v1)
- **Multi-language support** (deferred to v2 per PROJECT.md)
- **Social features** (deferred to v2 per PROJECT.md)

**Rationale:** Focus on core detection + unique tarot theme for v1. Get the fundamental value proposition working with visual polish. Advanced features can be added once users validate the core concept.

## Sources

- **Your Logical Fallacy Is** (yourlogicalfallacyis.com) - MEDIUM confidence - Direct observation of 24 fallacies with visual icons, linkable pages, downloadable resources (LOW confidence - web-only, no official docs)
- **Kialo** (kialo.com) - MEDIUM confidence - Direct observation of structured debates, visual tree structure, pro/con organization, voting, tagging (LOW confidence - web-only)
- **GPTZero** (gptzero.me) - HIGH confidence - Direct observation of AI detector features, sentence-level highlights, color-coded results, export capabilities, integrations, educational resources (MEDIUM confidence - official site with detailed feature descriptions)
- **Logically Fallacious** (logicallyfallacious.com) - MEDIUM confidence - Direct observation of searchable fallacy library, community archive, featured fallacies (LOW confidence - web-only)
- **Fallacy Files** (fallacyfiles.org) - MEDIUM confidence - Direct observation of fallacy blog format, glossary, taxonomy, historical perspective (LOW confidence - web-only)
- **Your Bias Is** (yourbias.is) - LOW confidence - Direct observation of cognitive bias visual library (sister site to fallacy site; similar patterns expected)
- **PROJECT.md** (project documentation) - HIGH confidence - Explicit project constraints, tech stack, design requirements

## Notes on Confidence Levels

- **HIGH:** Official project documentation, authoritative sources
- **MEDIUM:** Direct observation of competitor features from official websites with multiple feature examples
- **LOW:** Web-only sources without additional verification, single-source observations

**Gaps in Research:**
- No access to modern AI reasoning analysis tools (some URLs inaccessible or under construction)
- Limited data on user expectations for fallacy detection specifically (inferred from related tools)
- No official studies on what features users value most in fallacy detection tools
- Limited verification beyond direct website observation (no usage statistics, user reviews, or case studies)

**Research Flags for Phases:**
- Phase 1 (MVP): Standard web tool patterns - minimal additional research needed
- Phase 2 (Advanced features): User research recommended for prioritizing export, progress tracking, practice mode
- Phase 3 (Integrations): Research required for API, LMS integrations (Canvas, Google Classroom)
