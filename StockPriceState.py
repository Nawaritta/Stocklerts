import requests
from Credentials import AlphaVantage_API_key


def pricechange(STOCK_NAME, COMPANY_NAME):
    '''
    This function spots the stock price fluctuations (increase/decreases)
    between yesterday and the day before yesterday
    '''
    STOCK_ENDPOINT = "https://www.alphavantage.co/query"

    # Get yesterday's closing stock price
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": AlphaVantage_API_key,
    }

    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    if 'Error Message' in response.json():
        return None
    data = response.json()["Time Series (Daily)"]
    data_list = [value for value in data.values()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]

    # Get the day before yesterday's closing stock price

    Bfore_yesterday_data = data_list[1]
    Bfore_yesterday_closing_price = Bfore_yesterday_data["4. close"]

    # The percentage difference in price between the two days
    fluctuation = float(yesterday_closing_price) - float(Bfore_yesterday_closing_price)
    fluc_percent = round((abs(fluctuation) / float(yesterday_closing_price)) * 100)

    PRICE_CHANGE = {"fluctuation": fluctuation, "fluc_percent": fluc_percent}
    return PRICE_CHANGE
