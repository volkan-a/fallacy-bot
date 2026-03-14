# Domain Pitfalls

**Domain:** AI-Powered Text Analysis (Logical Fallacy Detection)
**Researched:** 2026-03-14
**Confidence:** HIGH (based on official documentation and common patterns)

## Critical Pitfalls

### Pitfall 1: Blocking LLM API Calls on the Main Thread

**What goes wrong:**
When a user submits text for fallacy analysis, the frontend waits for the backend's LLM API call to complete before responding. If the API takes 5-10 seconds (typical for complex text analysis), the UI appears frozen. Users may click "Analyze" multiple times, thinking it's broken, which triggers duplicate API calls and spirals costs.

**Why it happens:**
Developers forget that LLM API calls are inherently slow and unpredictable. They make synchronous API calls from React event handlers without showing loading states, or worse, make the calls directly from the frontend (bypassing rate limits and exposing API keys).

**How to avoid:**
1. Always use async/await patterns with explicit loading states
2. Disable submit buttons during API calls (prevent double submissions)
3. Implement progressive loading: show "Analyzing..." immediately, then results when ready
4. Never make LLM API calls directly from the frontend - route through Flask backend
5. Set reasonable timeouts and handle failures gracefully

**Warning signs:**
- Users clicking buttons multiple times
- Browser DevTools shows long tasks (>50ms) blocking interactions
- React Profiler shows components re-rendering unnecessarily during API calls
- Duplicate submissions appearing in your backend logs

**Phase to address:**
Phase 1 (MVP). This is foundational - without proper async handling, the app feels broken from day one.

---

### Pitfall 2: Exposing API Keys and No Rate Limiting

**What goes wrong:**
Frontend makes direct calls to OpenAI API with keys embedded in client-side code. Any user can extract the key and use your quota. Alternatively, Flask backend doesn't implement rate limiting, so a single user (or bot) can rapidly submit requests and exhaust your API budget.

**Why it happens:**
Developers prototype with direct API calls for speed, then forget to move to backend. Even when using Flask, they assume "users won't abuse it" or "our API quota is large enough." Rate limiting is seen as "something to add later."

**How to avoid:**
1. NEVER store API keys in client-side code (use environment variables on backend)
2. Implement per-IP rate limiting in Flask (use Flask-Limiter)
3. Implement per-user rate limiting when accounts are added (v2+)
4. Set explicit API usage quotas in OpenAI dashboard
5. Log all API calls with user identifiers for abuse detection
6. Add a circuit breaker to temporarily disable analysis when quota is near limit

**Warning signs:**
- API keys visible in browser DevTools (Sources/Network tabs)
- Sudden spike in API costs unrelated to traffic
- Flask logs show many requests from single IP
- OpenAI dashboard shows usage exceeding expected patterns

**Phase to address:**
Phase 1 (MVP). Security and cost control are not "nice to have" - they prevent the project from becoming financially unsustainable.

---

### Pitfall 3: Naive Caching Leading to Wrong Results

**What goes wrong:**
Flask implements caching of LLM responses to save costs and improve speed. However, caching is based on exact text match only. Two users submit similar but not identical texts:
- User 1: "This is a straw man argument"
- User 2: "This is a strawman argument"

The second request hits the cache from the first, but if LLM's interpretation was context-dependent or the prompt was updated, the second user gets stale or incorrect results. Worse, cache keys don't account for LLM model version updates.

**Why it happens:**
Developers implement simple `@cache.memoize` decorators without considering the semantic nature of text analysis. They optimize for "exact match" without thinking about "equivalent meaning."

**How to avoid:**
1. If caching, use semantic hashing or normalization (lowercase, remove extra whitespace)
2. Include LLM model version in cache keys
3. Set appropriate TTL (e.g., 24 hours) to prevent indefinite staleness
4. Allow cache invalidation when fallacy detection logic changes
5. Consider whether caching is appropriate for your use case - sometimes it's better not to cache
6. Add cache statistics to monitoring (hit rate, stale entries)

**Warning signs:**
- Users report inconsistent results for similar inputs
- Results don't reflect updates to your detection logic
- Cache hit rate is suspiciously high for an AI tool
- Tests pass with exact matches but fail with slight variations

**Phase to address:**
Phase 2 (Optimization). Implement basic caching only after core detection works, and add cache management in Phase 3.

---

### Pitfall 4: Missing Error Handling for LLM Failures

