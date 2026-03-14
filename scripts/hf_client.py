#!/usr/bin/env python3
"""
Hugging Face LLM client using InferenceClient.
Using Zephyr-7b-beta: The most reliable model on Free Inference API.
"""

import os
import logging
from typing import Dict, Optional
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

# Zephyr 7b beta: Hugging Face'in en stabil çalışan ücretsiz modeli
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"

# client endpoint'i otomatik yönlendirir
client = InferenceClient(model=HF_MODEL, token=os.getenv("HF_TOKEN"))


def analyze_fallacy(text: str) -> Optional[Dict]:
    """Analyze text for logical fallacies using Hugging Face LLM."""
    from scripts.fallacy_prompts import (
        create_fallacy_detection_prompt,
        parse_fallacy_response,
        get_confidence_level,
    )
    from scripts.fallacy_types import is_valid_fallacy_type

    prompt = create_fallacy_detection_prompt(text)

    try:
        # Chat model olduğu için chat_completion kullanıyoruz
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )

        content = response.choices[0].message.content
        result = parse_fallacy_response(content)

        if result:
            confidence = result.get("confidence", 0.0)
            result["confidence_level"] = get_confidence_level(confidence)

            if result.get("has_fallacy") and not is_valid_fallacy_type(
                result.get("fallacy_type", "")
            ):
                result["has_fallacy"] = False
                result["fallacy_type"] = "None"
            return result

    except Exception as e:
        logger.error(f"LLM request failed: {e}")
    return None
