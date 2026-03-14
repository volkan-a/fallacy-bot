#!/usr/bin/env python3
"""
Image Generator for Fallacy Tarot.
Implements IMG-01, IMG-02, IMG-03, IMG-04, IMG-05, IMG-06.
Calls Hugging Face Inference API for Stable Diffusion XL to generate tarot cards.
Includes retry logic, exponential backoff, image compression, and fallback handling.
"""

import os
import io
import time
import json
import logging
from datetime import datetime
from typing import Dict, Optional
import requests
from PIL import Image

logger = logging.getLogger(__name__)

# Hugging Face configuration
# Using a fast SDXL lightning model or standard SDXL via Inference API
# "stabilityai/stable-diffusion-xl-base-1.0" is the standard, but we'll use a reliable fast one
HF_IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_IMAGE_MODEL}"

# We'll use SD_TOKEN if available, otherwise fallback to HF_TOKEN
API_TOKEN = os.getenv("SD_TOKEN") or os.getenv("HF_TOKEN", "")

if not API_TOKEN:
    logger.warning("SD_TOKEN and HF_TOKEN not set, image generation will fail")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
}

# Directories
ASSETS_DIR = "docs/assets"
PLACEHOLDER_DIR = "docs/assets/placeholders"
PLACEHOLDER_PATH = os.path.join(PLACEHOLDER_DIR, "fallback_card.svg")

# Retry configuration
MAX_RETRIES = 4
BASE_DELAY = 5  # seconds
MAX_DELAY = 60  # seconds
REQUEST_TIMEOUT = 90  # 90 seconds timeout for image generation

# Prompts optimized for mystical tarot style (IMG-02)
STYLE_PROMPT = "mystical tarot card illustration, highly detailed, deep blues and purples, gold accents, magical, esoteric, intricate borders, professional fantasy art, masterpieces"
NEGATIVE_PROMPT = (
    "text, words, letters, ugly, deformed, blurry, poor quality, watermark, signature"
)

# Specific metaphors for each fallacy type
FALLACY_METAPHORS = {
    "Ad Hominem": "a warrior attacking the messenger instead of the message, shield and sword",
    "Straw Man": "a scarecrow being attacked by wind, fields of wheat",
    "Appeal to Authority": "a king on a throne dictating truth, crown and scepter",
    "False Dilemma": "two extreme paths diverging in a dark forest, black and white choices",
    "Slippery Slope": "a boulder rolling down a steep mountain, avalanche",
    "Circular Reasoning": "an ouroboros snake eating its own tail, infinite loop",
    "Hasty Generalization": "a single drop of water reflecting a whole ocean, jumping to conclusions",
    "Red Herring": "a glowing red fish distracting a hound, misdirection",
    "Tu Quoque": "two figures pointing accusing fingers at each other, mirrors",
    "Appeal to Emotion": "a heart glowing with intense light overriding a brain, tears and fire",
    "None": "a blank mystical mirror, cloudy crystal ball",
}


def ensure_directories():
    """Ensure output directories exist."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    os.makedirs(PLACEHOLDER_DIR, exist_ok=True)

    # Create a basic fallback SVG if it doesn't exist
    if not os.path.exists(PLACEHOLDER_PATH):
        create_fallback_svg()


def create_fallback_svg():
    """Create a basic SVG placeholder for when image generation fails."""
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" width="100%" height="100%">
  <rect width="400" height="600" fill="#1a1c29" rx="15" ry="15"/>
  <rect width="360" height="560" x="20" y="20" fill="none" stroke="#d4af37" stroke-width="4" rx="10" ry="10"/>
  <rect width="340" height="540" x="30" y="30" fill="none" stroke="#d4af37" stroke-width="1" rx="5" ry="5"/>
  <circle cx="200" cy="300" r="80" fill="none" stroke="#4A90A4" stroke-width="2"/>
  <path d="M 200 220 L 250 350 L 150 350 Z" fill="none" stroke="#2C5F7A" stroke-width="2"/>
  <circle cx="200" cy="300" r="10" fill="#d4af37"/>
  <text x="200" y="450" font-family="sans-serif" font-size="20" fill="#F8F9FA" text-anchor="middle" letter-spacing="2">MYSTIC VISION</text>
  <text x="200" y="480" font-family="sans-serif" font-size="12" fill="#6C757D" text-anchor="middle">IMAGE UNAVAILABLE</text>
</svg>"""
    with open(PLACEHOLDER_PATH, "w") as f:
        f.write(svg_content)
    logger.info(f"Created fallback placeholder at {PLACEHOLDER_PATH}")


