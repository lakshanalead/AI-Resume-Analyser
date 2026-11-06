"""
text_cleaner.py
Cleans and normalizes raw resume text while preserving
important technical symbols such as C++, C#, and .NET.
"""

import re

# Symbols that must NOT be stripped because they are part of real skill names
PROTECTED_TOKENS = ["c++", "c#", ".net", "node.js", "asp.net", "d3.js", "vue.js"]


def _protect_tokens(text: str) -> tuple[str, dict]:
    """Temporarily replace protected tokens with placeholders so regex cleanup
    doesn't destroy meaningful symbols like '++' or '#'."""
    placeholders = {}
    protected_text = text
    for i, token in enumerate(PROTECTED_TOKENS):
        placeholder = f"__token{i}__"
        pattern = re.compile(re.escape(token), re.IGNORECASE)
        if pattern.search(protected_text):
            protected_text = pattern.sub(placeholder, protected_text)
            placeholders[placeholder] = token
    return protected_text, placeholders


def _restore_tokens(text: str, placeholders: dict) -> str:
    for placeholder, token in placeholders.items():
        text = text.replace(placeholder, token)
    return text


def clean_resume_text(raw_text: str) -> str:
    """
    Clean resume text:
    - lowercase everything
    - protect technical symbols (C++, C#, .NET, etc.)
    - remove bullets, extra punctuation, and repeated whitespace
    """
    text = raw_text.lower()
    text, placeholders = _protect_tokens(text)

    # Remove bullet characters and stray symbols, but keep letters/digits/spaces/dots
    text = re.sub(r"[•▪●○·]", " ", text)
    text = re.sub(r"[^a-z0-9_.\s]", " ", text)

    # Collapse repeated whitespace
    text = re.sub(r"\s+", " ", text).strip()

    text = _restore_tokens(text, placeholders)
    return text
