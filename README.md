# AI Resume Analyzer & Job Recommendation System

An NLP-based Streamlit app that scores how well a resume matches different
job roles, lists missing skills, and generates a simple learning roadmap.

## How it works

1. Upload a PDF or DOCX resume.
2. Text is extracted and cleaned.
3. Skills are detected using a controlled skill dictionary (`data/skill_dictionary.csv`).
4. The resume is compared against job roles (`data/job_roles.csv`) using
   TF-IDF + cosine similarity.
5. You get: a match score, top 3 recommended roles, missing skills for your
   chosen target role, and a week-by-week learning roadmap.

## Project structure

```
ai_resume_analyzer/
├── app.py                     # Streamlit dashboard (entry point)
├── resume_parser.py           # PDF/DOCX text extraction + validation
├── text_cleaner.py            # Text normalization
├── skill_extractor.py         # Skill detection from skill_dictionary.csv
├── job_matcher.py             # TF-IDF + cosine similarity matching
├── roadmap_generator.py       # Skill-gap analysis + roadmap
├── requirements.txt
├── data/
│   ├── job_roles.csv          # Job roles + required skills
│   ├── skill_dictionary.csv   # Controlled skill list + categories
│   └── UpdatedResumeDataSet.csv  # Placeholder — replace with the real Kaggle file
├── tests/
│   └── evaluate_with_kaggle_dataset.py  # Bulk-tests the pipeline on the Kaggle dataset
└── sample_resumes/
```

## Using the Kaggle dataset

This project is set up for the Kaggle **Resume Dataset** format, which has
two columns: `Category` and `Resume` (raw resume text). A common source is:

- https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset

Steps:

1. Download the CSV from Kaggle.
2. Replace `data/UpdatedResumeDataSet.csv` in this project with the real file
   (keep the same filename, or update the path in
   `tests/evaluate_with_kaggle_dataset.py`).
3. Run the bulk evaluation script to see how well the matcher performs
   across hundreds of real, labeled resumes:

```bash
python tests/evaluate_with_kaggle_dataset.py
```

This prints a table comparing each resume's **true category** (from Kaggle)
to the **predicted top role** (from your matcher), and saves the full
results to `tests/evaluation_results.csv`. Use this to check precision/recall
and tune `data/skill_dictionary.csv` or `data/job_roles.csv`.

Note: the Kaggle dataset's categories (e.g. "Data Science", "Java Developer")
won't exactly match the role names in `job_roles.csv` — that's expected.
Part of the exercise is refining `job_roles.csv` so its role names and
required skills line up better with the categories you care about.

## Setup on Replit

1. Create a new Repl → **Python** template.
2. Upload every file/folder from this project into the Repl (drag-and-drop
   the whole `ai_resume_analyzer` folder, or use Replit's "Upload folder").
3. Open the Replit **Shell** tab and run:
   ```bash
   pip install -r requirements.txt
   ```
4. Replit doesn't run Streamlit apps via the green "Run" button by default —
   set the **Run command** (in `.replit` or Shell) to:
   ```bash
   streamlit run app.py --server.port 3000 --server.address 0.0.0.0
   ```
5. Click **Run**. Replit will give you a webview URL — open it to use the
   dashboard.

## Setup in Antigravity

1. Open Antigravity and create/open a new workspace.
2. Import or copy this `ai_resume_analyzer/` folder into the workspace.
3. Let Antigravity set up a Python environment, or run manually in its
   terminal:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app from the terminal:
   ```bash
   streamlit run app.py
   ```
5. Use Antigravity's preview/browser pane (or the local URL it prints,
   typically `http://localhost:8501`) to view the dashboard.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Responsible AI notes

- Match scores are **estimates** based on skill/keyword overlap — not a
  hiring or rejection decision.
- The system does not use gender, age, religion, nationality, photograph,
  marital status, or disability in scoring.
- Uploaded resumes are processed in-memory for the session and are not
  stored permanently.
- A missing keyword does not always mean missing ability — encourage users
  to treat the roadmap as a starting point, not a verdict.

## Next steps / optional advanced features

- Resume section detection (education, skills, projects, experience).
- Semantic matching with Sentence Transformers instead of TF-IDF.
- LLM-based resume feedback (Groq, Gemini, or OpenAI) with a controlled prompt.
- FastAPI backend + database + Docker deployment.
- Downloadable PDF (instead of .txt) analysis report.
