#!/usr/bin/env python3
"""
Hugging Face LLM client using InferenceClient for Mistral text_generation.
Uses text_generation method which is stable for instruct-tuned models.
"""

import os
import logging
from typing import Dict, Optional
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

# Mistral 7B Instruct v0.3: En stabil, ücretsiz Inference API'de çalışan model
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

# client endpoint'i otomatik yönlendirir
client = InferenceClient(model=HF_MODEL, token=os.getenv("HF_TOKEN"))


def analyze_fallacy(text: str) -> Optional[Dict]:
    """Analyze text for logical fallacies."""
    from scripts.fallacy_prompts import (
        create_fallacy_detection_prompt,
        parse_fallacy_response,
        get_confidence_level,
    )
    from scripts.fallacy_types import is_valid_fallacy_type

    prompt = create_fallacy_detection_prompt(text)

    try:
        # Mistral-Instruct için text_generation kullanıyoruz
        # Prompt'u doğrudan string olarak veriyoruz
        response = client.text_generation(
            prompt, max_new_tokens=500, temperature=0.3, return_full_text=False
        )

        result = parse_fallacy_response(response)

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
