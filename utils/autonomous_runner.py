import time
import os
import sys
from imap_tools import MailMessageFlags, MailBox, AND
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main 

def has_unseen_emails():
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    with MailBox('imap.gmail.com').login(from_email, password) as mailbox:
        mailbox.folder.set('INBOX')
        unseen = list(mailbox.fetch(criteria=AND(seen=False), limit=1, mark_seen=False))
        return len(unseen) > 0

def run_autonomously(poll_interval=2):  # check every "_" seconds
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