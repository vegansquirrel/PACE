import pdfplumber
from openai import OpenAI
from pathlib import Path
import json
from config.config import OPENAI_API_KEY, GPT_MODEL, MAX_TOKENS

class DocumentProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF with layout preservation"""
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(
                f"{page.page_number}|{text}" 
                for page in pdf.pages
                for text in page.extract_text_simple().split('\n')
            )
    
    def chunk_text(self, text: str, chunk_size: int = 3000) -> list:
        """Split text into manageable chunks"""
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    def analyze_document(self, text: str) -> dict:
        """LLM-powered document analysis"""
        prompt = """Analyze this financial document and identify:
1. Product type (autocallable, convertible, etc.)
2. Underlying assets with identifiers
3. Key dates (observation, maturity)
4. Payment conditions
5. Special clauses

Return JSON format with keys: product_type, underlyings, dates, payment_terms"""

        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a financial document analyst"},
                {"role": "user", "content": f"{prompt}\n\n{text[:MAX_TOKENS]}"}
            ],
            temperature=0.1,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)