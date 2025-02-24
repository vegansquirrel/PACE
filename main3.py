import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None




def calculate_payment_with_gpt4(text):
    """Use GPT-4 to analyze text and calculate payment"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    external_data = """
Date	SOFR (%)
2025-01-10	4.35
2025-01-13	4.35
2025-01-14	4.35
2025-01-15	4.35
2025-01-16	4.35
2025-01-17	4.35
2025-01-21	4.35
2025-01-22	4.35
2025-01-23	4.35
2025-01-24	4.35
2025-01-27	4.35
2025-01-28	4.35
2025-01-29	4.35
2025-01-30	4.35
2025-01-31	4.35
2025-02-03	4.35
2025-02-04	4.33
2025-02-05	4.33
2025-02-06	4.36
2025-02-07	4.35
2025-02-10	4.35
Note: SOFR is published for business days; weekends and holidays are excluded."""

    prompt = """Analyze the document and calculate the payment amount that needs to be made. 
    Consider all relevant numerical values, due dates, and payment terms. 
    Provide the final payment amount as a numerical value. 
    Include brief reasoning before stating the final amount.
    
    Document Content:
    {content}
    
    This is all the external data you need to calculate the payment amount:
    {external_data}
    Provide Final payment amount:"""
    
    # USE this Information to calculate the payment amount.
    
    # This is all the External information you need to calculate the payment amount.
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial analyst. Analyze documents and calculate payments accurately."},
                {"role": "user", "content": prompt.format(content=text[:6000],external_data=external_data)}  # Truncate to fit context
            ],
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

if __name__ == "__main__":
    # Update with your PDF filename
    pdf_filename = "input3\Final-terms-Pricing-supplement-_2024-10-10.pdf"  # PDF in input folder
    
    if not os.path.exists(pdf_filename):
        print(f"Error: PDF file not found at {pdf_filename}")
    else:
        extracted_text = extract_text_from_pdf(pdf_filename)
        if extracted_text:
            print("Processing document...\n")
            result = calculate_payment_with_gpt4(extracted_text)
            if result:
                print("Payment Calculation Result:")
                print(result)
                output_path = "output3/payment_calculation_result.json"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w') as json_file:
                    json.dump({"result": result}, json_file, indent=4)
                print(f"Result saved to {output_path}")