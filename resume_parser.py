"""
resume_parser.py
Extracts raw text from an uploaded PDF or DOCX resume.
"""

from pypdf import PdfReader
import docx
import io

ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILE_SIZE_MB = 5


def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def is_valid_file(filename: str, file_size_bytes: int) -> tuple[bool, str]:
    """Validate file type and size before processing."""
    ext = get_file_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type '.{ext}'. Please upload a PDF or DOCX file."
    if file_size_bytes > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, f"File is too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB."
    return True, ""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from every page of a PDF resume."""
    reader = PdfReader(io.BytesIO(file_bytes))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)
    return "\n".join(pages_text)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from every paragraph of a DOCX resume, including tables."""
    document = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]

    # Also pull text out of any tables (many resumes use table layouts)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    paragraphs.append(cell.text)

    return "\n".join(paragraphs)


def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    """Route to the correct extractor based on file extension."""
    ext = get_file_extension(filename)
    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext == "docx":
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
