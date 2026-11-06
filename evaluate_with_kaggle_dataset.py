"""
evaluate_with_kaggle_dataset.py

Uses the Kaggle "Resume Dataset" (Category, Resume columns) to bulk-test
the skill extraction and job-matching pipeline (Module 11: Testing and Evaluation).

Download the real dataset from Kaggle, e.g.:
  https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset
and save it as data/UpdatedResumeDataSet.csv (replacing the small placeholder
file that ships with this project). It must have columns: Category, Resume.

Run from the project root with:
  python tests/evaluate_with_kaggle_dataset.py
"""

import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from text_cleaner import clean_resume_text
from skill_extractor import load_skill_dictionary, extract_skills, flatten_found_skills
from job_matcher import load_job_roles, match_resume_to_roles

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "UpdatedResumeDataSet.csv")
JOB_ROLES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "job_roles.csv")
SKILL_DICT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skill_dictionary.csv")


def run_evaluation(sample_size: int = 20):
    df = pd.read_csv(DATA_PATH)
    if sample_size:
        df = df.head(sample_size)

    skill_dict_df = load_skill_dictionary(SKILL_DICT_PATH)
    job_roles_df = load_job_roles(JOB_ROLES_PATH)

    results = []
    for _, row in df.iterrows():
        raw_text = str(row["Resume"])
        true_category = str(row["Category"])

        cleaned = clean_resume_text(raw_text)
        found_by_category = extract_skills(cleaned, skill_dict_df)
        found_skills = flatten_found_skills(found_by_category)

        ranked = match_resume_to_roles(cleaned, job_roles_df)
        predicted_role = ranked.iloc[0]["role"]
        predicted_score = ranked.iloc[0]["match_score"]

        results.append({
            "true_category": true_category,
            "predicted_top_role": predicted_role,
            "predicted_score": predicted_score,
            "num_skills_found": len(found_skills),
        })

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    output_path = os.path.join(os.path.dirname(__file__), "evaluation_results.csv")
    results_df.to_csv(output_path, index=False)
    print(f"\nSaved detailed results to {output_path}")


if __name__ == "__main__":
    run_evaluation()
