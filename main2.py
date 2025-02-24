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
    Observation Date	Closing Price (€)	Coupon Paid (€)
    July 17, 2024	8.71	15.84
    August 16, 2024	8.79	15.84
    September 16, 2024	8.52	15.84
    October 16, 2024	8.67	15.84
    November 18, 2024	8.82	15.84
    December 16, 2024	9.26	15.84
    January 16, 2025	9.94	15.84
    ]"""
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
                {"role": "user", "content": prompt.format(content=text[:3000],external_data=external_data)}  # Truncate to fit context
            ],
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

if __name__ == "__main__":
    # Update with your PDF filename
    pdf_filename = "input2\Final-terms-Pricing-supplement-_2024-02-08.pdf"  # PDF in input folder
    
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
                output_path = "output2/payment_calculation_result.json"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w') as json_file:
                    json.dump({"result": result}, json_file, indent=4)
                print(f"Result saved to {output_path}")