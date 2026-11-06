"""
skill_extractor.py
Identifies technical/job-related skills in cleaned resume text
using a controlled skill dictionary (Module 3).
"""

import re
import pandas as pd


def load_skill_dictionary(path: str = "data/skill_dictionary.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def _skill_pattern(skill: str) -> re.Pattern:
    """
    Build a regex that matches the skill as a whole phrase.
    Uses word boundaries where safe; falls back to plain substring
    matching for skills containing symbols like C++ or .NET.
    """
    normalized = skill.lower().replace("-", " ")
    escaped = re.escape(normalized)
    if re.match(r"^[a-z0-9\s]+$", normalized):
        return re.compile(rf"\b{escaped}\b")
    return re.compile(re.escape(skill.lower()))


def extract_skills(cleaned_text: str, skill_df: pd.DataFrame) -> dict:
    """
    Search cleaned resume text for each skill in the dictionary.
    Returns skills grouped by category, e.g.
    {"programming": ["python", "sql"], "ml": ["machine learning"]}
    """
    found_by_category: dict[str, list[str]] = {}

    for _, row in skill_df.iterrows():
        skill = str(row["skill"]).strip().lower()
        category = str(row["category"]).strip().lower()
        pattern = _skill_pattern(skill)
        if pattern.search(cleaned_text):
            found_by_category.setdefault(category, [])
            if skill not in found_by_category[category]:
                found_by_category[category].append(skill)

    return found_by_category


def flatten_found_skills(found_by_category: dict) -> list[str]:
    all_skills = []
    for skills in found_by_category.values():
        all_skills.extend(skills)
    return sorted(set(all_skills))
