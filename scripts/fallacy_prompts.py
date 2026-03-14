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
5. Slippery Slope - Asserting a small step leads to extreme consequences
6. Circular Reasoning - The conclusion is included in the premise
7. Hasty Generalization - Drawing conclusion from insufficient evidence
8. Red Herring - Introducing irrelevant information to divert attention
9. Tu Quoque - Avoiding criticism by accusing opponent of the same thing
10. Appeal to Emotion - Manipulating emotions rather than using logic

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
    cleaned = re.sub(r"```json\s*", "", cleaned)
    cleaned = re.sub(r"```\s*", "", cleaned)

    # Find JSON object
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        try:
            result = json.loads(match.group())
            return result
        except json.JSONDecodeError as e:
            # Log parsing error
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
