import yfinance as yf
from yfinance import Ticker

def get_correct_ticker(asset: dict) -> str:
    """
    Convert asset info to a valid Yahoo Finance ticker.
    Handles cases like Euronext Paris (ENGIE.PA) and exchanges with suffixes.
    """
    ticker = asset.get("ticker", "").strip().upper()
    exchange = asset.get("exchange", "").strip().lower()

    # Known ticker corrections (e.g., ENGIE.PA vs ENGI.PA)
    corrections = {
        "euronext paris": {
            "ENGI": "ENGI.PA",  # ENGI FP in Bloomberg → ENGIE.PA in Yahoo
            "SAN": "SAN.PA"      # Société Générale example
        }
    }

    # Apply exchange-specific corrections
    if exchange in corrections:
        base_ticker = ticker.split(".")[0]  # Remove existing suffix if any
        if base_ticker in corrections[exchange]:
            return corrections[exchange][base_ticker]

    # Add exchange suffix if missing (e.g., Euronext → .PA)
    if exchange == "euronext paris" and "." not in ticker:
        return f"{ticker}.PA"
    
    return ticker

def fetch_market_data(asset: dict) -> float:
    """Get latest price with validation and retries."""
    ticker_symbol = get_correct_ticker(asset)
    
    try:
        yf_ticker = Ticker(ticker_symbol)
        hist = yf_ticker.history(period="1d", interval="1m")
        
        if hist.empty:
            raise ValueError(f"No data for {ticker_symbol} (may be delisted)")
            
        return hist["Close"].iloc[-1]
    
    except Exception as e:
        # Try Alpha Vantage as fallback
        try:
            return fetch_from_alphavantage(asset)
        except:
            raise ValueError(f"Failed {ticker_symbol}: {str(e)}")

def fetch_from_alphavantage(asset: dict) -> float:
    """Fallback API (requires API key)"""
    import requests
    API_KEY = "4AJTAJMPZJ0MHE7G"  # Get from https://www.alphavantage.co
    
    ticker = get_correct_ticker(asset)
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    
    response = requests.get(url).json()
    return float(response["Global Quote"]["05. price"])