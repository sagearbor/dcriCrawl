from typing import Dict, List

AI_KEYWORDS: List[str] = [
    "artificial intelligence",
    "ai",
    "machine learning",
    "ml",
]

POLICY_KEYWORDS: List[str] = [
    "policy",
    "privacy",
    "terms of service",
    "data usage",
    "gdpr",
]

def detect_keywords(text: str) -> Dict[str, List[str]]:
    """Detect AI and policy keywords in the given text.

    Args:
        text: The text to scan.

    Returns:
        A dictionary with two keys: "ai" and "policy", each containing
        a list of keywords that were found in the text.
    """
    lowered = text.lower()
    ai_found = sorted({kw for kw in AI_KEYWORDS if kw in lowered})
    policy_found = sorted({kw for kw in POLICY_KEYWORDS if kw in lowered})
    return {"ai": list(ai_found), "policy": list(policy_found)}
