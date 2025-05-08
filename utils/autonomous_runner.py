import time
import os
import sys
from imap_tools import MailMessageFlags
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main 

def has_new_files(receipt_folder="receipts"):
    # Check if any .jpg files exist that haven't been processed
    return any(f.endswith('.jpg') for f in os.listdir(receipt_folder))

def run_autonomously(poll_interval=60):  # check every 60 seconds
    print("[*] Autonomous runner started...")

    while True:
        print("[*] Checking for new receipts...")

        download_email_receipts()  # fetch unread emails

        if has_new_files():
            print("[*] New receipt found! Running main...")
            main()
            cleanup_drive_folder(folder_id="1KY4B9zWYuT0jn2CXC-b2SIGpnJfaPQrR")
        else:
            print("[*] No new receipts. Sleeping...\n")

        time.sleep(poll_interval)

if __name__ == "__main__":
    run_autonomously()