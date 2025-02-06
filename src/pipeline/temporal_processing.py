from dateutil.parser import parse
from src.adapters.llm_adapter import LLMAdapter

class TemporalProcessor:
    DATE_PROMPT = """Convert these date descriptions to ISO-8601 format:
{date_text}

Rules:
1. Handle business day conventions
2. Adjust for holidays if mentioned
3. Preserve date relationships

Return JSON with:
- original_description
- iso_date
- date_type
- adjustments_applied"""

    def process_dates(self, date_descriptions):
        processed = []
        for desc in date_descriptions:
            response = LLMAdapter().query(
                system_prompt="You are an expert date parser",
                user_prompt=self.DATE_PROMPT.format(date_text=desc)
            )
            processed.append(self._validate_date(response))
        return processed