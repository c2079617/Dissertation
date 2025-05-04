import time
import os
from main import main  # this is your existing main() function

def has_new_files(receipt_folder="receipts"):
    # Check if any .jpg files exist that haven't been processed
    return any(f.endswith('.jpg') for f in os.listdir(receipt_folder))

def run_autonomously(poll_interval=60):  # check every 60 seconds
    print("[*] Autonomous runner started...")

    while True:
        print("[*] Checking for new receipts...")
        if has_new_files():
            print("[*] New receipt found! Running main...")
            main()
        else:
            print("[*] No new receipts. Sleeping...\n")

        time.sleep(poll_interval)

if __name__ == "__main__":
    run_autonomously()