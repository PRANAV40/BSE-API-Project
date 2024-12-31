Create a script which will generate a report on **Profit and loss statement** of **share market portfolio**.

Get input from the user in **csv file**. Csv file will have 3 columns Company Name, Rate per share, quantity of share. The script should make a call to **BSE API** and get the current/LTP (last trading prize) of that company share. Get the mapping of **company name** and the **BSE stock code from the UR**L 
use this url for data https://static.quandl.com/BSE+Descriptions/stocks.txt
Generate a statement of **Profit and Loss** as well **calculate the deviation** from purchase price to current price. Log the data into another text file. The log data should contain the **company name and day high price** of that stock using python **BSE API**.

● Utilized Python to process a CSV file with company name, rate per share, and quantity. Retrieved LTP (Last Trading Price) and day 
high prices via BSE API, mapping stock codes. 
● Calculated profit/loss by comparing purchase price with current price and performed deviation analysis. Generated a detailed 
Profit and Loss statement. 
● Logged financial details into a excel file and stored them in MongoDB for analysis and tracking. 
● Compiled results into an Excel sheet and sent it to the user via Python's SMTP library.
