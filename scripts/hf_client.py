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

from fallacy_prompts import (
    create_fallacy_detection_prompt,
    parse_fallacy_response,
    get_confidence_level,
)
from fallacy_types import is_valid_fallacy_type

logger = logging.getLogger(__name__)

# Hugging Face configuration
# Using Mistral-7B-Instruct-v0.3 per REQUIREMENTS.md AUTO-03 and research recommendation
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
HF_API_URL = (
    f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}/v1/chat/completions"
)

HF_TOKEN = os.getenv("HF_TOKEN", "")
if not HF_TOKEN:
    logger.warning("HF_TOKEN not set, LLM calls will fail")

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

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
                    "temperature": 0.3,  # Low temperature for more consistent outputs
                },
                timeout=REQUEST_TIMEOUT,
            )

            # Check for rate limits
            if response.status_code == 429:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                logger.warning(
                    f"Rate limited. Waiting {delay}s before retry {attempt + 1}/{MAX_RETRIES}"
                )
                time.sleep(delay)
                continue

            # Check for model loading
            if response.status_code == 503:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                logger.warning(
                    f"Model loading. Waiting {delay}s before retry {attempt + 1}/{MAX_RETRIES}"
                )
                time.sleep(delay)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}/{MAX_RETRIES}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                time.sleep(delay)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on attempt {attempt + 1}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
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

    if re.sub(r"[^\w\s]", "", content).strip() == "":
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
            "has_fallacy": False,
            "fallacy_type": "None",
            "confidence": 0.0,
            "explanation": "Content validation failed - unsuitable for analysis",
            "quote": "",
        }

    # Create prompt
    prompt = create_fallacy_detection_prompt(text)

    # Call LLM with retry logic
    llm_response = call_llm_with_retry([{"role": "user", "content": prompt}])

    if not llm_response:
        # Graceful degradation: return None to signal failure (AI-04)
        logger.error("All retries exhausted, skipping this post")
        return None

    # Parse response
    try:
        content = llm_response["choices"][0]["message"]["content"]
        result = parse_fallacy_response(content)

        if not result:
            logger.error("Failed to parse LLM response")
            return None

        # Validate fallacy type
        if result.get("has_fallacy", False):
            fallacy_type = result.get("fallacy_type", "None")
            if not is_valid_fallacy_type(fallacy_type):
                logger.warning(f"Invalid fallacy type detected: {fallacy_type}")
                result["has_fallacy"] = False
                result["fallacy_type"] = "None"
                result["explanation"] = f"Invalid fallacy type: {fallacy_type}"

        # Add confidence level (AI-03)
        confidence = result.get("confidence", 0.0)
        result["confidence_level"] = get_confidence_level(confidence)

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
            print(
                f"  Confidence: {result['confidence']} ({result['confidence_level']})"
            )
            print(f"  Explanation: {result['explanation']}")
            print(f"  Quote: {result['quote']}")
        else:
            print("Analysis failed (graceful degradation)")
