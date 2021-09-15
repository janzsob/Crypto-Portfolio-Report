import pandas as pd
import matplotlib.pyplot as plt


def create_chart():
    df = pd.read_excel("portfolio.xlsx", "Érték")

    # columns of dates and portfolio value
    dates_vs = df['Dátum']
    values = df['Portfolió Érték']

    # It defines the style of figure
    plt.style.use('seaborn-darkgrid')

    plt.plot_date(dates_vs, values, linestyle='solid')

    # It rotates and formats dates on x axis
    plt.gcf().autofmt_xdate()

    #plt.title("Portfolió Értékének Alakulása")
    plt.ylabel("Portfolió Értéke (USD)")

    # Adjusts the padding
    plt.tight_layout()

    # it displays the figure
    #plt.show()

    # it saves the figure in png
    plt.savefig("chart.png")

#create_chart()