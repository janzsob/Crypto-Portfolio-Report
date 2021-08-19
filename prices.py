from pycoingecko import CoinGeckoAPI
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table

# Collect the current prices by CoinGecko API
cg = CoinGeckoAPI()
data = cg.get_price(ids='ethereum, binancecoin, cardano, ripple, vechain, 1inch', vs_currencies='usd')


# """Creating an excel from the gathered data"""
# now = datetime.now()
# today = now.strftime("%Y/%m/%d") 

# # workbook
# wb = Workbook()
# # worksheet
# ws = wb.active
# ws.title = "Árak"

# # add column headings. NB. these must be strings
# ws.append(["Dátum", "Ethereum", "BNB", "Cardano", "XRP", "VET", "1inch"])

# # appending data from coingecko api
# data = [
#     [
#     today, data['ethereum']['usd'], 
#     data['binancecoin']['usd'], 
#     data['cardano']['usd'], 
#     data['ripple']['usd'], 
#     data['vechain']['usd'], 
#     data['1inch']['usd']
#     ],
# ]

# for row in data:
#     ws.append(row)

# # Creating table
# table = Table(displayName="Crypto_prices", ref="A1:G2")

# ws.add_table(table)
# wb.save("portfolio.xlsx")

""" Loading workbook thean appending data in new row """
wb = load_workbook("portfolio.xlsx")
ws = wb.worksheets[0]

now = datetime.now()
today = now.strftime("%Y/%m/%d") 


ws.append([
    today, data['ethereum']['usd'], 
    data['binancecoin']['usd'], 
    data['cardano']['usd'], 
    data['ripple']['usd'], 
    data['vechain']['usd'], 
    data['1inch']['usd']
    ])

for table in ws.tables.values():
    if table.name == "Crypto_prices":
        table.ref = f"A1:G{ws.max_row}"
    #print(table.name)
    #print(table.ref)


wb.save("portfolio.xlsx")