**What goes wrong:**
OpenAI API returns 429 (rate limit exceeded), 500 (service unavailable), or the response is malformed/partial. Flask returns a generic 500 error to the frontend, which shows a blank "Something went wrong" message with no explanation. Users don't know if they should retry, if the problem is temporary, or if their text was problematic.

**Why it happens:**
Developers focus on happy path and assume LLM APIs always work. They don't handle edge cases like rate limiting, timeouts, or malformed responses. Error handling is deferred to "later," which often means never.

**How to avoid:**
1. Handle specific LLM API errors with user-friendly messages:
   - 429: "We're processing many requests right now. Please try again in a few minutes."
   - 500/503: "Our AI service is temporarily unavailable. Please try again later."
2. Implement exponential backoff for retryable errors
3. Validate LLM responses before returning to frontend (check expected structure)
4. Log detailed error info for debugging but show generic messages to users
5. Add retry buttons for transient failures
6. Implement fallback responses (e.g., "We couldn't analyze this text, but here's a general explanation of [fallacy]")

**Warning signs:**
- Sentry/bug tracking shows many unhandled API errors
- User feedback mentions "blank screen" or "no explanation"
- No error messages in UI logs when things fail
- Frontend shows same error for all types of failures

**Phase to address:**
Phase 1 (MVP). Error handling is part of core functionality, not an afterthought.

---

### Pitfall 5: Over-fetching Large Results and Poor UX

**What goes wrong:**
LLM returns detailed analysis for 10 fallacies when the user's text only contains 2. The UI shows all 10 results, overwhelming the user with irrelevant information. Conversely, for complex texts, only a short summary is shown without detail, leaving users wanting more. There's no balance - too much or too little.

**Why it happens:**
Developers use generic prompts ("analyze this text for fallacies") without specifying output format or detail level. They don't consider UX - what users actually need vs. what the model provides.

**How to avoid:**
1. Use structured prompts that specify desired output format
2. Implement progressive disclosure: show summary first, allow user to expand for details
3. Limit results to top N fallacies by confidence score
4. Allow user preferences: "brief explanation" vs "detailed analysis"
5. Validate that responses are concise and relevant to input text
6. A/B test different result presentations to find optimal UX

**Warning signs:**
- User analytics show short session times (users overwhelmed)
- Feedback requests mention "too much information" or "not enough detail"
- Heatmaps show users scrolling past long result sections
- Accessibility testing flags overwhelming content density

