---
phase: 01-automation-foundation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [.github/workflows/fallacy_automation.yml, scripts/main.py]
autonomous: true
requirements: [GHA-01, GHA-02, GHA-06, GHA-07, SEC-05]

must_haves:
  truths:
    - "GitHub Actions workflow runs automatically every 6 hours on cron schedule"
    - "Workflow concurrency group prevents parallel runs from conflicting"
    - "Aggressive timeouts (10s Reddit, 30s LLM, 90s image) prevent 6-hour GitHub Actions limit"
    - "Git operations handle conflicts with conflict resolution logic"
    - "HF_TOKEN is securely accessed from GitHub Secrets, never committed to repo"
  artifacts:
    - path: ".github/workflows/fallacy_automation.yml"
      provides: "Complete GitHub Actions automation workflow"
      contains: "concurrency:", "timeout:", "HF_TOKEN", "conflict resolution"
    - path: "scripts/main.py"
      provides: "Main orchestration script with error handling and logging"
      exports: ["main()"]
  key_links:
    - from: ".github/workflows/fallacy_automation.yml"
      to: "scripts/main.py"
      via: "python main.py command"
      pattern: "python.*main.py"
---

<objective>
Enhance GitHub Actions workflow with production-grade reliability features: concurrency control, aggressive timeouts, conflict resolution, and secure secrets management.

Purpose: Prevent workflow failures from concurrent runs, 6-hour timeout, and git conflicts. Ensure zero-cost operation with secure token handling.
Output: Robust GitHub Actions workflow that runs reliably every 6 hours.
</objective>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
@/Users/volkanakkaya/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/research/SUMMARY.md

# Existing code context
@.github/workflows/fallacy_automation.yml
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add workflow concurrency and timeout handling</name>
  <files>.github/workflows/fallacy_automation.yml</files>
  <action>
Modify the existing .github/workflows/fallacy_automation.yml file to add:

1. **Concurrency group** to prevent parallel runs:
   ```yaml
   concurrency:
     group: fallacy-automation-${{ github.ref }}
     cancel-in-progress: true
   ```

2. **Aggressive per-operation timeouts** (under fetch-and-analyze job):
   ```yaml
   timeout-minutes: 90
   steps:
     # ... existing steps ...
     - name: Fetch Reddit Data
       timeout-minutes: 2
       run: |
         # ... existing wget commands with --timeout=10 ...
   
     - name: Run Fallacy Analysis & Generation
       timeout-minutes: 5
       env:
         HF_TOKEN: ${{ secrets.HF_TOKEN }}
       run: python scripts/main.py
   
     - name: Commit and Push Results
       timeout-minutes: 10
       # ... existing commit/push ...
   ```

