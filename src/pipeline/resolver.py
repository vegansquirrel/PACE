from src.adapters.vector_db import VectorDB

class DocumentResolver:
    def __init__(self):
        self.vector_db = VectorDB()
        
    def resolve_missing(self, term_sheet_map, prospectus_text):
        queries = self._generate_queries(term_sheet_map)
        results = self.vector_db.search(
            queries=queries,
            context=prospectus_text
        )
        return self._merge_findings(results)
    
    def _generate_queries(self, conceptual_map):
        return [
            f"{comp['type']} {comp['description']}"
            for comp in conceptual_map['payment_components']
        ]