def generate_image_bytes(fallacy_type: str) -> Optional[bytes]:
    """
    Call Hugging Face SDXL API to generate an image.

    Args:
        fallacy_type: The type of fallacy to generate an image for

    Returns:
        Image bytes or None if generation fails
    """
    if not API_TOKEN:
        logger.error("Cannot generate image: API token not set")
        return None

    # Get specific metaphor or use generic
    metaphor = FALLACY_METAPHORS.get(
        fallacy_type, "mystical abstract representation of logic"
    )

    # Construct full prompt
    prompt = f"{metaphor}, {STYLE_PROMPT}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": NEGATIVE_PROMPT,
            "num_inference_steps": 25,
            "guidance_scale": 7.5,
        },
    }

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(
                f"Image generation attempt {attempt + 1}/{MAX_RETRIES} for '{fallacy_type}'..."
            )

            response = requests.post(
                HF_API_URL, headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT
            )

            # Check for model loading (503) or rate limits (429)
            if response.status_code in (503, 429):
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                # Model loading often takes time, so we add extra delay for 503
                if response.status_code == 503:
                    delay += 10
                    logger.warning(
                        f"Model loading (503). Waiting {delay}s before retry"
                    )
                else:
                    logger.warning(f"Rate limited (429). Waiting {delay}s before retry")

                time.sleep(delay)
                continue

            response.raise_for_status()

            # Verify we actually got an image back (not a JSON error object)
            if response.headers.get("content-type", "").startswith("image/"):
                logger.info(f"Successfully generated image for '{fallacy_type}'")
                return response.content
            else:
                logger.error(
                    f"Expected image, got {response.headers.get('content-type')}"
                )
                try:
                    error_msg = response.json()
                    logger.error(f"API Error details: {error_msg}")
                except:
                    pass

                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                time.sleep(delay)

        except requests.exceptions.Timeout:
            logger.warning(
                f"Image generation timeout on attempt {attempt + 1}/{MAX_RETRIES}"
            )
            delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
            time.sleep(delay)

        except requests.exceptions.RequestException as e:
            logger.error(f"Image generation request failed: {e}")
            delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
            time.sleep(delay)

    logger.error(
        f"Failed to generate image for '{fallacy_type}' after {MAX_RETRIES} attempts"
    )
    return None


def process_and_save_image(image_bytes: bytes, fallacy_type: str) -> str:
    """
    Compress and save the generated image.
    Implements IMG-04: Image compression (< 500KB) and IMG-06: Naming convention.

    Args:
        image_bytes: Raw image bytes from API
        fallacy_type: The fallacy type for naming

    Returns:
        Relative path to the saved image
    """
    try:
        # Load image with Pillow
        image = Image.open(io.BytesIO(image_bytes))

        # Resize if too large (SDXL typically outputs 1024x1024, resize to 600x900 for cards)
        # We want a portrait aspect ratio for tarot cards

        # Calculate crop box to get 2:3 aspect ratio (tarot card proportion)
        width, height = image.size
        target_ratio = 2 / 3
        current_ratio = width / height

        if current_ratio > target_ratio:
            # Image is too wide, crop width
            new_width = int(height * target_ratio)
            left = (width - new_width) / 2
            right = left + new_width
            crop_box = (left, 0, right, height)
        else:
            # Image is too tall, crop height
            new_height = int(width / target_ratio)
            top = (height - new_height) / 2
            bottom = top + new_height
            crop_box = (0, top, width, bottom)

        # Crop and resize
        cropped_img = image.crop(crop_box)
        resized_img = cropped_img.resize((400, 600), Image.Resampling.LANCZOS)

        # Generate filename
        clean_name = "".join(c if c.isalnum() else "_" for c in fallacy_type).lower()
        clean_name = clean_name.replace("__", "_").strip("_")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{clean_name}_{timestamp}.jpg"

        filepath = os.path.join(ASSETS_DIR, filename)

        # Save with optimization to keep file size small
        # Convert to RGB in case it's RGBA
        if resized_img.mode in ("RGBA", "P"):
            resized_img = resized_img.convert("RGB")

        resized_img.save(filepath, format="JPEG", optimize=True, quality=85)

        # Check file size
        size_kb = os.path.getsize(filepath) / 1024
        logger.info(f"Saved optimized image {filename} ({size_kb:.1f} KB)")

        # Return relative path starting with assets/ for the frontend
        return f"assets/{filename}"

    except Exception as e:
        logger.error(f"Error processing and saving image: {e}")
        return "assets/placeholders/fallback_card.svg"


def generate_card_for_fallacy(fallacy_type: str) -> str:
    """
    Main entry point to generate a card for a fallacy.
    Handles fallback if generation fails.

    Args:
        fallacy_type: The fallacy to generate an image for

    Returns:
        Relative path to the image to use (generated or fallback)
    """
    if fallacy_type == "None" or not fallacy_type:
        return "assets/placeholders/fallback_card.svg"

    ensure_directories()

    image_bytes = generate_image_bytes(fallacy_type)

    if image_bytes:
        return process_and_save_image(image_bytes, fallacy_type)
    else:
        # Implements IMG-05: Fallback placeholder
        logger.warning(f"Using fallback image for {fallacy_type}")
        return "assets/placeholders/fallback_card.svg"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ensure_directories()

    print("Testing image generator...")
    if not API_TOKEN:
        print("⚠️ API Token not set. Only testing fallback mechanism.")
        print(f"Fallback path: {generate_card_for_fallacy('Ad Hominem')}")
    else:
        print("Generating test image (this may take a minute)...")
        path = generate_card_for_fallacy("Straw Man")
        print(f"Image saved to: {path}")
