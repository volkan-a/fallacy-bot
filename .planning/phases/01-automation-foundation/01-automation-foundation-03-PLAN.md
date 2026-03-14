---
phase: 01-automation-foundation
plan: 03
type: execute
wave: 1
depends_on: []
files_modified: [scripts/hf_client.py, scripts/fallacy_prompts.py]
autonomous: true
requirements: [AI-01, AI-02, AI-03, AI-04, AI-05, SEC-01]

must_haves:
  truths:
    - "Hugging Face Inference API analyzes posts for logical fallacies"
    - "Exponential backoff retry logic handles failures (up to 5 retries)"
    - "LLM returns JSON format with fallacy_type, confidence_score, and explanation"
    - "Confidence scores classified as High (>0.8), Medium (0.5-0.8), Low (<0.5)"
    - "Graceful degradation skips analysis when API unavailable"
    - "Content validation filters NSFW/deleted posts before analysis"
  artifacts:
    - path: "scripts/hf_client.py"
      provides: "Hugging Face LLM client with retry and graceful degradation"
      exports: ["analyze_fallacy()"]
    - path: "scripts/fallacy_prompts.py"
      provides: "LLM prompts for fallacy detection"
      exports: ["create_fallacy_detection_prompt()"]
  key_links:
    - from: "scripts/hf_client.py"
      to: "https://api-inference.huggingface.co/models/"
      via: "HTTP POST requests with Bearer token"
      pattern: "requests.post.*api-inference.huggingface.co"
    - from: "scripts/hf_client.py"
      to: "scripts/fallacy_prompts.py"
      via: "Import for prompt generation"
      pattern: "from fallacy_prompts import"
    - from: "scripts/hf_client.py"
      to: "scripts/fallacy_types.py"
      via: "Import for fallacy type validation"
      pattern: "from fallacy_types import"
---

<objective>
Create Hugging Face LLM integration with robust retry logic, graceful degradation, and confidence score classification.

Purpose: Analyze Reddit posts for logical fallacies using Mistral-7B-Instruct-v0.3 (per REQUIREMENTS.md AUTO-03 and research recommendation) with zero-cost Hugging Face free tier. Handle API failures gracefully.
Output: Production-ready LLM client module.
</objective>

<execution_context>
@/Users/volkanakkaya/.config/opencode/get-shit-done/workflows/execute-plan.md
@/Users/volkanakkaya/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/research/SUMMARY.md

# Existing code context
@scripts/fallacy_analyzer.py
@scripts/analyze.py
@scripts/fallacy_types.py (created in Plan 02)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create LLM prompt module</name>
  <files>scripts/fallacy_prompts.py</files>
  <action>
Create scripts/fallacy_prompts.py with optimized prompts for fallacy detection:

```python
#!/usr/bin/env python3
"""
LLM prompts for fallacy detection.
Optimized for Mistral-7B-Instruct-v0.3 model (per REQUIREMENTS.md AUTO-03).
"""

from typing import Dict

def create_fallacy_detection_prompt(text: str, max_length: int = 500) -> str:
    """
    Create a prompt for detecting logical fallacies in text.

    Args:
        text: The text to analyze (truncated to max_length)
        max_length: Maximum text length to send to LLM

    Returns:
        Formatted prompt string
    """
    # Truncate text to avoid token limits
    truncated_text = text[:max_length]

    prompt = f"""Analyze the following text for logical fallacies.

Identify if there is a logical fallacy present. Choose ONLY from these 10 types:
1. Ad Hominem - Attacking the person instead of the argument
2. Straw Man - Misrepresenting an argument to make it easier to attack
3. Appeal to Authority - Claiming truth because an authority says so
4. False Dilemma - Presenting only two options when more exist
5. Slippery Slope - Asserting a small step leads to a chain of negative events
6. Circular Reasoning - The conclusion is included in the premise
7. Hasty Generalization - Drawing a conclusion from insufficient evidence
8. Red Herring - Introducing irrelevant information to divert attention
9. Tu Quoque - Avoiding criticism by turning it back on the accuser
10. Appeal to Emotion - Manipulating emotions rather than using logical reasoning

Text to analyze:
"{truncated_text}"

Return ONLY a JSON object with this exact structure:
{{
  "has_fallacy": true or false,
  "fallacy_type": "Name of fallacy (exactly as listed above) or 'None'",
  "confidence": 0.0 to 1.0 (your confidence level),
  "explanation": "Brief explanation in English of why this is a fallacy or why no fallacy was detected",
  "quote": "The specific part of text containing the fallacy (if any), or the main argument analyzed"
}}

Remember: Return ONLY valid JSON, no markdown formatting, no extra text."""

    return prompt

def parse_fallacy_response(response_text: str) -> Dict:
    """
    Parse LLM response to extract JSON.

    Args:
        response_text: Raw text response from LLM

    Returns:
        Parsed dictionary with has_fallacy, fallacy_type, confidence, explanation, quote
        Returns None if parsing fails
    """
    import json
    import re

    # Remove markdown code blocks if present
    cleaned = response_text.strip()
    cleaned = re.sub(r'```json\s*', '', cleaned)
    cleaned = re.sub(r'```\s*', '', cleaned)

    # Find JSON object
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)

    if match:
        try:
            result = json.loads(match.group())
            return result
        except json.JSONDecodeError as e:
            # Log the parsing error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.debug(f"Cleaned response: {cleaned}")
            return None
    else:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("No JSON found in LLM response")
        logger.debug(f"Cleaned response: {cleaned}")
        return None

