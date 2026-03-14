#!/usr/bin/env python3
"""
Fallacy type definitions for validation and analysis.
Based on REQUIREMENTS.md AUTO-04: System detects all 10 specific fallacy types.
"""

from typing import List

# The 10 fallacy types the system must detect
FALLACY_TYPES = [
    "Ad Hominem",
    "Straw Man",
    "Appeal to Authority",
    "False Dilemma",
    "Slippery Slope",
    "Circular Reasoning",
    "Hasty Generalization",
    "Red Herring",
    "Tu Quoque",
    "Appeal to Emotion",
]


def is_valid_fallacy_type(fallacy_type: str) -> bool:
    """
    Check if a fallacy type is one of the 10 valid types.

    Args:
        fallacy_type: The fallacy type string to validate

    Returns:
        True if valid, False otherwise
    """
    return fallacy_type in FALLACY_TYPES


def get_fallacy_types() -> List[str]:
    """Return list of valid fallacy types"""
    return FALLACY_TYPES.copy()


if __name__ == "__main__":
    # Test validation
    print("Valid fallacy types:")
    for ft in FALLACY_TYPES:
        print(f"  - {ft}")

    # Test validation function
    assert is_valid_fallacy_type("Ad Hominem") == True
    assert is_valid_fallacy_type("Invalid Type") == False
    print("\n✅ Fallacy types validation working correctly")
