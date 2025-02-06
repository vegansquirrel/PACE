from src.adapters.llm_adapter import LLMAdapter
from src.utils.chunker import dynamic_chunker

class ConceptualAnalyzer:
    SYSTEM_PROMPT = """You are a financial document analyst. Analyze term sheets through:
1. Product Type Identification: autocallable, reverse convertible, etc.
2. Underlying Asset Recognition: stocks, indices, commodities
3. Temporal Event Detection: observation dates, maturity
4. Payment Condition Extraction: barriers, coupons, capital protection
5. Market Data Requirements: prices, volatilities, dividends"""

    def analyze(self, document_text):
        chunks = dynamic_chunker(document_text)
        analysis = {"sections": []}
        
        for chunk in chunks:
            response = LLMAdapter().query(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=f"""Analyze this document section:
                {chunk}
                
                Return JSON with:
                - product_type
                - underlyings: [{"name", "ticker", "type"}]
                - key_dates: {"observation", "maturity"}
                - payment_terms: {"type", "level", "currency"}
                - market_data_needed"""
            )
            analysis["sections"].append(response)
        
        return analysis