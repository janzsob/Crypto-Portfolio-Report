import os
import smtplib
from email.message import EmailMessage


def send_email():
    email_address = os.environ.get("EMAIL")
    email_password = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = "Test email wit excel."
    msg['From'] = email_address
    msg['To'] = [email_address]

    msg.set_content("Hello, test email with excel file attachment.")


    with open("portfolio.xlsx", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