**Phase to address:**
Phase 1 (MVP) for basic result display, Phase 2 (UX Refinement) for optimization based on user feedback.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcoding prompt templates in Python | Faster initial development | Impossible to A/B test prompts, difficult to optimize | Never - use configuration files or database from start |
| No tests for LLM responses | Save development time | Regression bugs when prompts change, can't verify improvements | Only for quick prototype (discard code), never ship to production |
| Using Flask development server in production | Works locally, easy to deploy | Poor performance, security issues, crashes under load | Never - documented as production-unsafe in Flask docs |
| Skipping proxy configuration | Simpler deployment | Wrong client IPs in logs, security issues behind reverse proxy | Never - required for any real deployment |
| Direct API calls from frontend for prototyping | Faster iteration cycles | Security risk, no rate limiting, exposed keys | Only local development, never commit to repo |
| Monolithic Flask route for all analysis | Simple code structure | Hard to test, impossible to scale independently, can't optimize specific fallacies | Only MVP, refactor in Phase 2 |
| No caching of static assets | Simpler build process | Slower page loads, worse Lighthouse scores, higher bandwidth costs | Only development, always cache in production |

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| OpenAI API | Using `gpt-4` for all requests (expensive) | Use `gpt-3.5-turbo` for simple queries, `gpt-4` only for complex cases |
| OpenAI API | Not setting `max_tokens`, allowing runaway responses | Always set reasonable `max_tokens` based on expected output length |
| OpenAI API | Not setting `temperature`, getting inconsistent results | Set `temperature=0` for deterministic fallacy detection |
| OpenAI API | Retrying all errors indefinitely | Retry only specific errors (429, 500, 502, 503, 504) with backoff |
| Flask + OpenAI | Making synchronous calls, blocking other requests | Use `async` Flask routes or background tasks for long-running LLM calls |
| Flask + OpenAI | Not handling rate limits, cascading failures | Implement per-endpoint rate limiting with Flask-Limiter |
| React + Flask | CORS errors in production | Configure Flask-CORS properly with specific origins, not wildcard |
| React + Flask | No proxy configuration, frontend calls fail on deploy | Use Flask's `ProxyFix` middleware behind reverse proxy |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|-----------------|
| Synchronous LLM calls in Flask routes | Requests queue up, timeouts increase, users see slow responses | Use async routes (`@app.route(..., async=True)`) or background tasks (`Celery`) | At 10+ concurrent users with 5s+ LLM response times |
| No response streaming | UI frozen during analysis, poor INP scores | Implement server-sent events (SSE) or WebSocket for streaming results | When LLM responses exceed 3 seconds |
| Full page reloads on each analysis | Jarring UX, lost scroll position, slow perceived performance | Use AJAX/fetch for API calls, update DOM dynamically | Immediately - never acceptable in modern SPA |
| No code splitting in React | Large initial bundle, slow FCP, poor Lighthouse scores | Use React.lazy() and Suspense for code splitting | When React bundle exceeds 200KB |
| Not optimizing images | Slow LCP, bandwidth waste | Use WebP, responsive images, lazy loading | Immediately - Lighthouse flags immediately |
| Rendering large tarot card images | Memory issues, slow paint | Use SVG or optimize PNG, lazy load below fold | When tarot card assets exceed 500KB total |
| No debouncing on user input | Excessive API calls, rate limit hits | Implement 500ms debounce on text input | When users type/paste text rapidly |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| API keys in client-side code | Keys stolen, quota exhausted, unauthorized charges | Store keys in Flask environment variables, never frontend |
| No input sanitization before sending to LLM | Prompt injection attacks, manipulated outputs | Sanitize/validate user text before sending to API |
| No rate limiting | DoS attacks, cost exhaustion, service disruption | Implement IP and user-based rate limiting with Flask-Limiter |
| CORS misconfiguration | Cross-origin attacks, data exposure | Use specific allowed origins, never wildcard `*` |
| No SSL/TLS in production | Credentials transmitted in plaintext | Always use HTTPS, configure Flask's `SESSION_COOKIE_SECURE` |
| Trusting X-Forwarded headers blindly | IP spoofing, security bypass | Configure ProxyFix with correct number of proxies |
| Not validating LLM responses | Malformed data, injection attacks | Validate response structure before rendering |
| Logging sensitive text | Privacy violations, data exposure | Hash or truncate sensitive text in logs, follow GDPR |

## UX Pitfalls