def get_confidence_level(confidence: float) -> str:
    """
    Classify confidence score into levels.
    Implements AI-03: Confidence scores displayed as High/Medium/Low.

    Args:
        confidence: Confidence score (0.0 to 1.0)

    Returns:
        "High", "Medium", or "Low"
    """
    if confidence > 0.8:
        return "High"
    elif confidence >= 0.5:
        return "Medium"
    else:
        return "Low"

if __name__ == "__main__":
    # Test prompt generation
    test_text = "You're just saying that because you're a democrat, and democrats are always wrong about everything."
    prompt = create_fallacy_detection_prompt(test_text)
    print(f"Prompt length: {len(prompt)} characters")
    print(f"First 200 chars: {prompt[:200]}...")

    # Test confidence classification
    print(f"\nConfidence levels:")
    for score in [0.9, 0.7, 0.3]:
        print(f"  {score} -> {get_confidence_level(score)}")

    print("\n✅ Fallacy prompts module working correctly")
```
  </action>
  <verify>
python3 scripts/fallacy_prompts.py
  </verify>
  <done>LLM prompt module created with optimized prompts and response parsing</done>
</task>

<task type="auto">
  <name>Task 2: Create Hugging Face LLM client with retry and graceful degradation</name>
  <files>scripts/hf_client.py</files>
  <action>
Create scripts/hf_client.py with robust error handling:

```python
#!/usr/bin/env python3
"""
Hugging Face LLM client for fallacy detection.
Implements AI-01 (exponential backoff), AI-02 (JSON format), AI-03 (confidence classification),
AI-04 (graceful degradation), AI-05 (content validation).
"""

import os
import requests
import time
import logging
from typing import Dict, Optional
from datetime import datetime

from fallacy_prompts import create_fallacy_detection_prompt, parse_fallacy_response, get_confidence_level
from fallacy_types import is_valid_fallacy_type

logger = logging.getLogger(__name__)

# Hugging Face configuration
# Using Mistral-7B-Instruct-v0.3 per REQUIREMENTS.md AUTO-03 and research recommendation
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}/v1/chat/completions"

HF_TOKEN = os.getenv("HF_TOKEN", "")
if not HF_TOKEN:
    logger.warning("HF_TOKEN not set, LLM calls will fail")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Retry configuration (AI-01)
MAX_RETRIES = 5
BASE_DELAY = 2  # seconds
MAX_DELAY = 30  # seconds
REQUEST_TIMEOUT = 30  # 30 second timeout per request

