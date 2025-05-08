# 🧾 AI-Powered Receipt Scanning Tool

This project is a final-year Computer Science dissertation at Sheffield Hallam University. It is an AI-powered receipt scanning tool built in Python that automates expense tracking by extracting and structuring receipt data from images received via email and Google Drive, then uploads the data to Azure IoT Hub.

Additionally, data is stored in an Azure SQL database and exported to CSV for further analysis.

---

## 📌 Project Summary

The goal of this tool is to simplify receipt tracking and expense logging. Users can send receipt images either by uploading to Google Drive or by emailing them to a dedicated inbox. The system automatically downloads the images, extracts text, parses it into structured data using GPT, and sends the information to Azure IoT Hub.

Additionally, data is stored in an Azure SQL database and exported to CSV for further analysis.

---

## 🔧 Key Features

- 📨 **Email Integration** – Downloads receipt images sent to a Gmail inbox
- ☁️ **Google Drive Sync** – Grabs new receipt images from a specified folder
- 🔍 **OCR with Tesseract** – Extracts raw text from receipts
- 🧠 **Data Structuring via GPT** – Converts text into structured JSON format
- 📤 **Azure IoT Hub Integration** – Sends processed data to the cloud
- 📝 **Local JSON Storage** – Saves structured receipts in local `.json` format
- 🔧 **Email Reports** - Spending reports and graphs sent via email
- 📊 **CSV Export** – Automatically exports all data to a CSV file from Azure SQL

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
│   ├── image_processor.py           # OpenCV preprocessing
│   ├── receipt_parser.py            # Tesseract OCR + GPT structuring
│   ├── gdrive_sync.py               # Google Drive sync and monitoring
│   ├── email_fetcher.py             # Email Input
│   ├── iot_sender.py                # Link to Azure IoT Hub
│   ├── email_reporter.py            # Email Reports
│   └── db_exporter.py               # Export data to CSV from Azure SQL
│   └── autonomous_runner.py         # Runs Application Autonomusley
└── README.md

---

## 🚀 How It Works

1. Checks Gmail inbox for new `.jpg/.png` receipt attachments  
2. Syncs a specified Google Drive folder for any new receipt uploads  
3. Preprocesses the image (grayscale, thresholding)  
4. Uses OCR to extract raw text from the receipt  
5. Sends the text to GPT to generate structured JSON data  
6. Saves the JSON to the `results/` folder  
7. Sends the data to Azure IoT Hub  
8. Sends a summarized report with charts via email  
9. Exports all structured data to a CSV file from the Azure SQL database

---

## 🔐 .env Configuration

OPENAI_API_KEY=your_openai_key_here
IOTHUB_CONNECTION_STRING=your_azure_iot_hub_connection_string
EMAIL_USER=your_receiving_gmail_address
EMAIL_PASS=your_gmail_app_password (generated via Google App Passwords)

---

## 📨 Email-Based Input

	•	Send an email to your configured Gmail inbox
	•	The system will download any .jpg, .jpeg, or .png attachments
	•	Each will be processed automatically

---

## 🔗 Azure IoT Hub Integration

The structured receipt data is sent to Azure IoT Hub where it can later be:
	•	Streamed into Azure SQL or Cosmos DB
	•	Visualized via Power BI
	•	Used to trigger alerts or automation

---

## 📬 Author

Jack Kong
Sheffield Hallam University – BSc Computer Science
2025 Dissertation Project