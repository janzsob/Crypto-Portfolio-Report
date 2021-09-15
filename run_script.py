from prices import append_data
from send_email import send_email
from generate_pdf import generating_pdf
from chart import create_chart


# Appending current crypto prices in a new row in portfolio.xlsx
append_data()

# creating a chart about changes in portfolio value
create_chart()

# Generating a PDF file from data from portfolio.xlsx
generating_pdf()

# Sending email with pdf attachment
send_email()