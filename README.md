# SMTP Credential Verification

This script verifies the validity of SMTP credentials (email and password) using the Office 365 SMTP server. It uses multiple threads to perform the verification efficiently.

## Requirements

- Python 3.6 or higher
- Python modules:
  - `smtplib` (included in Python's standard library)
  - `concurrent.futures` (included in Python's standard library)
  - `logging` (included in Python's standard library)

## Installation

1. **Clone the repository or download the files.**

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

    Install dependencies (if any). In this case, there are no external dependencies to install.

Usage

    Prepare the credentials file.

    The text file should contain a list of credentials in the format email:password, one per line. For example:

    scss

test@example.com:password123
another@example.com:mysecurepassword

Save this file with a name, for example, smtp_credentials.txt.

Run the script:

Make sure the credentials file is in the same directory as the script or provide the correct path to the file.

bash

python main.py

Provide the credentials file when prompted.

plaintext

    Enter the SMTP TXT file: smtp_credentials.txt

    The script will process the credentials and display the results in the console. Valid emails will be marked in green, and invalid ones will be marked in red.

Configuration

You can adjust the following parameters in the code as needed:

    MAX_RETRIES: Maximum number of attempts to verify each credential.
    NUM_THREADS: Number of concurrent threads to process the credentials.
    RETRY_DELAY: Time to wait between retries in seconds.
    LOGIN_TIMEOUT: Maximum wait time for connecting to the SMTP server.

Signal Handling

The script handles interruption signals (Ctrl+C) to exit cleanly.
Troubleshooting

    File not found: Ensure that the credentials file exists and that the path provided is correct.
    Connection errors: Verify that the SMTP server is accessible and that the credentials are correct.

License

This project is licensed under the MIT License. See the LICENSE file for more details.
Contact

If you have questions or issues, you can contact the developer via [email or social media] (optional).

csharp


### Notes:
- Replace the placeholder for contact information with your actual details if you wish users to reach out to you.
- Include any additional information that you think is relevant for using or configuring the script.

Save this content in a file named `README.md` in the same directory as your script to provide clear and accessible documentation.