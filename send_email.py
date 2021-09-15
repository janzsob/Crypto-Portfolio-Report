import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()

def send_email():
    email_address = os.environ.get("EMAIL")
    email_password = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = "Heti crypto riport"
    msg['From'] = email_address
    msg['To'] = [os.getenv('recipients')]
    msg['Cc'] = [email_address]

    msg.set_content("Szia, \nKüldöm a heti jelentést a portfóliónkról.\nBence")


    with open("report.pdf", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

#send_email()