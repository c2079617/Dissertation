from utils.gdrive_sync import authenticate_drive, download_files_from_folder
from utils.image_processor import preprocess_image
from utils.receipt_parser import extract_text, extract_structured_data
from utils.iot_sender import send_to_iot_hub
from utils.email_fetcher import download_email_receipts
import os
from datetime import datetime

def main():
    folder_id = "1KY4B9zWYuT0jn2CXC-b2SIGpnJfaPQrR"  # ID of the Google Drive folder
    service = authenticate_drive()  # login to Google Drive
    download_files_from_folder(service, folder_id)  # grab any .jpgs from the folder

    receipt_folder = "receipts"  # our local folder where images are stored
    files = [f for f in os.listdir(receipt_folder) if f.endswith('.jpg')]  # only look for jpg files

    if not files:
        print("No receipt images found.")  # nothing to process, exit early
        return

    for file_name in files:  # go through each receipt
        print(f"\n[*] Processing: {file_name}")  # show which file we're on
        image_path = os.path.join(receipt_folder, file_name)  # full path to the image

        print("[*] Preprocessing image...")  # getting the image ready for OCR
        processed_image = preprocess_image(image_path)  # use OpenCV stuff

        print("[*] Extracting text from image...")  # now do OCR
        raw_text = extract_text(processed_image)  # get plain text
        print("Extracted text:\n", raw_text)  # print it out

        print("[*] Sending to GPT for structuring...")  # ask GPT to turn the text into a JSON receipt
        structured_data = extract_structured_data(raw_text)  # get that JSON response
        print("Structured data:\n", structured_data)  # display it

        with open(f"results/{file_name.replace('.jpg', '.json')}", "w") as f:
            f.write(structured_data)  # save what GPT gave us for later

        if isinstance(structured_data, str):  # sometimes GPT returns a string
            import json
            structured_data = structured_data.strip().strip("```json").strip("```")  # clean the formatting
            raw_copy = structured_data
            structured_data = json.loads(structured_data)  # turn string into dictionary
            structured_data["rawJson"] = json.dumps(structured_data)  # include full JSON for rawJson field
        else:
            raw_copy = structured_data.get("rawJson", "")

        # Build a clean version of the data to match our database schema
        cleaned_data = {
            "storeName": structured_data.get("storeName") or structured_data.get("store_name") or structured_data.get("store name"),
            "receiptDate": structured_data.get("date"),
            "totalSpent": float(str(structured_data.get("total", "0")).replace("£", "").strip()) if structured_data.get("total") else 0.0,
            "itemCount": len(structured_data.get("items", [])),
            "rawJson": raw_copy
        }

        send_to_iot_hub(cleaned_data)  # send the final cleaned receipt to the cloud

if __name__ == "__main__":
    main() 