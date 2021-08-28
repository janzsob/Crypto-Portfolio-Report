from prices import append_data
from send_email import send_email

# Appending current crypto prices in a new row in portfolio.xlsx
append_data()

# Sending email with excel attachment
send_email()