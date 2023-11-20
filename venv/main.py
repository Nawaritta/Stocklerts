import requests
from sendmail import emailsubject, emailbody, sendmail
from credentials import AlphaVantage_API_key, NEWS_API_KEY

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"


# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": AlphaVantage_API_key,
}
'''
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for value in data.values()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

#Get the day before yesterday's closing stock price

Bfore_yesterday_data = data_list[1]
Bfore_yesterday_closing_price = Bfore_yesterday_data["4. close"]

# The percentage difference in price between the two days
fluctuation = float(yesterday_closing_price) - float(Bfore_yesterday_closing_price)
fluc_percent = round((abs(fluctuation) / float(yesterday_closing_price)) * 100)
'''

fluctuation = -7
fluc_percent = 3
rate = 1

PRICE_CHANGE = {"fluctuation": fluctuation, "fluc_percent": rate}

if emailsubject(PRICE_CHANGE, rate):
    EmailSubject = emailsubject(PRICE_CHANGE, rate)
    EmailBody = emailbody()
    client = "Nor.benhaddou@gmail.com"
    sendmail(client, EmailSubject, EmailBody)

