from utils.gdrive_sync import authenticate_drive, download_files_from_folder
from utils.image_processor import preprocess_image
from utils.receipt_parser import extract_text, extract_structured_data
from utils.iot_sender import send_to_iot_hub
from utils.email_fetcher import download_email_receipts
import os

def main():
    # Check inbox and download any new email receipt images
    download_email_receipts()

    # Authenticate with Google Drive and download any new receipt images
    folder_id = "1KY4B9zWYuT0jn2CXC-b2SIGpnJfaPQrR"
    service = authenticate_drive()
    download_files_from_folder(service, folder_id)

    # Look through the local 'receipts' folder for all .jpg files
    receipt_folder = "receipts"
    files = [f for f in os.listdir(receipt_folder) if f.endswith('.jpg')]
    
    if not files:
        print("No receipt images found.")
        return

    # Go through each image file one by one
    for file_name in files:
        print(f"\n[*] Processing: {file_name}")
        image_path = os.path.join(receipt_folder, file_name)

        # Make the image easier for the OCR to read
        print("[*] Preprocessing image...")
        processed_image = preprocess_image(image_path)

        # Use OCR to extract raw text from the receipt
        print("[*] Extracting text from image...")
        raw_text = extract_text(processed_image)
        print("Extracted text:\n", raw_text)

        # Send the text to GPT to convert it into structured receipt data
        print("[*] Sending to GPT for structuring...")
        structured_data = extract_structured_data(raw_text)
        print("Structured data:\n", structured_data)

        #Save structured_data
        with open(f"results/{file_name.replace('.jpg', '.json')}", "w") as f:
            f.write(structured_data)

        # Send the structured data to Azure IoT Central
        if isinstance(structured_data, str): 
            import json
            # Clean up GPT formatting like ```json and ```
            structured_data = structured_data.strip().strip("```json").strip("```")
            structured_data = json.loads(structured_data)

        send_to_iot_hub(structured_data)

if __name__ == "__main__":
    main()