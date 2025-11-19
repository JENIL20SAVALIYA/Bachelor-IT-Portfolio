import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

e_mail = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASS")

def send_mail(email: str, message: str):
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = "Welcome to the Job Board!"
        msg["From"] = e_mail
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(e_mail, password)
            smtp.send_message(msg)

    except Exception as e:
        print(f"Email sending failed: {e}")
