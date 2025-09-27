import imaplib
import email
from email.header import decode_header
import re
import time

# Email credentials
# PRIMARY_EMAIL = "Rothy1122@yandex.com"  # Use your primary email for login
# PASSWORD = "jxlnuqhctvarttkh"  # Use the same password as your primary email
PRIMARY_EMAIL = "n3w.mmo@yandex.com"  # Use your primary email for login
PASSWORD = "wkhjqdqgqnczdebn"  # Use the same password as your primary email
IMAP_SERVER = "imap.yandex.com"
IMAP_PORT = 993

def get_facebook_otp(alias_email):
    """
    Fetch Facebook OTP from Yandex Mail for the given alias email.
    Returns the OTP if found, otherwise returns None.
    """
    try:
        # Connect to Yandex Mail using primary email credentials
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(PRIMARY_EMAIL, PASSWORD)  # Log in with primary email credentials
        
        # Select the correct folder (INBOX)
        mail.select("INBOX")
        
        # Senders to check for OTP emails
        senders = ["facebookmail.com", "security@facebookmail.com"]

        # Search emails from these senders directed to the alias email
        for sender in senders:
            status, messages = mail.search(None, f'(TO "{alias_email}" FROM "{sender}")')
            if status != 'OK':
                continue
            
            email_ids = messages[0].split()
            if not email_ids:
                print(f"No emails from {sender} to {alias_email}.")
                continue

            # Fetch the latest email (last email in the list)
            email_id = email_ids[-1]
            res, msg = mail.fetch(email_id, "(RFC822)")
            if res != 'OK':
                continue

            # Parse the email content
            msg = email.message_from_bytes(msg[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            
            print(f"Subject: {subject}")  # Debugging: Print the subject line

            # Search for OTP in the subject line (FB- followed by 5-6 digits)
            otp_match = re.search(r'(\d{5,6})', subject)
            if otp_match:
                otp = otp_match.group(1)
                print(f"OTP Found: {otp}")  # Debugging: Print found OTP
                return otp

        # If no OTP is found
        return None  # Return None if no OTP is found
    
    except imaplib.IMAP4.error as e:
        return f"IMAP Error: {e}"
    except Exception as e:
        return f"Error: {e}"
    
    finally:
        # Ensure logout from the mail server
        try:
            mail.logout()
        except Exception:
            print("Failed to logout from the mail server.")

def call_facebook_otp_function(alias_email):
    """
    This function calls `get_facebook_otp` to retrieve and display the OTP.
    """
    otp = get_facebook_otp(alias_email)
    return otp  # Only return the OTP code, not extra print statements

# Main loop to check for OTP
def check_for_otp(alias_email):
    elapsed_time = 0
    while elapsed_time < 120:  # Check for OTP for 2 minutes
        print("Checking for Facebook OTP...")
        
        # Call the function to check for OTP
        otp = call_facebook_otp_function(alias_email)
        
        # If OTP is found, stop the loop
        if otp and otp != "No OTP found in recent emails.":
            print(f"Facebook OTP Found: {otp}")
            return otp  # Stop the loop and return the OTP
        
        # Wait for 1 second before checking again
        time.sleep(1)  # Check every 1 second
        
        # Increment elapsed time
        elapsed_time += 1
    
    # If OTP is not found within 120 seconds
    print("OTP not found within 120 seconds.")
    return None  # Return None if no OTP was found in 120 seconds

# Example usage
# alias_email = "rothy1122+BrendaJones@yandex.com"
# otp = check_for_otp(alias_email)

# if otp:
#     print(f"Received OTP: {otp}")
# else:
#     print("No OTP received.")