3. **Secure HF_TOKEN access** (already present, verify it's correct):
   ```yaml
   - name: Run Fallacy Analysis & Generation
     env:
       HF_TOKEN: ${{ secrets.HF_TOKEN }}
   ```

Keep the existing cron schedule ('0 */6 * * *') and workflow_dispatch triggers.
  </action>
  <verify>
grep -q "concurrency:" .github/workflows/fallacy_automation.yml && grep -q "timeout-minutes: 90" .github/workflows/fallacy_automation.yml && grep -q "HF_TOKEN: \${{ secrets.HF_TOKEN }}" .github/workflows/fallacy_automation.yml
  </verify>
  <done>Workflow has concurrency control, 90-minute overall timeout, per-step timeouts, and secure HF_TOKEN access</done>
</task>

<task type="auto">
  <name>Task 2: Add git conflict resolution and main orchestration script</name>
  <files>.github/workflows/fallacy_automation.yml, scripts/main.py</files>
  <action>
**Part A: Update workflow commit step with conflict resolution**

Modify the "Commit and Push Results" step in .github/workflows/fallacy_automation.yml:
```yaml
- name: Commit and Push Results
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add data/ docs/data/ output_images/ generated_cards/ || true

    # Conflict resolution: pull first, then commit
    if git diff --staged --quiet; then
      echo "No changes to commit"
    else
      git pull --rebase origin main || git pull --strategy-option=theirs origin main
      git commit -m "Auto-update: New fallacy cards generated [skip ci]"
      git push origin main
    fi
```

**Part B: Create main orchestration script**

Create scripts/main.py:
```python
#!/usr/bin/env python3
"""
Main orchestration script for Fallacy Tarot automation.
Coordinates Reddit scraping, LLM analysis, and data persistence.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import client modules (these will be created in subsequent plans)
try:
    from reddit_client import fetch_reddit_posts
    from hf_client import analyze_fallacy
    from data_manager import DataManager
except ImportError as e:
    logger.error(f"Failed to import client modules: {e}")
    logger.info("Client modules will be created in subsequent plans")
    sys.exit(0)

def main():
    """Main orchestration function"""
    logger.info("=" * 60)
    logger.info("🔮 Fallacy Tarot Automation Started")
    logger.info("=" * 60)

    try:
        # Step 1: Fetch Reddit posts
        logger.info("Step 1: Fetching Reddit posts...")
        posts = fetch_reddit_posts(limit=10)
        logger.info(f"Fetched {len(posts)} posts")

        if not posts:
            logger.warning("No posts fetched, exiting gracefully")
            return

        # Step 2: Analyze posts for fallacies
        logger.info("Step 2: Analyzing posts for fallacies...")
        analyzed_posts = []

        for i, post in enumerate(posts, 1):
            logger.info(f"Analyzing post {i}/{len(posts)}: {post['id']}")
            try:
                analysis = analyze_fallacy(post['content'])

                if analysis and analysis.get('has_fallacy'):
                    post['analysis'] = analysis
                    analyzed_posts.append(post)
                    logger.info(f"  → Detected: {analysis['fallacy_type']} (confidence: {analysis['confidence']:.2f})")
                else:
                    logger.info(f"  → No fallacy detected")

            except Exception as e:
                logger.error(f"Error analyzing post {post['id']}: {e}")
                # Continue with next post (graceful degradation)
                continue

        logger.info(f"Analysis complete: {len(analyzed_posts)}/{len(posts)} posts have fallacies")

        if not analyzed_posts:
            logger.info("No fallacies detected in this batch")
            return

        # Step 3: Save data
        logger.info("Step 3: Saving analyzed data...")
        data_manager = DataManager()
        data_manager.add_entries(analyzed_posts)
        logger.info("Data saved successfully")

        logger.info("=" * 60)
        logger.info("✅ Automation completed successfully")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error in automation: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

This creates a scaffold that will be populated by subsequent plans (reddit_client, hf_client, data_manager).
  </action>
  <verify>
test -f scripts/main.py && grep -q "git pull --rebase" .github/workflows/fallacy_automation.yml && python3 -m py_compile scripts/main.py
  </verify>
  <done>Git conflict resolution implemented in workflow, main orchestration script created with logging</done>
</task>

</tasks>

<verification>
Verify workflow has all reliability features:
- [ ] Concurrency group defined to prevent parallel runs
- [ ] 90-minute overall timeout set on job
- [ ] Per-step timeouts (2min for Reddit, 5min for analysis)
- [ ] HF_TOKEN accessed from GitHub Secrets
- [ ] Git conflict resolution with pull-then-commit
- [ ] main.py orchestration script with logging created

Run workflow validation (dry run):
```bash
# Validate YAML syntax
cat .github/workflows/fallacy_automation.yml | python3 -c "import yaml,sys; yaml.safe_load(sys.stdin)"
```
</verification>

<success_criteria>
GitHub Actions workflow is production-ready with:
- Automatic scheduling every 6 hours (cron: '0 */6 * * *')
- Concurrency control preventing parallel runs
- Aggressive timeouts preventing 6-hour limit
- Secure token management (HF_TOKEN from secrets)
- Git conflict resolution handling
- Main orchestration script with logging framework
</success_criteria>

<output>
After completion, create `.planning/phases/01-automation-foundation/01-automation-foundation-01-SUMMARY.md`
</output>
