# Dissertation
# 🧾 AI-Powered Receipt Scanning Tool

This project is a final-year Computer Science dissertation for Sheffield Hallam University. It is an AI-powered receipt scanning tool built in Python that automates expense tracking by extracting and structuring receipt data from images.

## 📌 Project Summary

The goal of this tool is to simplify the process of recording expenses by allowing users to simply take a photo of a receipt and send it via email. The system automatically processes the image, extracts important information such as the store name, items purchased, total amount, and stores this structured data in a database.

## 🔧 Key Features

- 📸 **Image Preprocessing** using OpenCV  
- 🔍 **Text Extraction** with Tesseract OCR  
- 🤖 **Structured Data Generation** using OpenAI’s GPT model  
- 🧠 Converts raw receipt text into JSON format (store, items, prices, total)  
- 💾 Data ready to be saved in a database or displayed on a dashboard  
- 📨 Future expansion: Email-to-cloud upload & message queue processing

## 🗂️ Project Structure

receipt-scanner/
├── main.py
├── .env
├── requirements.txt
├── utils/
│   ├── image_processor.py
│   └── receipt_parser.py
├── receipts/
│   └── sample.jpg

## 🚀 How It Works

1. The user sends a photo of a receipt.
2. The image is preprocessed (grayscale, thresholding) using OpenCV.
3. Tesseract OCR extracts the text from the receipt.
4. The raw text is sent to GPT-4 to be structured as JSON data.
5. (Planned) The structured data will be stored in a database for easy tracking.

## 🔐 Environment Variables

Create a `.env` file to store your OpenAI API key:
