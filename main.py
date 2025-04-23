from utils.image_processor import preprocess_image
from utils.receipt_parser import extract_text, extract_structured_data
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    image_path = "receipts/test2.jpg"
    
    print("[*] Preprocessing image...")
    processed_image = preprocess_image(image_path)

    print("[*] Extracting text from image...")
    raw_text = extract_text(processed_image)
    print("Extracted text:\n", raw_text)

    print("[*] Sending to GPT for structuring (simulated)...")
    structured_data = extract_structured_data(raw_text)
    print("Structured data:\n", structured_data)

if __name__ == "__main__":
    main()