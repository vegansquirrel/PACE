from datetime import datetime

from datetime import datetime

def is_past_date(date_str: str) -> bool:
    """Check if a date (YYYY-MM-DD) has already occurred."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        return target_date.date() < datetime.today().date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")

def parse_date(date_str: str) -> datetime:
    """Safely parse dates from term sheets."""
    formats = ["%Y-%m-%d", "%d %b %Y", "%B %d, %Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")

def calculate_payment(terms: dict, prices: dict) -> dict:
    initial_price = terms["payment_terms"]["initial_level"]  # e.g., 12.50 (real value)
    current_price = prices["Engie shares"]  # e.g., 15.88
    
    # Convert percentage-based barriers to absolute values
    autocall_level = initial_price * (terms["payment_terms"]["autocall_level"] / 100)
    barrier_level = initial_price * (terms["payment_terms"]["barrier_level"] / 100)
    
    # Calculate performance
    performance = (current_price - initial_price) / initial_price
    
    if current_price >= autocall_level:
        payment = terms["principal"]["amount"] * terms["payment_terms"]["coupon_rate"]
        trigger = "autocall"
    elif current_price >= barrier_level:
        payment = terms["principal"]["amount"]
        trigger = "barrier"
    else:
        payment = terms["principal"]["amount"] * (current_price / initial_price)
        trigger = "loss"
    
    return {
        "payment_due": round(payment, 2),
        "currency": terms["principal"]["currency"],
        "performance_pct": round(performance * 100, 2),
        "trigger": trigger
    }