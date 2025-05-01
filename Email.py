import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def email(address, subject, body):
    # Get credentials from the environment
    from_email = os.getenv("OUTLOOK_EMAIL")
    password = os.getenv("OUTLOOK_APP_PASSWORD")

    if not from_email or not password:
        print("Error: Please set the OUTLOOK_EMAIL and OUTLOOK_APP_PASSWORD in the .env file.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = address

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            smtp.starttls()  # Upgrade to secure connection
            smtp.login(from_email, password)
            smtp.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