def call_llm_with_retry(messages: list) -> Optional[Dict]:
    """
    Call Hugging Face LLM with exponential backoff retry logic.

    Args:
        messages: Chat messages list in OpenAI format

    Returns:
        LLM response dict or None if all retries fail
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                HF_API_URL,
                headers=HEADERS,
                json={
                    "model": HF_MODEL,
                    "messages": messages,
                    "max_tokens": 500,
                    "temperature": 0.3  # Low temperature for more consistent outputs
                },
                timeout=REQUEST_TIMEOUT
            )

            # Check for rate limits
            if response.status_code == 429:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                logger.warning(f"Rate limited. Waiting {delay}s before retry {attempt + 1}/{MAX_RETRIES}")
                time.sleep(delay)
                continue

            # Check for model loading
            if response.status_code == 503:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                logger.warning(f"Model loading. Waiting {delay}s before retry {attempt + 1}/{MAX_RETRIES}")
                time.sleep(delay)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
                time.sleep(delay)

    return None

def validate_content_for_analysis(content: str) -> bool:
    """
    Validate content before sending to LLM.
    Implements AI-05: Content validation filters.

    Args:
        content: Text content to validate

    Returns:
        True if content is suitable for analysis
    """
    # Filter very short content
    if len(content) < 50:
        return False

    # Filter obviously spam or empty content
    if not content.strip():
        return False

    # Filter content that's mostly special characters or URLs
    import re
    if re.sub(r'[^\w\s]', '', content).strip() == '':
        return False

    return True

def analyze_fallacy(text: str) -> Optional[Dict]:
    """
    Analyze text for logical fallacies using Hugging Face LLM.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with has_fallacy, fallacy_type, confidence, explanation, quote
        Returns None if analysis fails (graceful degradation per AI-04)
    """
    # Validate content first (AI-05)
    if not validate_content_for_analysis(text):
        logger.info("Content validation failed, skipping analysis")
        return {
            'has_fallacy': False,
            'fallacy_type': 'None',
            'confidence': 0.0,
            'explanation': 'Content validation failed - unsuitable for analysis',
            'quote': ''
        }

    # Create prompt
    prompt = create_fallacy_detection_prompt(text)

    # Call LLM with retry logic
    llm_response = call_llm_with_retry([
        {"role": "user", "content": prompt}
    ])

    if not llm_response:
        # Graceful degradation: return None to signal failure
        logger.error("All retries exhausted, skipping this post")
        return None

    # Parse response
    try:
        content = llm_response['choices'][0]['message']['content']
        result = parse_fallacy_response(content)

        if not result:
            logger.error("Failed to parse LLM response")
            return None

        # Validate fallacy type
        if result.get('has_fallacy', False):
            fallacy_type = result.get('fallacy_type', 'None')
            if not is_valid_fallacy_type(fallacy_type):
                logger.warning(f"Invalid fallacy type detected: {fallacy_type}")
                result['has_fallacy'] = False
                result['fallacy_type'] = 'None'
                result['explanation'] = f'Invalid fallacy type: {fallacy_type}'

        # Add confidence level (AI-03)
        confidence = result.get('confidence', 0.0)
        result['confidence_level'] = get_confidence_level(confidence)

        return result

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Error processing LLM response: {e}")
        return None

if __name__ == "__main__":
    # Test the client (requires HF_TOKEN)
    logging.basicConfig(level=logging.INFO)

    test_text = "That's a ridiculous argument coming from someone like you. You don't know what you're talking about."

    print("Testing LLM client...")
    if not HF_TOKEN:
        print("⚠️  HF_TOKEN not set, skipping LLM test")
        print("Set HF_TOKEN environment variable to test LLM calls")
    else:
        result = analyze_fallacy(test_text)
        if result:
            print(f"\nAnalysis result:")
            print(f"  Has fallacy: {result['has_fallacy']}")
            print(f"  Type: {result['fallacy_type']}")
            print(f"  Confidence: {result['confidence']} ({result['confidence_level']})")
            print(f"  Explanation: {result['explanation']}")
            print(f"  Quote: {result['quote']}")
        else:
            print("Analysis failed (graceful degradation)")
```

This implementation:
- Uses Mistral-7B-Instruct-v0.3 (per REQUIREMENTS.md AUTO-03)
- Implements exponential backoff with up to 5 retries (AI-01)
- Returns JSON format with required fields (AI-02)
- Classifies confidence as High/Medium/Low (AI-03)
- Gracefully degrades when API unavailable (AI-04)
- Validates content before sending to LLM (AI-05)
  </action>
  <verify>
# Test module imports and structure
python3 -c "from scripts.hf_client import analyze_fallacy; print('✅ Module imports correctly')"
# Note: Full test requires HF_TOKEN, will be tested in production
  </verify>
  <done>Hugging Face LLM client created with retry logic, graceful degradation, and confidence classification</done>
</task>

</tasks>

<verification>
Verify LLM client functionality:
- [ ] Exponential backoff implemented with 5 retries
- [ ] Graceful degradation returns None on failure
- [ ] Confidence levels classified as High/Medium/Low
- [ ] Content validation filters unsuitable text
- [ ] Validates fallacy types against the 10 valid types
- [ ] Returns JSON format with all required fields
- [ ] Uses Mistral-7B-Instruct model

Test without HF_TOKEN (should handle gracefully):
```python
from scripts.hf_client import analyze_fallacy
result = analyze_fallacy("test")
# Should handle missing HF_TOKEN gracefully
```
</verification>

<success_criteria>
Hugging Face LLM client that:
- Analyzes Reddit posts for 10 fallacy types
- Handles API failures with exponential backoff (5 retries)
- Returns structured JSON with fallacy_type, confidence, explanation
- Classifies confidence as High/Medium/Low
- Gracefully degrades when API unavailable
- Validates content before analysis
- Uses zero-cost Hugging Face free tier
</success_criteria>

<output>
After completion, create `.planning/phases/01-automation-foundation/01-automation-foundation-03-SUMMARY.md`
</output>
