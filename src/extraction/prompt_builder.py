# src/extraction/prompt_builder.py
import json
class ExtractionPromptBuilder:
    def generate_prompt(self, conceptual_map):
        requirements = conceptual_map['required_data']
        return f"""Extract EXACT values for these parameters:
{json.dumps(requirements, indent=2)}

Rules:
1. Maintain original units
2. Preserve numerical precision
3. Handle conditional logic
4. Cross-reference tables

Document Sections:
{conceptual_map['concept_map']}

Return JSON with:
- extracted_values
- verification_sources
- confidence_score
"""