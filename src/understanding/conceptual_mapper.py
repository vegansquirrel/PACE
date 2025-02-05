# src/understanding/conceptual_mapper.py
class ConceptualMapper:
    COT_PROMPT = """Analyze this financial document through these steps:
1. Identify the product category (e.g., autocallable, credit-linked note)
2. List all payment condition types present
3. Identify temporal dependencies (observation dates, maturity)
4. Determine required market data inputs
5. Map document sections to financial concepts

Document: {document_chunk}
Previous Thoughts: {previous_thoughts}

Generate JSON with:
- product_type
- payment_components
- temporal_events
- required_data
- concept_map
"""

    def build_conceptual_map(self, document):
        chunks = self._chunk_document(document)
        context = []
        for chunk in chunks:
            response = llm.invoke(
                self.COT_PROMPT.format(document_chunk=chunk, previous_thoughts=context[-3:]),
                response_format={"type": "json_object"}
            )
            context.append(json.loads(response))
        return self._consolidate_context(context)