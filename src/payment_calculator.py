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
    principal = terms["principal"]["amount"]
    currency = terms["principal"]["currency"]
    payment_terms = terms["payment_terms"]
    
    # Get initial price from term sheet
    initial_price = payment_terms["initial_level"]  # Added to payment_terms
    
    payment_due = 0
    conditions = []

    # 1. Check autocall triggers
    for date_str in payment_terms["observation_dates"]:
        if is_past_date(date_str):
            asset_price = prices[terms["underlying_assets"][0]["name"]]  # First asset
            if asset_price >= payment_terms["autocall_level"] * initial_price / 100:
                payment_due = principal * payment_terms["coupon_rate"]
                conditions.append(f"Autocall @ {date_str}")
                break  # Stop at first trigger

    # 2. If no autocall, check barrier at maturity
    if not conditions:
        final_price = prices[terms["underlying_assets"][0]["name"]]
        
        if final_price >= payment_terms["barrier_level"] * initial_price / 100:
            payment_due = principal
            conditions.append("Barrier condition met")
        else:
            payment_due = principal * (final_price / initial_price)
            conditions.append("Below barrier")

    return {
        "payment_due": round(payment_due, 2),
        "currency": currency,
        "conditions": conditions
    }