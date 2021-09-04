from prices import append_data
from send_email import send_email
from generate_pdf import generating_pdf


# Appending current crypto prices in a new row in portfolio.xlsx
append_data()

# Generating a PDF file from data from portfolio.xlsx
generating_pdf()

# Sending email with pdf attachment
send_email()