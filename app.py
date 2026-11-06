"""
app.py
Streamlit dashboard for the AI Resume Analyzer and Job Recommendation System.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import is_valid_file, extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import load_skill_dictionary, extract_skills, flatten_found_skills
from job_matcher import load_job_roles, match_resume_to_roles, top_n_roles
from roadmap_generator import analyze_skill_gap, generate_roadmap

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer & Job Recommendation System")
st.caption(
    "Upload your resume to see how well it matches different job roles, "
    "spot missing skills, and get a simple learning roadmap. "
    "This is guidance only — not a hiring decision."
)

# ---------- Load reference data ----------
skill_dict_df = load_skill_dictionary("data/skill_dictionary.csv")
job_roles_df = load_job_roles("data/job_roles.csv")

# ---------- Module 1: Resume Upload ----------
st.subheader("1. Upload your resume")
uploaded_file = st.file_uploader("Upload a PDF or DOCX resume", type=["pdf", "docx"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    valid, error_msg = is_valid_file(uploaded_file.name, len(file_bytes))

    if not valid:
        st.error(error_msg)
        st.stop()

    st.success(f"Uploaded: {uploaded_file.name} ({len(file_bytes) / 1024:.1f} KB)")

    # ---------- Module 2: Text Extraction and Cleaning ----------
    with st.spinner("Extracting and cleaning resume text..."):
        raw_text = extract_resume_text(uploaded_file.name, file_bytes)
        cleaned_text = clean_resume_text(raw_text)

    if not cleaned_text.strip():
        st.warning(
            "No readable text was found in this file. "
            "It may be a scanned/image-based resume — try a text-based PDF or DOCX."
        )
        st.stop()

    # ---------- Module 3: Skill Extraction ----------
    found_by_category = extract_skills(cleaned_text, skill_dict_df)
    found_skills_flat = flatten_found_skills(found_by_category)

    st.subheader("2. Skills found in your resume")
    if found_skills_flat:
        cols = st.columns(min(4, len(found_by_category)) or 1)
        for i, (category, skills) in enumerate(found_by_category.items()):
            with cols[i % len(cols)]:
                st.markdown(f"**{category.title()}**")
                for s in skills:
                    st.write(f"- {s}")
    else:
        st.info("No known skills were detected. Consider expanding the skill dictionary.")

    # ---------- Module 5: Matching and Recommendation ----------
    st.subheader("3. Target role & match scores")
    target_role = st.selectbox("Select a target role", job_roles_df["role"].tolist())

    ranked_roles = match_resume_to_roles(cleaned_text, job_roles_df)
    top_matches = top_n_roles(ranked_roles, n=3)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        target_score_row = ranked_roles[ranked_roles["role"] == target_role]
        target_score = target_score_row["match_score"].values[0] if not target_score_row.empty else 0.0
        st.metric(f"Match score for '{target_role}'", f"{target_score}%")

        fig = px.bar(
            top_matches,
            x="role",
            y="match_score",
            title="Top 3 recommended roles",
            labels={"match_score": "Match score (%)", "role": "Role"},
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------- Module 6: Skill-Gap Analysis ----------
    with col_b:
        target_required_skills = job_roles_df.loc[
            job_roles_df["role"] == target_role, "required_skills"
        ].values[0]

        gap = analyze_skill_gap(found_skills_flat, target_required_skills)

        st.markdown(f"**Skill coverage for '{target_role}': {gap['coverage_pct']}%**")

        st.markdown("✅ **Skills you have:**")
        st.write(", ".join(gap["matched_skills"]) if gap["matched_skills"] else "None found yet.")

        st.markdown("❌ **Missing skills:**")
        st.write(", ".join(gap["missing_skills"]) if gap["missing_skills"] else "None — great match!")

    # ---------- Roadmap ----------
    st.subheader("4. Suggested learning roadmap")
    roadmap = generate_roadmap(gap["missing_skills"])
    if roadmap:
        roadmap_df = pd.DataFrame(roadmap)
        st.table(roadmap_df.rename(columns={"week": "Week", "focus": "Focus", "suggestion": "Suggestion"}))
    else:
        st.success("No skill gaps for this role — nothing to add to the roadmap!")

    # ---------- Downloadable report ----------
    st.subheader("5. Download your analysis report")
    report_lines = [
        f"AI Resume Analyzer Report",
        f"Target Role: {target_role}",
        f"Match Score: {target_score}%",
        "",
        "Skills Found:",
        *(f"- {s}" for s in found_skills_flat),
        "",
        "Missing Skills:",
        *(f"- {s}" for s in gap["missing_skills"]),
        "",
        "Top Recommended Roles:",
        *(f"{i+1}. {row.role} - {row.match_score}%" for i, row in top_matches.iterrows()),
        "",
        "Suggested Roadmap:",
        *(f"Week {r['week']}: {r['suggestion']}" for r in roadmap),
        "",
        "Note: This score is an estimate based on keyword/skill overlap, not a recruiter decision.",
    ]
    report_text = "\n".join(report_lines)

    st.download_button(
        label="Download report (.txt)",
        data=report_text,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )

else:
    st.info("Upload a resume above to get started.")

st.divider()
st.caption(
    "Responsible AI note: this tool does not use gender, age, religion, nationality, "
    "photograph, marital status, or disability in scoring. Match scores are estimates "
    "based on skill overlap, not a hiring recommendation."
)
