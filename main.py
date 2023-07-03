"""
Create a script which will generate a report on Profit and loss statement of share market portfolio.
Get input from the user in csv file. Csv file will have 3 columns Company Name, Rate per share, quantity of share.
The script should make a call to BSE API and get the current/LTP (last trading prize) of that company share.
Get the mapping of company name and the BSE stock code from the
URL https://static.quandl.com/BSE+Descriptions/stocks.txt
Generate a statement of Profit and Loss as well calculate the deviation from purchase price to current price.
Log the data into another text file. The log data should contain the company name and day high price of that stock.
You an use pandas for this assignment and connect the file to database and also make a sender of excel file using
smtplib """

# For import the csv file, make a log file and export the data into excel file
import os.path
import pandas as pd
from bsedata.bse import BSE
import logging
from bsedata.exceptions import InvalidStockException

# For connecting the database
from database import connect_to_database

# For sending the file using e-mail ids
from mail import send_email


# Function for checking stock_code
def get_stock_code(company_name, stock_data):
    for code, name in stock_data.items():
        if name == company_name:
            return code
    return None


# Function for checking current price of stock
def get_current_price(stock_code, bse):
    try:
        stock_info = bse.getQuote(stock_code)
        current_price = stock_info['currentValue']
        high_price = stock_info['dayHigh']
        low_price = stock_info['dayLow']
        return current_price, high_price, low_price
    except InvalidStockException:
        return None, None, None


# Function for generating profit and loss in the stocks
def generate_profit_loss(csv_file):
    if not os.path.isfile(csv_file):
        logging.error(f'CSV file "{csv_file}" not found.')
        return
    df = pd.read_csv(csv_file)
    bse = BSE()
    stock_data = bse.getScripCodes()
    log_data = []

    # For making the log file for saving the data into log file
    logging.basicConfig(filename='profit_loss.log', level=logging.INFO, format='%(message)s')

    total_purchase_amount = 0
    total_current_amount = 0

    for index, row in df.iterrows():
        company_name = row['Company Name']
        rate_per_share = row['Rate per Share']
        quantity = row['Quantity']
        if pd.isna(quantity):
            logging.error(f"Invalid quantity value for company: {company_name}. Please check you CSV File")
            continue
        stock_code = get_stock_code(company_name, stock_data)
        if stock_code is None:
            logging.error(f'Stock code not found for company: {company_name}. Please check you csv file')
            continue

        current_prices, high_prices, low_prices = get_current_price(stock_code, bse)
        if current_prices is None:
            logging.error(f'Unable to fetch current price of company: {company_name}.')
            continue

        rate_per_share = float(rate_per_share)
        quantity = int(quantity)
        purchase_amount = rate_per_share * quantity
        current_amount = float(current_prices) * quantity
        deviation = current_amount - purchase_amount

        total_purchase_amount += purchase_amount
        total_current_amount += current_amount
        profit_loss_percentage = (deviation / purchase_amount) * 100

        logging.info(f'Company Name: {company_name}\n'
                     f'Deviation of Stocks: {deviation:.2f}\n'
                     f'Profit/Loss Percentage of Stocks: {profit_loss_percentage:.2f}%\n'
                     f'Current Stock Price(LTP): {current_prices}\n'
                     f'High Price of Stocks in a Day: {high_prices}\n'
                     f'Low Price of Stocks in a Day: {low_prices}\n')

        log_data.append([company_name, deviation, profit_loss_percentage, current_prices, high_prices, low_prices])

    overall_deviation = total_current_amount - total_purchase_amount
    overall_profit_loss_percentage = (overall_deviation / total_purchase_amount) * 100

    logging.info(f'Total Deviation of Stocks: {overall_deviation:.2f}\n'
                 f'Total Profit/Loss Percentage of Stocks: {overall_profit_loss_percentage:.2f}%\n')

    print(f'Report file generated successfully. Please check "profit_loss.log" for details.')

    # For exporting the data into excel file
    excel_file = 'log_data_file.xlsx'
    column_names = ['Company Name', 'Deviation of Stocks', 'Profit/Loss Percentage', 'Current Stock Price(LTP)',
                    'High Price', 'Low Price']
    df_export = pd.DataFrame(log_data, columns=column_names)
    df_export.to_excel(excel_file, index=False)
    print(f'Report file generated successfully. Please check "{excel_file}" for details.')

    # For inserting the data in Database
    for data in log_data:
        document = {
            'Company Name': data[0],
            'Deviation of Stocks': data[1],
            'Profit/Loss Percentage': data[2],
            'Current Stock Price(LTP)': data[3],
            'High Price': data[4],
            'Low Price': data[5]
        }
        records.insert_one(document)

    # Sending Mail
    sender_email_id = 'parkardigital95@gmail.com'
    password = input("Enter your password and Press Enter: ")
    receiver_email_id = input("Enter the receiver mail ID here: ")
    names = input("Enter the receiver name: ")
    subject = "File of BSE API Data"
    body = f"Dear {names}, \n \t I have sent you an excel file of BSE API data. " \
           f"\n\nThanks and Regards \nParkar Digital \n5th Floor, C-Wing, Manikchand Ikon,\nBund Garden," \
           f"Dhole Patil Road,\nPune Maharashtra, 411001."
    attachment_filename = 'log_data_file.xlsx'
    send_email(sender_email_id, password, receiver_email_id, names, subject, body, attachment_filename)


# Database connection
db = connect_to_database()
records = db.stocks_records
document_count = records.count_documents({})
print("Number of documents in database:", document_count)

# For importing the data from .csv file
csv_file = 'portfolio.csv'
generate_profit_loss(csv_file)
