# src/processing/cross_document.py
class CrossDocumentResolver:
    def __init__(self, vector_db):
        self.vector_db = vector_db
    
    def find_missing_terms(self, term_sheet, base_prospectus):
        # Create embeddings for key concepts
        query_embeddings = create_embeddings(term_sheet['missing_concepts'])
        
        # Search base prospectus
        results = self.vector_db.similarity_search(
            query_embeddings,
            document=base_prospectus
        )
        
        # Validate relevance
        return self._filter_results(results, term_sheet['product_type'])