from src.pipeline.conceptual_analysis import ConceptualAnalyzer
from src.pipeline.dynamic_extractor import DynamicExtractor
from src.pipeline.temporal_processing import TemporalProcessor
from src.pipeline.calculation_engine import CalculationEngine
from src.pipeline.validation import TermValidator



from src.utils.document_loader import load_term_sheet, save_result
from src.adapters.market_data import MarketDataFetcher

def main():
    # Initialize components
    analyzer = ConceptualAnalyzer()
    extractor = DynamicExtractor()
    temporal = TemporalProcessor()
    calculator = CalculationEngine()
    validator = TermValidator()
    
    # Load document
    doc_text = load_term_sheet("input/Final-terms-Pricing-supplement-_2024-02-08.pdf")
    
    # Process pipeline
    analysis = analyzer.analyze(doc_text)
    
    extracted = extractor.extract(analysis, doc_text)
    
    dates = temporal.process_dates(extracted)
    market_data = MarketDataFetcher().get_prices(extracted, dates)
    
    payment = calculator.execute(extracted, market_data)
    
    save_result(payment, "output/payment_report.json")

if __name__ == "__main__":
    main()