Common user experience mistakes in AI-powered text analysis.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No loading state during analysis | Users think it's broken, submit multiple times | Show spinner/progress immediately, disable button |
| Generic "error occurred" messages | Users don't know what to do next | Show specific, actionable error messages with retry options |
| Overwhelming results | Users can't find relevant information | Progressive disclosure: summary first, details on expand |
| No explanation of fallacies | Users don't learn or trust the tool | Always provide educational context for detected fallacies |
| Tarot theme overwhelms content | Aesthetic distracts from utility | Use theme as accent, ensure readability is primary |
| No feedback mechanism | Can't improve detection or UX | Add "Was this helpful?" feedback, report incorrect results |
| Mobile-unresponsive results | Poor experience on small screens | Design mobile-first, test on actual devices |
| Keyboard navigation not supported | Inaccessible to keyboard users | Ensure all interactive elements are keyboard-accessible |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **LLM Integration:** Often missing exponential backoff for rate limits — verify by reviewing error handling code
- [ ] **Cost Management:** Often missing API usage monitoring and alerts — verify by checking OpenAI dashboard integration
- [ ] **Error Handling:** Often missing user-friendly error messages for LLM failures — verify by testing with deliberate failures (e.g., invalid API key)
- [ ] **Performance:** Often missing async routes for long LLM calls — verify by checking Flask route definitions
- [ ] **Security:** Often missing rate limiting — verify by testing rapid successive submissions
- [ ] **Caching:** Often missing cache invalidation strategy — verify by checking if prompts can be updated without breaking cache
- [ ] **Accessibility:** Often missing keyboard navigation and screen reader support — verify by testing with NVDA/VoiceOver
- [ ] **Mobile:** Often missing actual device testing — verify by checking analytics for mobile device performance
- [ ] **Proxy Config:** Often missing ProxyFix middleware — verify by checking production deployment behind nginx/Apache
- [ ] **Testing:** Often missing integration tests with actual LLM responses — verify by checking test coverage of API routes

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| API keys exposed | HIGH | 1. Rotate API keys immediately in OpenAI dashboard<br>2. Audit usage logs for unauthorized access<br>3. Add environment variable checks to prevent future commits<br>4. Scan GitHub/GitLab for accidentally committed keys<br>5. Implement secret scanning in CI/CD |
| Rate limit exhaustion | MEDIUM | 1. Increase API quota temporarily<br>2. Implement aggressive rate limiting<br>3. Add caching to reduce API calls<br>4. Review logs for abuse patterns<br>5. Add quota alerts for early warning |
| Broken LLM responses | MEDIUM | 1. Switch to older stable model version<br>2. Add response validation to catch malformed data<br>3. Implement fallback to cached results<br>4. Monitor response quality in production<br>5. Roll back prompt changes |
| Poor UX feedback | LOW | 1. Add in-app feedback mechanism<br>2. Review user analytics and comments<br>3. A/B test different result presentations<br>4. Iterate based on user testing<br>5. Monitor engagement metrics |
| Performance degradation | MEDIUM | 1. Enable query/response logging<br>2. Profile Flask routes to find bottlenecks<br>3. Add async for long operations<br>4. Implement response caching<br>5. Scale horizontally if needed |
| Security breach | HIGH | 1. Rotate all secrets immediately<br>2. Audit access logs for intrusion<br>3. Patch vulnerabilities<br>4. Notify affected users (if PII involved)<br>5. Hire security audit if breach is serious |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Blocking LLM API calls on main thread | Phase 1 (MVP) | Test with slow API responses, verify UI remains responsive |
| Exposed API keys | Phase 1 (MVP) | Check browser DevTools for API keys, run secret scanner |
| Naive caching | Phase 2 (Optimization) | Test cache invalidation, monitor hit rate and staleness |
| Missing error handling | Phase 1 (MVP) | Intentionally trigger errors, verify user-friendly messages |
| Over-fetching results | Phase 1 (MVP) | Test with various text lengths, verify appropriate result density |
| No async LLM calls | Phase 1 (MVP) | Load test with concurrent users, verify no request queuing |
| Missing rate limiting | Phase 1 (MVP) | Simulate rapid requests, verify rate limiting kicks in |
| Poor mobile experience | Phase 1 (MVP) | Test on actual mobile devices, verify responsive design |
| No caching strategy | Phase 2 (Optimization) | Monitor API usage, verify caching reduces calls |
| Accessibility issues | Phase 1 (MVP) | Run Lighthouse accessibility audit, test with screen readers |
| Proxy configuration issues | Phase 3 (Production Hardening) | Deploy behind reverse proxy, verify correct client IPs in logs |
| Security vulnerabilities | Phase 1 (MVP) | Run security audit tools (OWASP ZAP, Bandit) |
| Performance regressions | Phase 2 (Optimization) | Set up Lighthouse CI, track performance metrics |
| Poor UX for results | Phase 1 (MVP), Phase 2 (UX Refinement) | User testing, analytics monitoring, feedback collection |
| Cost overruns | Phase 1 (MVP) | Set up cost alerts, monitor OpenAI dashboard weekly |

## Sources

- **Flask Official Documentation:** https://flask.palletsprojects.com/en/latest/deploying/ (HIGH confidence - official docs explicitly warn against dev server in production)
- **Flask ProxyFix:** https://flask.palletsprojects.com/en/latest/deploying/proxy_fix/ (HIGH confidence - official docs on security issues)
- **React Official Docs:** https://react.dev/learn/render-and-commit (HIGH confidence - official React documentation)
- **React Performance:** https://react.dev/learn/ (HIGH confidence - official React guidance)
- **web.dev Performance:** https://web.dev/articles/optimize-long-tasks (HIGH confidence - authoritative source on web performance)
- **web.dev Third-Party JS:** https://web.dev/articles/third-party-javascript (HIGH confidence - official web.dev guidance)
- **Sentry Flask Integration:** https://docs.sentry.io/platforms/python/integrations/flask/ (HIGH confidence - official Sentry docs)
- **Common LLM API Patterns:** Based on production experience with OpenAI API and community best practices (MEDIUM confidence - inferred from documentation and common patterns)
- **Prompt Injection Attacks:** Based on OWASP and security community discussions about AI applications (MEDIUM confidence - widely documented security concern)
- **Cost Management:** Based on OpenAI pricing documentation and production experience (HIGH confidence - documented pricing and quota limits)

---

*Last updated: 2026-03-14*
*Domain: AI-Powered Text Analysis (Logical Fallacy Detection)*
