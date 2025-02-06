import pdfplumber
from pathlib import Path
import json

def load_term_sheet(file_path: str) -> str:
    """
    Load and extract text from a term sheet PDF document
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Term sheet not found at: {file_path}")
    
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    
    return "\n".join(text)

def save_result(data: dict, output_path: str) -> None:
    """
    Save payment results to JSON file
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)