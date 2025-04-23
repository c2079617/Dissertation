from utils.gdrive_sync import authenticate_drive, download_files_from_folder
from utils.image_processor import preprocess_image
from utils.receipt_parser import extract_text, extract_structured_data
import os

def main():
    # Step 1: Authenticate with Google Drive and download any new receipt images
    folder_id = "1KY4B9zWYuT0jn2CXC-b2SIGpnJfaPQrR"
    service = authenticate_drive()
    download_files_from_folder(service, folder_id)

    # Step 2: Look through the local 'receipts' folder for all .jpg files
    receipt_folder = "receipts"
    files = [f for f in os.listdir(receipt_folder) if f.endswith('.jpg')]
    
    if not files:
        print("No receipt images found.")
        return

    # Step 3: Go through each image file one by one
    for file_name in files:
        print(f"\n[*] Processing: {file_name}")
        image_path = os.path.join(receipt_folder, file_name)

        # Step 4: Make the image easier for the OCR to read
        print("[*] Preprocessing image...")
        processed_image = preprocess_image(image_path)

        # Step 5: Use OCR to extract raw text from the receipt
        print("[*] Extracting text from image...")
        raw_text = extract_text(processed_image)
        print("Extracted text:\n", raw_text)

        # Step 6: Send the text to GPT to convert it into structured receipt data
        print("[*] Sending to GPT for structuring...")
        structured_data = extract_structured_data(raw_text)
        print("Structured data:\n", structured_data)

if __name__ == "__main__":
    main()