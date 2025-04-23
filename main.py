from utils.gdrive_sync import authenticate_drive, download_files_from_folder
from utils.image_processor import preprocess_image
from utils.receipt_parser import extract_text, extract_structured_data
import os

def main():
    # Step 1: Authenticate and sync from Google Drive
    folder_id = "1KY4B9zWYuT0jn2CXC-b2SIGpnJfaPQrR"
    service = authenticate_drive()
    download_files_from_folder(service, folder_id)

    # Step 2: Pick the first image in the receipts folder
    receipt_folder = "receipts"
    files = [f for f in os.listdir(receipt_folder) if f.endswith('.jpg')]
    if not files:
        print("No receipt images found.")
        return

    image_path = os.path.join(receipt_folder, files[0])
    
    print("[*] Preprocessing image...")
    processed_image = preprocess_image(image_path)

    print("[*] Extracting text from image...")
    raw_text = extract_text(processed_image)
    print("Extracted text:\n", raw_text)

    print("[*] Sending to GPT for structuring...")
    structured_data = extract_structured_data(raw_text)
    print("Structured data:\n", structured_data)

if __name__ == "__main__":
    main()