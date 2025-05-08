import smtplib
import matplotlib.pyplot as plt
import io
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from utils.db_exporter import export_sql_to_csv
import os

load_dotenv()

def generate_chart_image(items):
    names = []
    prices = []

    for item in items:
        name = item.get("name") or item.get("description", "Unknown Item")
        raw_price = (
            item.get("price") or
            item.get("discounted_price") or
            item.get("total_price") or
            item.get("price_total") or
            0
        )
        try:
            price = float(str(raw_price).replace("£", "").strip())
            if price > 0:
                names.append(name)
                prices.append(price)
        except ValueError:
            continue

    if not prices:
        print("⚠️ No valid prices to generate chart.")
        return None

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

def send_email_report(receipt_data, image_path=None):
    sender = os.getenv("EMAIL_USER")        
    password = os.getenv("EMAIL_PASS")      
    recipient = "c2079617@hallam.shu.ac.uk" # recipiant email

    msg = MIMEMultipart("related")
    msg["Subject"] = f"Receipt Summary - {receipt_data['storeName']}"
    msg["From"] = sender
    msg["To"] = recipient

    # Generate chart
    chart_base64 = generate_chart_image(receipt_data["items"])

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #2F4F4F;">🧾 Receipt Summary</h2>
            <p><b>🛒 Store:</b> {receipt_data['storeName']}</p>
            <p><b>📅 Date:</b> {receipt_data['receiptDate']}</p>
            <p><b>💰 Total Spent:</b> £{receipt_data['totalSpent']:.2f}</p>
            <p><b>📦 Item Count:</b> {receipt_data['itemCount']}</p>

            <h3 style="margin-top:20px;">🛍️ Items Purchased</h3>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
                <tr style="background-color: #f2f2f2;">
                    <th>Item</th>
                    <th>Price</th>
                </tr>
                {''.join(f"<tr><td>{item.get('name', item.get('description', 'Unknown'))}</td><td>£{item.get('price', item.get('discounted_price', item.get('total_price', item.get('price_total', '0'))))}</td></tr>" for item in receipt_data["items"])}
            </table>

            <h3 style="margin-top:20px;">📊 Spending Breakdown</h3>
            <img src="cid:chartimage" alt="Receipt Chart" style="width: 100%; max-width: 500px; border: 1px solid #ccc;">

            {"<h3 style='margin-top:20px;'>🖼️ Receipt Image</h3><img src='cid:receiptimage' alt='Receipt Image' style='width:100%; max-width:500px; border: 1px solid #ccc;'>" if image_path else ""}
        </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    image_data = base64.b64decode(chart_base64)
    image = MIMEImage(image_data, name="chart.png")
    image.add_header("Content-ID", "<chartimage>")
    msg.attach(image)

    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            receipt_img = MIMEImage(img_file.read(), name=os.path.basename(image_path))
            receipt_img.add_header("Content-ID", "<receiptimage>")
            msg.attach(receipt_img)

    # Generate and attach the CSV export
    csv_path = export_sql_to_csv()
    if os.path.exists(csv_path):
        with open(csv_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(csv_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(csv_path)}"'
            msg.attach(part)
        os.remove(csv_path)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    print("📧 Email report sent to jackkongjack@gmail.com")