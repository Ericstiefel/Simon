import smtplib
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

def email(address, subject, body, filename="results.txt"):
    # Get Gmail credentials from the environment
    from_email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_PASSWORD")  

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = address
    msg.set_content(f"Please see attached file: {filename}")

    # Attach the .txt file (as bytes)
    msg.add_attachment(body.encode('utf-8'), 
                       maintype='text', 
                       subtype='plain', 
                       filename=filename)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, password)
            smtp.send_message(msg)
            print("Email sent successfully with attachment.")
    except Exception as e:
        print(f"Error sending email: {e}")
