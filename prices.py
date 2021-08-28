from pycoingecko import CoinGeckoAPI
from datetime import datetime, date
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table

def creating_file():
    # Using Coingecki API
    cg = CoinGeckoAPI()
    data = cg.get_price(ids='ethereum, binancecoin, cardano, ripple, vechain, 1inch', vs_currencies='usd')

    now = datetime.now()
    today = now.strftime("%Y/%m/%d") 

    # workbook
    wb = Workbook()
    # worksheet
    ws = wb.active
    ws.title = "Árak"

    # add column headings. NB. these must be strings
    ws.append(["Dátum", "Ethereum", "BNB", "Cardano", "XRP", "VET", "1inch"])

    # appending data from coingecko api
    data = [
        [
        today, data['ethereum']['usd'], 
        data['binancecoin']['usd'], 
        data['cardano']['usd'], 
        data['ripple']['usd'], 
        data['vechain']['usd'], 
        data['1inch']['usd']
        ],
    ]

    for row in data:
        ws.append(row)

    # Creating table
    table = Table(displayName="Crypto_prices", ref="A1:G2")

    ws.add_table(table)
    wb.save("portfolio.xlsx")

""" Collecting historical data and append it in a file"""
def gather_historic_data(date_request):
    cg = CoinGeckoAPI()

    # collecting prices
    request_eth = cg.get_coin_history_by_id(id="ethereum", date=date_request, localization=False)
    eth = request_eth['market_data']['current_price']['usd']
    
    request_bnb = cg.get_coin_history_by_id(id="binancecoin", date=date_request, localization=False)
    bnb = request_bnb['market_data']['current_price']['usd']
    
    request_ada = cg.get_coin_history_by_id(id="cardano", date=date_request, localization=False)
    ada = request_ada['market_data']['current_price']['usd']
    
    request_xrp = cg.get_coin_history_by_id(id="ripple", date=date_request, localization=False)
    xrp = request_xrp['market_data']['current_price']['usd']
    
    request_vet = cg.get_coin_history_by_id(id="vechain", date=date_request, localization=False)
    vet = request_vet['market_data']['current_price']['usd']
    
    request_1inch = cg.get_coin_history_by_id(id="1inch", date=date_request, localization=False)
    inch = request_1inch['market_data']['current_price']['usd']

    # loading excel file
    wb = load_workbook("portfolio.xlsx")
    ws = wb.worksheets[0]

    day = int(date_request[0:2])
    if date_request[3] == '0':
        month = int(date_request[4])
    else:
        month = int(date_request[3:5])
    year = int(date_request[6:11])
    date_append = date(year, month, day) 

    ws.append([date_append, round(eth, 0), round(bnb, 0), round(ada, 2), round(xrp, 2), round(vet, 4), round(inch, 2)])

    for table in ws.tables.values():
        if table.name == "Árak":
            table.ref = f"A1:G{ws.max_row}"
    
    wb.save("portfolio.xlsx")


""" Loading workbook then appending data in new row """
def append_data():
    # Collect the current prices by CoinGecko API
    cg = CoinGeckoAPI()
    data = cg.get_price(ids='ethereum, binancecoin, cardano, ripple, vechain, 1inch', vs_currencies='usd')

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
        if table.name == "Árak":
            table.ref = f"A1:G{ws.max_row}"
        #print(table.name)
        #print(table.ref)


    wb.save("portfolio.xlsx")


#gather_historic_data('22-08-2021')
