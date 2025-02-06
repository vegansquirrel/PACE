import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
DOCUMENT_PATHS = {
    "term_sheet": PROJECT_ROOT / "data" / "input" / "term_sheets\Final-terms-Pricing-supplement-_2024-02-08.pdf"
}

class Config:
    load_dotenv(PROJECT_ROOT / '.env')
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = "gpt-4-turbo"
    MAX_TOKENS = 4000