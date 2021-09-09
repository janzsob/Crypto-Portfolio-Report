import pandas as pd
from fpdf import FPDF


def generating_pdf():
    # loading dataframe
    df = pd.read_excel('portfolio.xlsx')

    TABLE_COL_NAMES = list(df.columns) 
    TABLE_DATA = []
    for index, rows in df.iterrows():
        row_list = [pd.Timestamp(rows['Dátum']).strftime("%Y/%m/%d") , f"${str(rows.Ethereum)}", f"${str(rows.BNB)}", f"${str(rows.Cardano)}", f"${str(rows.XRP)}", f"${str(rows['1inch'])}"]
        TABLE_DATA.append(row_list)

    # creatinf pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    line_height = pdf.font_size * 2
    

    """ Page1: portfolio composition """
    # page title
    pdf.set_margins(left=40, top=0, right=40)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 20, "Portfolió összetétele", ln=1, align="C")

    # table about composition
    # header
    col_table_names = ["Valuták", "Mennyiség (db)"]
    pdf.set_font(style="B", size=14)
    col_width = pdf.epw / 2
    for title in col_table_names:
        pdf.cell(col_width, line_height, title, border=1, align="C")

    pdf.ln(line_height) # break
    pdf.set_font(style="")  # disabling bold text

    # table body
    table_content = []
    df = pd.read_excel('portfolio.xlsx', "Mennyiség")
    
    for index, rows in df.iterrows():
        row_list = [rows[0], str(rows[1])]
        table_content.append(row_list)

    # create table body
    for row in table_content:
        for item in row:
            pdf.set_font("Times", size=14)
            pdf.cell(col_width, line_height, item, border=1, align="C")
        pdf.ln(line_height)
    
    # portfolio value
    # title 
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 25, "Portfolió aktuális értéke", ln=1, align="C")

    # table
    pdf.set_margins(left=50, top=0, right=50)
    df = pd.read_excel('portfolio.xlsx', "Érték")
    current_value = f"${str(df.iloc[-1,1])}" # extract portfolio value from the last row.
    current_date = pd.Timestamp(df.iloc[-1,0]).strftime("%Y/%m/%d")
    
    pdf.set_font("Times", style="B", size=14)
    col_width = pdf.epw / 2
    pdf.set_fill_color(37, 196, 49)  # background color
    pdf.cell(col_width, line_height, current_date, border=1, align="C")
    pdf.cell(col_width, line_height, current_value, border=1, align="C", fill=True)


    """ Page2: list of prices """
    # title for table
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 25, "Árak heti bontásban", ln=1, align="C")
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