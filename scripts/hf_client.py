#!/usr/bin/env python3
"""
Hugging Face LLM client using direct requests to router.huggingface.co.
"""

import os
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Model: Fallacy detection specific model
HF_MODEL = "mrm8488/logical-fallacy-detection"
# MUST use router.huggingface.co
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"
HF_TOKEN = os.getenv("HF_TOKEN", "")


def analyze_fallacy(text: str) -> Optional[Dict]:
    """Analyze text for logical fallacies using raw requests."""
    from scripts.fallacy_types import is_valid_fallacy_type

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text[:500]}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result_list = response.json()
            if isinstance(result_list, list) and len(result_list) > 0:
                # Get label with highest score
                best_match = max(result_list[0], key=lambda x: x["score"])
                fallacy_name = best_match.get("label", "None")

                return {
                    "has_fallacy": True,
                    "fallacy_type": fallacy_name
                    if is_valid_fallacy_type(fallacy_name)
                    else "Unknown",
                    "confidence": best_match.get("score", 0.0),
                    "explanation": f"Detected: {fallacy_name}",
                    "quote": text[:100],
                }
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"LLM request failed: {e}")
    return None
