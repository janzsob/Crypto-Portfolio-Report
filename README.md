# Automatic reporting about a crypto portfolio
The script creates a pdf report about the value and composition of a crypto portfolio and sends it via email.

It is running on AWS Lambda to automate the report generation, but the script can also be used locally.

The purpose of this project is to be able to share the performance of a portfolio with third parties.

## Functionality
The current crypto prices are collected by CoinGecko API wrapper (https://github.com/man-c/pycoingecko) and are saved in an excel file.

The most relevant details about the portfolio must be recorded in advance in the mentioned excel file.

Based on data in the excel a pdf report is generated that consists of the following:
* Portfolio composition
* Invested amount vs current value of the portfolio
* A Chart about the historic changes in portfolio value
* Collected historic prices in a table

The pdf is sent via email after the report generation is done.

## Technologies
The project was made purely in python 3.9. Main python libraries:
* Pandas and Openpyxl: to read and write excel file.
* fpdf2: to generate a pdf file with tables, diagrams and some texts.
* Matplotlib: to create a chart that shows the historical changes in portfolio value. The chart is inserted in the pdf file.
* email package: to send the report via email


The script can also be run manually, but there is a lambda function that was created to run automatically on AWS.

