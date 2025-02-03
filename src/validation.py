from datetime import datetime

# validation.py
VALID_TICKERS = ["ENGIE.PA", "SAN.PA", "BNP.PA"]  # Common Euronext Paris tickers

def validate_ticker(asset: dict):
    if asset["ticker"] not in VALID_TICKERS:
        raise ValueError(f"Unrecognized ticker: {asset['ticker']}. Verify term sheet!")

def validate_terms(terms: dict) -> None:
    # Check for required keys
    required_keys = ["underlying_assets", "payment_terms", "principal"]
    for key in required_keys:
        if key not in terms:
            raise ValueError(f"Missing required key: {key}")
    
    if "initial_level" not in terms["payment_terms"]:
        raise ValueError("Missing initial_level in payment_terms")
    # Validate underlying assets
    for asset in terms["underlying_assets"]:
        if not asset.get("ticker"):
            raise ValueError(f"Asset {asset.get('name')} has no ticker!")
    
    # Validate observation dates
    for date_str in terms["payment_terms"].get("observation_dates", []):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")