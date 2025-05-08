import time
import os
import sys
from imap_tools import MailMessageFlags, MailBox, AND
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main 

def has_new_files(receipt_folder="receipts"):
    # Check if any .jpg files exist that haven't been processed
    return any(f.endswith('.jpg') for f in os.listdir(receipt_folder))

def has_unseen_emails():
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    with MailBox('imap.gmail.com').login(from_email, password) as mailbox:
        unseen_messages = list(mailbox.fetch(criteria=AND(seen=False), limit=1))
        return len(unseen_messages) > 0

def run_autonomously(poll_interval=60):  # check every 60 seconds
    print("[*] Autonomous runner started...")

    while True:
        print("[*] Checking for new unread emails...")
        if has_unseen_emails():
            print("[*] New unseen email(s) found! Running main...")
            main()
        else:
            print("[*] No new unread emails. Sleeping...\n")

        time.sleep(poll_interval)

if __name__ == "__main__":
    run_autonomously()