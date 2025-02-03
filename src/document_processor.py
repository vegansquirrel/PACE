import pdfplumber
from openai import OpenAI
from pathlib import Path
from config.config import OPENAI_API_KEY, GPT_MODEL, DOCUMENT_PATHS
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_text(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)

def parse_terms_with_gpt(text: str) -> dict:
    """Use GPT to extract structured terms from text."""
    response = client.chat.completions.create(
        model=GPT_MODEL,
         messages=[{
        "role": "user",
        "content":f"""
    Extract financial terms from this term sheet as JSON. Follow these rules:
    1. For "underlying_assets", include ALL assets (stocks, indices, etc.) with:
       - "name" (e.g., "Apple Inc. shares")
       - "ticker" (e.g., "AAPL" or "ENGI.PA")
       - "exchange" (e.g., "Euronext Paris")
    2. For "payment_terms", include:
        - "initial_level": [numeric value from "Asset Initial Price" section]
       - "autocall_level" (as a percentage, e.g., 100)
       - "barrier_level" (as a percentage, e.g., 70)
       - "coupon_rate" (as a decimal, e.g., 0.0785)
       - "observation_dates" (list of dates in YYYY-MM-DD format)
    3. For "principal":
       - "amount" (e.g., 100)
       - "currency" (e.g., "EUR")

    Example Output:
    {{
      "underlying_assets": [
        {{"name": "Engie shares", "ticker": "ENGI.PA", "exchange": "Euronext Paris"}}
      ],
      "payment_terms": {{
        "autocall_level": 100,
        "barrier_level": 70,
        "coupon_rate": 0.0785,
        "observation_dates": ["2025-06-13", "2025-12-15"]
      }},
      "principal": {{"amount": 100, "currency": "EUR"}}
    }}

    Term Sheet Text:
    {text[:15000]}
    """  # Handle token limits
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)