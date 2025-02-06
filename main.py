from src.pipeline.conceptual_analysis import ConceptualAnalyzer
from src.pipeline.dynamic_extractor import DynamicExtractor
from src.pipeline.temporal_processing import TemporalProcessor
from src.pipeline.calculation_engine import CalculationEngine
from src.pipeline.validation import TermValidator

from src.utils.document_loader import load_term_sheet

def main():
    # Initialize components
    analyzer = ConceptualAnalyzer()
    extractor = DynamicExtractor()
    temporal = TemporalProcessor()
    calculator = CalculationEngine()
    validator = TermValidator()
    
    # Load document
    doc_text = load_term_sheet("input/term_sheet.pdf")
    
    # Process pipeline
    analysis = analyzer.analyze(doc_text)
    validator.validate_conceptual(analysis)
    
    extracted = extractor.extract(analysis, doc_text)
    validator.validate_extraction(extracted)
    
    dates = temporal.process_dates(extracted['dates'])
    market_data = MarketDataClient().fetch(extracted['underlyings'], dates)
    
    payment = calculator.execute(extracted, market_data)
    validator.validate_result(payment)
    
    save_result(payment, "output/payment_report.json")

if __name__ == "__main__":
    main()