---
phase: 02-visual-generation-frontend
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [scripts/image_generator.py, .github/workflows/fallacy_automation.yml, scripts/main.py]
autonomous: true
requirements: [IMG-01, IMG-02, IMG-03, IMG-06, GHA-05]

must_haves:
  truths:
    - "Stable Diffusion XL generates unique tarot card images for each detected fallacy type"
    - "Image generation prompts are optimized for mystical tarot style (blues, purples, gold accents)"
    - "Retry logic with exponential backoff handles image generation failures"
    - "Images are stored in docs/assets/ directory with specific naming convention"
    - "SD_TOKEN secret securely accessed in workflow for Stable Diffusion API"
  artifacts:
    - path: "scripts/image_generator.py"
      provides: "Script to call Hugging Face SDXL API and save images"
    - path: ".github/workflows/fallacy_automation.yml"
      provides: "Updated workflow to pass SD_TOKEN"
---

<objective>
Implement the Stable Diffusion XL image generation script to create mystical tarot cards for detected fallacies and integrate it into the automation pipeline.

Purpose: Automate the visual generation of tarot cards for each fallacy type using the Hugging Face Inference API.
Output: An `image_generator.py` script that reads `fallacies.json`, generates missing images, saves them to `docs/assets/`, and an updated GitHub Actions workflow.
</objective>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/phases/02-visual-generation-frontend/02-CONTEXT.md
</context>
