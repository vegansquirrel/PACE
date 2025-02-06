import RestrictedPython
from src.adapters.market_data import MarketDataFetcher
from src.adapters.llm_adapter import LLMAdapter
import json
class CalculationEngine:
    CODE_PROMPT = """Generate Python code to calculate payments:

Requirements:
- Product Type: {product_type}
- Terms: {terms}
- Market Data: {market_data}

Rules:
1. Use defensive programming
2. Include validation checks
3. Handle edge cases
4. Output format: {{"amount", "currency", "conditions"}}

Return only the Python function code:"""

    def execute(self, terms, market_data):
        code = LLMAdapter().query(
            system_prompt="You are a financial quant developer",
            user_prompt=self.CODE_PROMPT.format(
                product_type=terms['product_type'],
                terms=json.dumps(terms['payment_terms']),
                market_data=list(market_data.keys())
            )
        )
        return self._safe_execute(code, terms, market_data)