"""
job_matcher.py
Compares resume text against job-role requirements using
TF-IDF vectorization + cosine similarity (Module 5, beginner approach).
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles(path: str = "data/job_roles.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["required_skills"] = df["required_skills"].apply(
        lambda s: [skill.strip().lower() for skill in str(s).split(",")]
    )
    return df


def match_resume_to_roles(cleaned_resume_text: str, job_roles_df: pd.DataFrame) -> pd.DataFrame:
    """
    Vectorize the resume and each job role's skill list, then rank roles
    by cosine similarity to the resume text.
    Returns a DataFrame sorted by descending match_score (0-100).
    """
    role_documents = [" ".join(skills) for skills in job_roles_df["required_skills"]]
    corpus = [cleaned_resume_text] + role_documents

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    resume_vector = tfidf_matrix[0:1]
    role_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vector, role_vectors)[0]

    results = job_roles_df.copy()
    results["match_score"] = (similarities * 100).round(1)
    results = results.sort_values("match_score", ascending=False).reset_index(drop=True)
    return results


def top_n_roles(ranked_roles_df: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    return ranked_roles_df.head(n)
