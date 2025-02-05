from pathlib import Path
from config.config import DOCUMENT_PATHS, PROJECT_ROOT
from src.core.document_processor import DocumentProcessor
import json

def main():
    # Initialize components
    processor = DocumentProcessor()
    
    # Process document
    try:
        # 1. Extract text
        raw_text = processor.extract_text(DOCUMENT_PATHS["term_sheet"])
        
        # 2. Analyze with LLM
        analysis = processor.analyze_document(raw_text)
        
        # 3. Save preliminary results
        output_dir = PROJECT_ROOT / "output"
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "initial_analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)
            
        print("Initial analysis complete. Results saved to output/")
        
    except Exception as e:
        print(f"Processing failed: {str(e)}")

if __name__ == "__main__":
    main()