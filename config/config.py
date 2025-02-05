from pathlib import Path
from dotenv import load_dotenv
import os

# Path configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_PATHS = {
    "term_sheet": PROJECT_ROOT / "input" / "Final-terms-Pricing-supplement-_2024-02-08.pdf"
}

# API configuration
load_dotenv(PROJECT_ROOT / '.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-4-turbo"
MAX_TOKENS = 4096 # Adjust based on model context window