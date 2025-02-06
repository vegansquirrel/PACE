from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # This goes up from config/ to project root

DOCUMENT_PATHS = {
    "term_sheet": PROJECT_ROOT / "input" / "Final-Terms_GB00BTC0W820.pdf"
}

import pdfplumber
def extract_text(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)


print(PROJECT_ROOT)