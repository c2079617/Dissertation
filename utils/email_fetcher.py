from imap_tools import MailBox, AND, MailMessageFlags
import os

def download_email_receipts(download_folder="receipts/"):
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    with MailBox('imap.gmail.com').login(from_email, password) as mailbox:
        print("📬 Checking inbox for receipt images...")
        messages = mailbox.fetch(criteria=AND(seen=False))
        for msg in messages:
            downloaded = False
            for att in msg.attachments:
                if att.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(download_folder, att.filename)
                    print(f"📥 Downloading: {att.filename}")
                    with open(file_path, 'wb') as f:
                        f.write(att.payload)
                    downloaded = True

            # Only mark email as seen if a receipt was actually downloaded
            if downloaded:
                mailbox.flag(msg.uid, MailMessageFlags.SEEN, True)