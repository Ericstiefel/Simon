import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def email(address, subject, body):
    # Get Gmail credentials from the environment
    from_email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")  

    if not from_email or not password:
        print("Error: Please set the GMAIL_EMAIL and GMAIL_APP_PASSWORD (or GMAIL_PASSWORD) in the .env file.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = address

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:  # Use SMTP_SSL for port 465
            smtp.login(from_email, password)
            smtp.send_message(msg)
            print("Email sent successfully via Gmail.")
    except Exception as e:
        print(f"Error sending email via Gmail: {e}")

# Example usage remains the same
email('ericslide318@gmail.com', 'check', 'This worked via Gmail')