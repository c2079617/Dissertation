# Dissertation
# 🧾 AI-Powered Receipt Scanning Tool

This project is a final-year Computer Science dissertation at Sheffield Hallam University. It is an AI-powered receipt scanning tool that automates expense tracking by extracting and structuring receipt data from images stored in a synced Google Drive folder.

---

## 📌 Project Summary

The system watches a Google Drive folder for new receipt images. Once detected, each image is:
1. Downloaded locally
2. Preprocessed with OpenCV
3. Scanned using Tesseract OCR
4. Parsed and structured with GPT-4 into JSON format
5. Stored in a database for user-friendly tracking and reporting

---

## 🔧 Key Features

- ✅ Sync with Google Drive folder
- 📨 Email Integration — Automatically fetches receipt images from a Gmail inbox (supports attachments like .jpg/.png)
- 📸 Image preprocessing (grayscale, thresholding)
- 🔍 Text extraction via Tesseract OCR
- 🤖 Structured data creation using OpenAI's GPT
- 💾 Temporary local storage of images
- Integration with a web dashboard or database

---

## 🗂️ Project Structure

Dissertation/
├── main.py                          # Entry point
├── .env                             # Environment variables (API keys, etc.)
├── credentials.json                 # Google API OAuth credentials (downloaded from Google)
├── requirements.txt                 # Python dependencies
├── receipts/                        # Folder to store temporarily downloaded receipt images
│   └── sample.jpg
├── utils/                           # Helper modules
│   ├── image_processor.py          # OpenCV preprocessing
│   ├── receipt_parser.py           # Tesseract OCR + GPT structuring
│   └── gdrive_sync.py              # Google Drive sync and monitoring
└── README.md

## 🚀 How It Works

1. The user sends a photo of a receipt.
2. The image is preprocessed (grayscale, thresholding) using OpenCV.
3. Tesseract OCR extracts the text from the receipt.
4. The raw text is sent to GPT-4 to be structured as JSON data.
