# Add this at the top of main.py
import sys
from pathlib import Path
import json
# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Now import your modules
from src.document_processor import extract_text, parse_terms_with_gpt
from src.payment_calculator import calculate_payment
from config.config import DOCUMENT_PATHS
from src.market_data import fetch_market_data
from src.validation import validate_terms


import argparse


def save_text(content: str, filename: str):
    """
    Save a string to the `output/` folder as a text file.
    """
    out_path = Path("output") / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

def save_json(data, filename: str):
    """
    Save a dictionary (or list) to `output/` as a JSON file.
    """
    out_path = Path("output") / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
def run_pipeline(term_sheet_path: Path):
    # 1. Extract terms
    term_text = extract_text(term_sheet_path)
    terms = parse_terms_with_gpt(term_text)
    save_json(terms, "extracted_terms.json")  # For debugging
    
    # 2. Validate terms
    validate_terms(terms)
    
    # 3. Fetch market data
    prices = {}
    for asset in terms["underlying_assets"]:
        try:
            price = fetch_market_data(asset)
            prices[asset["name"]] = price  # Use asset name as key to avoid ticker mismatch
        except Exception as e:
            print(f"Critical error for {asset['name']}: {str(e)}")
            raise  # Stop pipeline if any critical asset is missing
    
    # 4. Validate all required prices exist
    required_assets = [a["name"] for a in terms["underlying_assets"]]
    missing = [name for name in required_assets if name not in prices]
    if missing:
        raise ValueError(f"Missing prices for: {', '.join(missing)}")
    
    # 4. Calculate payment
    result = calculate_payment(terms, prices)
    save_json(result, "payment_report.json")
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--term_sheet", type=Path, default=DOCUMENT_PATHS["term_sheet"])
    parser.add_argument("--prospectus", type=Path, default=DOCUMENT_PATHS["prospectus"])
    
    args = parser.parse_args()
    result = run_pipeline(args.term_sheet)
    print("Payment calculation complete:", result)