import json
import boto3
import pandas as pd
from openpyxl import load_workbook
from pycoingecko import CoinGeckoAPI
from datetime import date
from fpdf import FPDF
import os
import smtplib
from email.message import EmailMessage


s3 = boto3.client("s3")
bucket = "crypto-portfolio-bucket"
key = "portfolio.xlsx"

def lambda_handler(event, context):
    """ Collect new prices and append them in the excel file """
    # Download excel file from s3 bucket
    local_file = "/tmp/downloaded.xlsx"
    s3.download_file(bucket, key, local_file)
    
    # Make API call via to Coingeco for prices
    cg = CoinGeckoAPI()
    data = cg.get_price(ids='ethereum, binancecoin, cardano, ripple, vechain, 1inch', vs_currencies='usd')
    
    # Load excel by openpyxl
    wb = load_workbook("/tmp/downloaded.xlsx")
    ws = wb.worksheets[0]

    today = date.today() 

    # Append data in a new row
    ws.append([
        today, 
        round(data['ethereum']['usd'], 0), 
        round(data['binancecoin']['usd'], 0), 
        round(data['cardano']['usd'], 2), 
        round(data['ripple']['usd'], 2), 
        round(data['vechain']['usd'], 4), 
        round(data['1inch']['usd'], 2)
        ])
        
    for table in ws.tables.values():
        if table.name == "Árak":
            table.ref = f"A1:G{ws.max_row}"

    wb.save("/tmp/downloaded.xlsx")
    
    # Load back the excel file to s4 bucket
    s3.upload_file("/tmp/downloaded.xlsx", bucket, key)
    
    
    """ Generate PDF file """
    # load dataframe
    df = pd.read_excel('/tmp/downloaded.xlsx')

    TABLE_COL_NAMES = list(df.columns) 
    TABLE_DATA = []
    for index, rows in df.iterrows():
        row_list = [pd.Timestamp(rows['Dátum']).strftime("%Y/%m/%d") , f"${str(rows.Ethereum)}", f"${str(rows.BNB)}", f"${str(rows.Cardano)}", f"${str(rows.XRP)}", f"${str(rows.VET)}", f"${str(rows['1inch'])}"]
        TABLE_DATA.append(row_list)

    # create pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 7  # distribute content evenly

    # title for table
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 25, "Árak heti bontásban", ln=1, align="C")

    # header in table
    pdf.set_font(style="B", size=14)  # enabling bold text
    for col_name in TABLE_COL_NAMES:
        if col_name == "Dátum":
            pdf.cell(col_width, line_height, '', border=1, align="C")
        else:    
            pdf.cell(col_width, line_height, col_name, border=1, align="C")
    
    pdf.ln(line_height)
    pdf.set_font(style="")  # disabling bold text

    # table data
    for row in TABLE_DATA:
        for datum in row:
            pdf.set_font("Times", size=14)
            pdf.cell(col_width, line_height, datum, border=1, align="C")
        pdf.ln(line_height)
    
    pdf.output("/tmp/report.pdf")
    
    
    """ Send report via email """
    email_address = os.environ.get("EMAIL")
    email_password = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = "Email by Lambda"
    msg['From'] = email_address
    msg['To'] = [email_address]

    msg.set_content("Hello, test email by a Lambda function. You can find attached the requested report in PDF format.")


    with open("/tmp/report.pdf", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="report.pdf")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)