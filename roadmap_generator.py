"""
roadmap_generator.py
Module 6: Skill-gap analysis
Compares extracted resume skills with a target role's requirements
and generates a simple week-by-week learning roadmap for missing skills.
"""


def analyze_skill_gap(found_skills: list[str], required_skills: list[str]) -> dict:
    found_set = set(found_skills)
    required_set = set(required_skills)

    matched = sorted(found_set & required_set)
    missing = sorted(required_set - found_set)

    coverage_pct = round((len(matched) / len(required_set)) * 100, 1) if required_set else 0.0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage_pct": coverage_pct,
    }


def generate_roadmap(missing_skills: list[str], weeks_per_skill: int = 1) -> list[dict]:
    """
    Rule-based roadmap: allocate a study week to each missing skill,
    in the order they appear.
    """
    roadmap = []
    for i, skill in enumerate(missing_skills, start=1):
        roadmap.append({
            "week": i,
            "focus": skill,
            "suggestion": f"Learn the fundamentals of '{skill}' and build one small project using it.",
        })
    return roadmap
