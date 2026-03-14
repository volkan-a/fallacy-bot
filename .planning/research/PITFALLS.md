# Domain Pitfalls

**Domain:** Automated Reddit scraping with AI image generation
**Researched:** 2026-03-14
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Reddit API Rate Limit Exceeded

**What goes wrong:**
Automated Reddit scraping bots hit API rate limits (typically 30 requests per minute for unauthenticated, ~60/minute for OAuth), causing all subsequent requests to fail. The workflow runs but produces no new data, and the website shows stale content.

**Why it happens:**
Developers implement scraping without implementing proper rate limiting, backoff strategies, or respecting the `Retry-After` header. The 6-hour schedule doesn't prevent bursts of requests during execution, and the current workflow's `wget` approach doesn't implement any throttling.

**How to avoid:**
- Implement exponential backoff with jitter for failed requests
- Add delays between subreddit fetches (current workflow has 2-second sleep, which is good)
- Cache responses locally to avoid repeated identical requests
- Use OAuth authentication for higher rate limits (60 requests/minute vs 30 unauthenticated)
- Monitor remaining rate limit quota via `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers
- Never exceed 30 requests/minute for unauthenticated access, 60/minute for authenticated

**Warning signs:**
- HTTP 429 (Too Many Requests) errors in workflow logs
- Workflow completes but `docs/data/archive.json` has no new entries
- GitHub Actions runs consistently fail at the "Fetch Reddit Data" step
- Reddit API returns empty data arrays despite recent subreddit activity

**Phase to address:**
Phase 1 (Reddit Integration) - This is foundational; without reliable data access, nothing else works.

---

### Pitfall 2: Hugging Face Free Tier Quota Exhaustion

**What goes wrong:**
Hugging Face free tier (Inference API) has unspecified but enforced limits. When quotas are exceeded, API calls fail with 429 or 503 errors, breaking fallacy detection and image generation. Free tier may also experience throttling during high-demand periods.

**Why it happens:**
Developers assume "free" means "unlimited" and don't implement fallback strategies. The workflow calls the API multiple times per execution (once per Reddit post for analysis, plus image generation), and running every 6 hours means ~120 API calls/day without error handling. Hugging Face may enforce monthly request limits or concurrent request limits that aren't documented.

**How to avoid:**
- Implement graceful degradation: when HF API fails, continue with existing data or skip that iteration
- Add retry logic with exponential backoff (3-5 retries max)
- Cache analysis results locally to avoid re-analyzing same content
- Monitor API response headers for rate limit information
- Have a fallback mechanism: use a smaller/faster model or skip AI features temporarily
- Consider self-hosting models if free tier proves unreliable
- Track API usage metrics in workflow logs to detect limits being approached

**Warning signs:**
- HTTP 429 (Too Many Requests) from Hugging Face endpoints
- HTTP 503 (Service Unavailable) during high-demand periods
- Workflow succeeds but generates no new cards
- Increased response times from Hugging Face API (throttling indicator)
- Analysis step fails consistently but image generation still works (or vice versa)

**Phase to address:**
Phase 1 (AI Integration) - Core functionality depends entirely on HF APIs; failure means no fallacy detection.

---

### Pitfall 3: GitHub Actions 6-Hour Job Timeout

**What goes wrong:**
GitHub Actions jobs have a 6-hour execution limit on standard runners. If Reddit scraping, LLM analysis, and image generation collectively take too long, the workflow times out mid-execution. This can result in partial data writes, corrupted JSON files, or broken git state.

**Why it happens:**
Developers underestimate the cumulative time of:
- Reddit API fetching (with rate limiting delays)
- Hugging Face API calls (with retries and potential timeouts)
- Stable Diffusion image generation (can take 30-90 seconds per image)
- Git operations (clone, add, commit, push)

A single iteration might take 2-3 minutes; processing multiple posts could exceed 6 hours. The current workflow processes up to 20 posts sequentially without time budgeting.

**How to avoid:**
- Set aggressive timeouts for each external API call (Reddit: 10s, HF LLM: 30s, HF Image: 90s)
- Process fewer posts per run (current fetches 20, recommend 5-10 max)
- Implement parallel processing where possible (analyze multiple posts concurrently)
- Add checkpointing: save progress incrementally so partial failures don't waste work
- Skip posts that exceed time thresholds (fail-fast on slow operations)
- Monitor total execution time and abort remaining work if approaching 6-hour limit

**Warning signs:**
- GitHub Actions workflow runs show duration approaching 4-5 hours regularly
- Workflow logs show "Error: Process completed with exit code 143" (timeout signal)
- Partially written JSON files (e.g., incomplete entries array)
- Git push fails because no files changed (work timed out before commit)

**Phase to address:**
Phase 1 (Automation Foundation) - Timeout constraints affect all subsequent phases; must design for this from start.

---

### Pitfall 4: JSON File Corruption During Concurrent Writes

**What goes wrong:**
Multiple GitHub Actions workflow runs could execute simultaneously (e.g., if a previous run is slow and a new one triggers), leading to race conditions on `docs/data/archive.json`. One workflow reads the file, another modifies it, then the first writes stale data. Result: lost entries, corrupted JSON syntax, or broken website.

**Why it happens:**
JSON files don't support atomic writes or transactions. The pattern `read -> modify -> write` is not safe with concurrent processes. GitHub Actions has a 6-hour timeout but doesn't prevent concurrent executions, and the cron schedule (every 6 hours) doesn't guarantee sequential runs if a previous run is delayed.

**How to avoid:**
- Implement file locking: create a `.lock` file before writing, abort if lock exists
- Use atomic writes: write to a temp file, then `os.replace()` (atomic on POSIX)
- Add workflow concurrency limits in GitHub Actions YAML (`concurrency:` key)
- Validate JSON syntax before committing (fail fast on corruption)
- Maintain a backup of the last good state (e.g., `archive.json.backup`)
- Consider migrating to a proper database if corruption becomes frequent

**Warning signs:**
- Workflow runs complete but `docs/data/archive.json` has syntax errors
- Website shows fewer entries than expected (lost data)
- Git history shows "reverting" commits (overwrites from stale data)
- GitHub Actions logs show JSON parsing errors during read operations

**Phase to address:**
Phase 1 (Data Persistence) - Data integrity is foundational; corruption breaks everything downstream.

---

### Pitfall 5: Stable Diffusion Image Generation Failures

**What goes wrong:**
Stable Diffusion XL on Hugging Face free tier can fail due to:
- GPU resource contention (free tier uses shared GPUs)
- Model loading timeouts
- Prompt complexity causing excessive generation time
- API returning 503 or 500 errors
- Generated images are corrupted, blank, or don't match prompt

Without fallbacks, failed generation results in broken image paths on the website.

**Why it happens:**
The workflow assumes image generation always succeeds and writes the image path directly to JSON. If generation fails, the path points to a non-existent file, causing broken images on the website. Free tier GPUs are oversubscribed, and complex prompts (the current prompt is quite detailed) can exceed generation timeouts.

**How to avoid:**
- Implement fallback: use a pre-generated placeholder card when generation fails
- Validate generated image (check file size > 0 bytes, valid PNG signature)
- Simplify prompts (reduce token count, avoid excessive detail)
- Set aggressive timeouts for generation (60-90 seconds max)
- Retry failed generations once with a simplified prompt
- Log generation failures but don't abort the entire workflow
- Maintain a library of pre-generated tarot cards as backup

**Warning signs:**
- Workflow logs show "Image generation error" exceptions
- `assets/` directory contains 0-byte or invalid PNG files
- Website displays broken image icons instead of tarot cards
- Image generation step consistently times out or fails

**Phase to address:**
Phase 2 (Visual Generation) - Core differentiator; broken images undermine the entire "tarot card" concept.

---

### Pitfall 6: Git Push Conflicts from Concurrent Runs

**What goes wrong:**
Two GitHub Actions workflows running simultaneously both attempt to push to the same branch. The second push fails with "remote contains work that you do not have" errors, preventing deployment of updated data. Workflow completes successfully from a script perspective but doesn't update the website.

**Why it happens:**
Git doesn't handle concurrent pushes to the same branch gracefully. When multiple workflows try to push, the second workflow's local state is stale. The workflow uses standard `git push` without `--force` or conflict resolution logic.

**How to avoid:**
- Add `concurrency:` group in GitHub Actions YAML to prevent overlapping runs
- Implement a pull/merge before push: `git pull --rebase` to integrate remote changes
- Use `git push --force-with-lease` (safer than `--force`) for automated pushes
- Detect conflicts early: `git fetch && git diff HEAD @{u}` before attempting push
- Add workflow-level mutex: check for running workflows before starting work
- Consider using a separate deployment branch to avoid conflicts

**Warning signs:**
- GitHub Actions logs show "failed to push some refs" errors
- Workflow completes but `git status` shows unpushed commits
- Website doesn't update despite successful workflow runs
- Git history shows multiple attempts to push the same changes

**Phase to address:**
Phase 1 (Automation Foundation) - Affects all phases; prevents reliable data updates.

---

### Pitfall 7: GitHub Pages Deployment Lag

**What goes wrong:**
After GitHub Actions commits and pushes changes, GitHub Pages doesn't immediately rebuild the website. Updates can take 1-5 minutes, during which visitors see stale content or broken image references. If the workflow assumes immediate availability, monitoring scripts or automated checks may fail.

**Why it happens:**
GitHub Pages has a build queue and isn't instant. The workflow commits and exits, but Pages builds asynchronously. The website's HTML may reference new images that haven't been deployed yet, causing temporary broken states.

**How to avoid:**
- Don't assume immediate availability after push; add a wait/check mechanism if needed
- Use a dedicated monitoring workflow that checks site health after deployment
- Document the expected lag for stakeholders (1-5 minutes typical)
- Consider using a preview deployment for testing before publishing
- Monitor GitHub Pages deployment status via GitHub API if real-time checks are needed

**Warning signs:**
- Workflow succeeds but website shows old content immediately after
- Image references broken for 1-5 minutes after workflow completion
- Automated site health checks fail immediately after successful workflow runs
- GitHub Pages build queue shows pending builds

**Phase to address:**
Phase 1 (Deployment Setup) - Affects all monitoring and validation; manage expectations.

---

### Pitfall 8: Hugging Face Token Exposure in Logs

**What goes wrong:**
The Hugging Face API token is passed as an environment variable (`HF_TOKEN`), and if the Python script logs errors or debug information, the token could be exposed in GitHub Actions logs. This is a security vulnerability: anyone with access to the repository logs can steal the token.

**Why it happens:**
Python's default exception handling includes the full environment context. If an error occurs in the `analyze_fallacy` or `generate_tarot_card` functions, the exception traceback might include environment variables. GitHub Actions logs are retained and accessible to anyone with repository access.

**How to avoid:**
- Never log environment variables directly; use filtered logging
- Set `ACTIONS_STEP_DEBUG` to false (default) and avoid `ACTIONS_RUNNER_DEBUG`
- Add workflow-level secret masking (GitHub masks secrets automatically in logs, but validate)
- Use `.env` files with restricted permissions, don't hardcode tokens
- Rotate tokens if accidental exposure is suspected
- Audit workflow logs periodically for leaked credentials

**Warning signs:**
- GitHub Actions logs show `HF_TOKEN=...` in output
- Workflow logs contain full environment variable dumps
- Unexpected API usage on Hugging Face account (token theft indicator)
- Secrets scanner warnings in GitHub repository

**Phase to address:**
Phase 1 (Security Foundation) - Security is foundational; token exposure compromises the entire project.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcoded subreddit list in workflow | Quick setup, no configuration needed | Hard to add new subreddits, requires workflow file change | Never - extract to config file |
| No retry logic for API calls | Simpler code, fewer lines | Fragile automation, breaks on transient failures | Never - retries are essential |
| Using `wget` instead of proper Reddit API wrapper | No dependencies, built-in tool | Limited error handling, can't auth for higher rate limits | Phase 1 only - replace with PRAW later |
| Storing votes in localStorage | No backend needed, simple implementation | Not persistent across devices, vulnerable to spam | Phase 1-2 only - migrate to backend for Phase 3+ |
| Linear processing of posts (no parallelization) | Simple control flow | Slow execution, wastes job time, may hit timeout | Phase 1 only - optimize in Phase 2 |
| No monitoring/alerting for failed workflows | Less noise in inbox | Silent failures, stale data undetected for days | Never - essential for automation reliability |
| Committing generated images directly to git | Simple deployment, no external storage needed | Repository bloat, slower clones, can't purge old assets | Phase 1 only - migrate to S3/CDN for Phase 2+ |

---

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| **Reddit API** | Using unauthenticated requests for high-volume scraping | Implement OAuth with token rotation for higher rate limits (60 vs 30 req/min) |
| **Reddit API** | Not respecting `Retry-After` header on 429 responses | Parse `Retry-After` header and wait exactly that duration |
| **Reddit API** | Fetching from `/new` instead of `/hot` or `/top` | Use `/top?t=week` for quality content; `/hot` is volatile |
| **Hugging Face LLM** | Not setting `max_tokens` parameter | Always set `max_tokens` (500-1000) to prevent runaway costs |
| **Hugging Face LLM** | Using `temperature=0` (deterministic) | Use `temperature=0.3-0.7` for varied, more natural outputs |
| **Hugging Face Image** | Not validating image format before saving | Check content-type header and file size before writing to disk |
| **GitHub Actions** | Not using `continue-on-error` for non-critical steps | Mark image generation as `continue-on-error: true` to prevent total failures |
| **GitHub Actions** | Committing everything including dependencies | Add `.gitignore` patterns for `__pycache__`, `*.pyc`, `.DS_Store` |
| **GitHub Pages** | Not specifying exact build directory | Configure `docs/` as the source directory in repository settings |
| **Git Push** | Using `git push --force` blindly | Use `git push --force-with-lease` for safety, or implement conflict resolution |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|------------------|
| **Fetching all subreddits sequentially** | Workflow takes >10 minutes for Reddit step | Fetch subreddits in parallel (async/await or concurrent threads) | 10+ subreddits |
| **Processing 20+ posts per run** | Job timeout after 5-6 hours | Limit to 5-10 posts, prioritize by score/recency | 15+ posts with LLM + image gen |
| **Storing all generated images in git** | Repository size >100MB, slow clones | Migrate images to S3/Git LFS, serve via CDN | 50+ images @ 2MB each |
| **No caching of LLM responses** | Same post analyzed multiple times | Cache analysis results by content hash, reuse for duplicates | 7+ days of history with similar content |
| **Linear processing without early exit** | Workflow continues after first success | Process posts in priority order, stop after N successful cards | 3+ successful generations per run unnecessary |
| **No pagination in HTML generation** | Page becomes slow with 100+ cards | Implement pagination (10 cards per page, lazy loading) | 50+ entries in archive |
| **Synchronous image generation** | Each image blocks workflow for 60-90s | Generate images in parallel, then collect results | 3+ images per run |

---

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Hardcoding `HF_TOKEN` in workflow YAML | Token exposed in git history, accessible to all repo users | Always use `${{ secrets.HF_TOKEN }}`, never commit secrets |
| Logging full error messages with environment context | Accidental token or credential exposure in logs | Sanitize logs before output, mask secrets via GitHub Actions |
| No secret rotation plan | Long-lived tokens increase compromise impact | Rotate tokens quarterly, have revocation procedure ready |
| Trusting user input in prompts | Prompt injection attacks, unexpected LLM behavior | Sanitize Reddit content before passing to LLM |
| No rate limiting on public endpoints | Abuse by bots, quota exhaustion | Implement IP-based or token-based rate limiting (if building API) |
| Not validating image formats | Malicious file uploads, XSS via image metadata | Validate PNG/JPEG headers, strip metadata |
| Exposing `archive.json` with sensitive data | PII from Reddit (usernames, emails) exposed | Scrub PII before storage, consider minimal data retention |
| No authentication on voting endpoints | Bot manipulation of voting system | Add CAPTCHA or rate limiting (Phase 3+ when backend is added) |

---

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Loading all tarot cards at once | Slow page load, high bandwidth usage | Lazy load images, show placeholder until in viewport |
| No loading indicators during image generation | Users think site is broken | Show loading spinners/skeletons while waiting for content |
| Sorting buttons (Hot/Best/Newest) don't work | Confusing UI, broken expectations | Implement actual sorting logic or hide non-functional buttons |
| No fallback for missing images | Broken image icons, unprofessional look | Always show placeholder card with "Image unavailable" message |
| Infinite scroll without pagination | Browser performance issues with 100+ cards | Load 10 at a time, show "Load more" button |
| No indication of content age | Users think content is outdated | Show "Last updated: X hours ago" badge |
| Voting buttons don't persist | Votes lost on refresh, frustrating UX | Persist votes to localStorage with expiration, or migrate to backend in Phase 3 |
| No responsive design on mobile | 50%+ of users can't use the site | Test on mobile, implement responsive breakpoints |
| No error recovery for failed API calls | Silent failures, users don't know what's happening | Show error messages with retry buttons, fallback content |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Reddit Integration:** Often missing **rate limiting** — verify `Retry-After` header handling, delays between requests
- [ ] **Hugging Face API:** Often missing **fallback logic** — verify graceful degradation when API fails
- [ ] **Image Generation:** Often missing **placeholder cards** — verify default tarot card exists and is used on failures
- [ ] **JSON Storage:** Often missing **atomic writes** — verify temp file + rename pattern, file locking
- [ ] **GitHub Actions:** Often missing **concurrency control** — verify only one workflow runs at a time
- [ ] **Git Operations:** Often missing **conflict resolution** — verify `git pull --rebase` before push
- [ ] **Error Handling:** Often missing **logging** — verify all exceptions are caught and logged with context
- [ ] **Monitoring:** Often missing **alerts** — verify failed workflows send notifications
- [ ] **Deployment:** Often missing **validation** — verify JSON syntax before committing
- [ ] **Voting System:** Often missing **persistence** — verify votes survive browser refresh (localStorage)
- [ ] **Pagination:** Often missing **for 50+ entries** — verify HTML loads efficiently with many cards
- [ ] **Mobile Responsiveness:** Often missing **media queries** — verify site works on phones/tablets

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| **Rate limit exceeded (Reddit)** | LOW | Wait until rate limit resets (check `X-RateLimit-Reset` header), resume workflow |
| **Rate limit exceeded (Hugging Face)** | LOW | Wait 1-5 minutes, retry with exponential backoff, skip failing post |
| **GitHub Actions timeout** | MEDIUM | Check workflow logs for last successful step, resume from checkpoint or skip remaining work |
| **JSON file corruption** | HIGH | Restore from `.backup` file, validate git history for last good commit, manual reconstruction if needed |
| **Concurrent git push conflict** | LOW | `git pull --rebase` to integrate remote changes, retry push, or abort if conflicts unresolvable |
| **Stable Diffusion failure** | LOW | Use placeholder card, log failure, continue workflow (don't abort) |
| **Hugging Face token exposed** | HIGH | Revoke token immediately, generate new token, audit workflow logs for usage, rotate all secrets |
| **Git history corrupted (force push)** | HIGH | Use `git reflog` to find lost commits, force push from earlier point, or reconstruct from backup |
| **GitHub Pages build stuck** | MEDIUM | Contact GitHub Support, trigger manual build via API, or commit a dummy change to force rebuild |
| **Disk space full (too many images)** | MEDIUM | Delete old images (keep last 50), migrate to external storage, compress existing images |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Reddit API rate limiting | Phase 1 (Reddit Integration) | Monitor logs for 429 errors, verify backoff in code |
| Hugging Face quota exhaustion | Phase 1 (AI Integration) | Check workflow logs for retries, verify fallback behavior |
| GitHub Actions timeout | Phase 1 (Automation Foundation) | Run full workflow, measure execution time, verify <5 hours |
| JSON file corruption | Phase 1 (Data Persistence) | Test concurrent workflow runs, verify JSON validity |
| Stable Diffusion failures | Phase 2 (Visual Generation) | Intentionally break HF API, verify placeholder used |
| Git push conflicts | Phase 1 (Automation Foundation) | Trigger two workflows simultaneously, verify no conflicts |
| GitHub Pages deployment lag | Phase 1 (Deployment Setup) | Commit change, measure time to live site (should be <5 min) |
| Hugging Face token exposure | Phase 1 (Security Foundation) | Scan workflow logs for token patterns, verify masking |
| GitHub Actions concurrency | Phase 1 (Automation Foundation) | Add `concurrency:` group to YAML, test simultaneous triggers |
| Image generation timeouts | Phase 2 (Visual Generation) | Set aggressive timeout, verify workflow doesn't hang |
| Voting system spam | Phase 3 (Backend - Optional) | Add rate limiting, CAPTCHA (deferred from Phase 1-2) |
| Repository bloat (images) | Phase 2 (Infrastructure) | Measure repo size after 50 images, plan migration to S3 |

---

## Sources

- **Reddit API**: Official documentation (https://www.reddit.com/dev/api/) - Rate limits documented
- **GitHub Actions Limits**: Official documentation (https://docs.github.com/en/actions/reference/actions-limits) - 6-hour job timeout, concurrency limits verified
- **GitHub Actions Usage**: Official documentation (https://docs.github.com/en/actions/usage-limits-billing-and-administration) - Free tier quotas confirmed
- **GitHub Actions Caching**: Official documentation (https://docs.github.com/en/actions/using-workflows/caching-dependencies) - Cache limits (10GB free, eviction policy)
- **GitHub Actions Security**: Official documentation (https://docs.github.com/en/actions/security-guides/automatic-token-authentication) - GITHUB_TOKEN permissions, secret handling
- **Hugging Face Inference**: Official documentation (https://huggingface.co/docs/api-inference/index) - Provider selection, error handling
- **Hugging Face Spaces**: Official documentation (https://huggingface.co/docs/hub/spaces-overview) - Hardware specs, pricing (free tier limits)
- **GitHub Pages**: Official documentation (https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages) - Static hosting constraints
- **Project Context**: Review of existing `.github/workflows/fallacy_automation.yml` and `scripts/fallacy_analyzer.py` - Identified current anti-patterns

---

*Pitfalls research for: Automated Reddit scraping with AI image generation*
*Researched: 2026-03-14*
*Confidence: HIGH (all findings verified against official documentation)*
