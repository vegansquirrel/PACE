from pathlib import Path

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # This goes up from config/ to project root
DOCUMENT_PATHS = {
    "term_sheet": PROJECT_ROOT / "input" / "Final-Terms_GB00BTC0W820.pdf",
    "prospectus": PROJECT_ROOT / "input" / "GS-Series-P-Master-Base-Prospectus-12-January-2024-FINAL.pdf"
}


OPENAI_API_KEY = "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"  # Or load from .env
GPT_MODEL = "gpt-4-turbo"