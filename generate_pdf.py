import pandas as pd
from fpdf import FPDF
from datetime import date

def generating_pdf():
    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica', '', 14)
            # count weeks
            week_count = date.today().strftime("%V")
            self.cell(0, 5, f"{week_count}. hét, Crypto riport", border=0, align='L')
            # date
            today = date.today().strftime("%Y/%m/%d")
            self.cell(0, 5, today, border=0, align='R')
            # Line break
            self.ln(15)

    # loading dataframe
    df = pd.read_excel('portfolio.xlsx')

    TABLE_COL_NAMES = list(df.columns) 
    TABLE_DATA = []
    for index, rows in df.iterrows():
        row_list = [pd.Timestamp(rows['Dátum']).strftime("%Y/%m/%d") , f"${str(rows.Ethereum)}", f"${str(rows.BNB)}", f"${str(rows.Cardano)}", f"${str(rows.XRP)}", f"${str(rows['1inch'])}"]
        TABLE_DATA.append(row_list)

    # creating pdf
    pdf = PDF()
    # default format for FPDF is A4
    # dimensions of A4: widt=210mm height=297mm
    pdf.add_page()
    pdf.set_font("Times", size=14)
    line_height = pdf.font_size * 2
    

    """ Page1: portfolio composition """
    # portfolio value and invested amount
    pdf.set_margins(left=50, top=10, right=50)

    df = pd.read_excel('portfolio.xlsx', "Érték")
    current_value = f"${str(df.iloc[-1,1])}" # extract portfolio value from the last row.    
    invested_amount = round(df.iloc[0, 2])

    # building table
    pdf.set_font('helvetica', 'B', 14)
    col_width = pdf.epw / 2
    pdf.cell(col_width, line_height, "Befektetett összeg", border=0, align="C")
    pdf.cell(col_width, line_height, "Portfolió értéke", border=0, ln=1, align="C")
    
    pdf.set_font("Times", style="B", size=14)
    pdf.set_fill_color(252, 3, 3)  # background color
    pdf.cell(col_width, line_height, f"${invested_amount}", border=1, align="C", fill=True)
    pdf.set_fill_color(37, 196, 49)  # background color
    pdf.cell(col_width, line_height, current_value, border=1, align="C", fill=True)

    pdf.ln(16) # break

    # table about portfolio composition
    # header
    col_table_names = ["Valuták", "Mennyiség (db)"]
    pdf.set_font('helvetica', 'B', 14)
    col_width = pdf.epw / 2
    pdf.cell(pdf.epw, line_height, "Portfolió összetétele", border=0, ln=1, align="C")
    for title in col_table_names:
        pdf.set_font('helvetica', 'B', 13)
        pdf.cell(col_width, line_height, title, border=1, align="C")

    pdf.ln(line_height) # break
    pdf.set_font(style="")  # disabling bold text

    # table body
    table_content = []
    df = pd.read_excel('portfolio.xlsx', "Mennyiség")
    pdf.set_font("Times", style="B", size=14)
    for index, rows in df.iterrows():
        row_list = [rows[0], str(rows[1])]
        table_content.append(row_list)

    # create table body
    for row in table_content:
        for item in row:
            pdf.set_font("Times", size=13)
            pdf.cell(col_width, line_height, item, border=1, align="C")
        pdf.ln(line_height)
    
    pdf.ln(8) # break

    # Insert a chart about changes in portfolio value
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, line_height, "Portfolió értékének alakulása", ln=1, align="C")
    pdf.set_margins(left=10, top=10, right=10) # default marging dimensions
    pdf.ln()
    pdf.image("chart.png", x=5, y=135, w=210-10)


    """ Page2: list of prices """
    # title for table
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, line_height, "Árak heti bontásban", ln=1, align="C")
    pdf.set_margins(left=10, top=0, right=10)

    # header in table
    col_width = pdf.epw / 6  # distribute content evenly
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
    
    # save pdf
    pdf.output("report.pdf")

generating_pdf()