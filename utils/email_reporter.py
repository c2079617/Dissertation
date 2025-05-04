import smtplib
import matplotlib.pyplot as plt
import io
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

def generate_chart_image(items):
    names = [item["name"] for item in items]
    prices = [float(str(item["price"]).replace("£", "")) for item in items]

    plt.figure(figsize=(6, 6))
    plt.pie(prices, labels=names, autopct='%1.1f%%', startangle=140)
    plt.title('Spending Breakdown by Item')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode()
    buffer.close()
    plt.close()

    return encoded

def send_email_report(receipt_data):
    sender = os.getenv("EMAIL_USER")        
    password = os.getenv("EMAIL_PASS")      
    recipient = "jackkongjack@gmail.com"

    msg = MIMEMultipart("related")
    msg["Subject"] = f"Receipt Summary - {receipt_data['storeName']}"
    msg["From"] = sender
    msg["To"] = recipient

    # Generate chart
    chart_base64 = generate_chart_image(receipt_data["items"])

    html = f"""
    <html>
        <body>
            <h2>Receipt from {receipt_data['storeName']}</h2>
            <p><b>Date:</b> {receipt_data['receiptDate']}</p>
            <p><b>Total Spent:</b> £{receipt_data['totalSpent']:.2f}</p>
            <p><b>Item Count:</b> {receipt_data['itemCount']}</p>
            <h3>Items:</h3>
            <ul>
                {''.join(f"<li>{item['name']}: £{item['price']}</li>" for item in receipt_data["items"])}
            </ul>
            <h3>Visual Breakdown:</h3>
            <img src="cid:chartimage" alt="Receipt Chart" style="width: 100%; max-width: 500px;">
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    image_data = base64.b64decode(chart_base64)
    image = MIMEImage(image_data, name="chart.png")
    image.add_header("Content-ID", "<chartimage>")
    msg.attach(image)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    print("📧 Email report sent to jackkongjack@gmail.com")