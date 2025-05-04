from utils.gdrive_sync import authenticate_drive, download_files_from_folder
from utils.image_processor import preprocess_image
from utils.receipt_parser import extract_text, extract_structured_data
from utils.iot_sender import send_to_iot_hub, send_item_to_iot_hub
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
        print(f"\n📄 Processing '{file_name}'")  # show which file we're on
        image_path = os.path.join(receipt_folder, file_name)  # full path to the image

        processed_image = preprocess_image(image_path)  # use OpenCV to clean up image
        raw_text = extract_text(processed_image)  # use OCR to get plain text
        structured_data = extract_structured_data(raw_text)  # send to GPT to get structured data

        print("✅ OCR and structuring completed")

        # save GPT result as a raw .json file
        with open(f"results/{file_name.replace('.jpg', '.json')}", "w") as f:
            f.write(structured_data)

        if isinstance(structured_data, str):  # check if GPT returned a string
            import json
            structured_data = structured_data.strip().strip("```json").strip("```")  # clean triple backticks etc.
            raw_copy = structured_data
            try:
                structured_data = json.loads(structured_data)  # convert to dict
            except json.JSONDecodeError as e:
                print("❌ Could not parse structured JSON:", e)
                continue  # skip this receipt if it fails
            structured_data["rawJson"] = raw_copy  # store original
        else:
            raw_copy = structured_data.get("rawJson", "")

        # now build a version of the data that matches our schema
        cleaned_data = {
            "storeName": structured_data.get("storeName") or structured_data.get("store_name") or structured_data.get("store name"),
            "receiptDate": structured_data.get("date"),
            "totalSpent": float(str(structured_data["total"].get("total_amount", "0")).replace("£", "").strip()) if isinstance(structured_data.get("total"), dict) else float(str(structured_data.get("total", "0")).replace("£", "").strip()),
            "itemCount": len(structured_data.get("items", [])),
            "rawJson": raw_copy
        }

        send_to_iot_hub(cleaned_data)  # send main receipt info

        # send each item to IoT Hub separately
        for item in structured_data.get("items", []):
            try:
                clean_price = float(str(item.get("price", "0")).replace("£", "").strip())
            except:
                clean_price = 0.0

            item_payload = {
                "storeName": cleaned_data["storeName"],
                "receiptDate": cleaned_data["receiptDate"],
                "itemName": item.get("name"),
                "price": clean_price
            }

            send_item_to_iot_hub(item_payload)  # send this item to the item stream

        # cleanup - delete the file from disk now that we're done
        try:
            os.remove(image_path)
            print(f"🗑️ Deleted: {file_name}")
        except Exception as e:
            print(f"⚠️ Could not delete {file_name}")

if __name__ == "__main__":
    main()
