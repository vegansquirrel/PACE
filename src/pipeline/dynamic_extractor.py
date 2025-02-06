import json
from src.adapters.llm_adapter import LLMAdapter

class DynamicExtractor:
    EXTRACTION_PROMPT = """Extract EXACT values from this term sheet:

Required Parameters:
{parameters}

Rules:
1. Maintain original units and precision
2. Handle conditional statements carefully
3. Cross-reference tables with text
4. Validate numerical consistency

Document:
{document}

Return JSON with:
- extracted_values
- confidence: 0-1
- validation_checks"""

    def extract(self, analysis, document_text):
        parameters = analysis
        prompt = self.EXTRACTION_PROMPT.format(
            parameters=json.dumps(parameters, indent=2),
            document=document_text[:8000]
        )
        
        return LLMAdapter().query(
            system_prompt="You are a precise financial data extractor",
            user_prompt=prompt,
            temperature=0.1
        )