import pytesseract
import os
from openai import OpenAI

def extract_text(image):
    return pytesseract.image_to_string(image)

def extract_structured_data(raw_text):
    client = OpenAI()
    
    # Simple prompt to structure the receipt text
    prompt = f"""
You are an intelligent assistant. Structure the following receipt text into JSON format:
{raw_text}
Return raw JSON with: store name, date, list of items (name + price), and total.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}