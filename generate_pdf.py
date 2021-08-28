import pandas as pd
from fpdf import FPDF


def generating_pdf():
    # loading dataframe
    df = pd.read_excel('portfolio.xlsx')

    TABLE_COL_NAMES = list(df.columns) 
    TABLE_DATA = []
    for index, rows in df.iterrows():
        row_list = [pd.Timestamp(rows['Dátum']).strftime("%Y/%m/%d") , f"${str(rows.Ethereum)}", f"${str(rows.BNB)}", f"${str(rows.Cardano)}", f"${str(rows.XRP)}", f"${str(rows.VET)}", f"${str(rows['1inch'])}"]
        TABLE_DATA.append(row_list)

    # creatinf pdf
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
    pdf.output("report.pdf")

#generating_pdf()
