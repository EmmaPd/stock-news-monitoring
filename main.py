import requests
from datetime import datetime, timedelta, date
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY_TRADING = "0CGZ27UBAGH8TZV7"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

TRIGGER = 5


def percentage_difference(yesterday_price, day_before_yesterday_price):
    if yesterday_price > day_before_yesterday_price:
        price_difference = yesterday_price - day_before_yesterday_price
        return (price_difference/yesterday_price)*100
    else:
        price_difference = day_before_yesterday_price - yesterday_price
        return (price_difference / day_before_yesterday_price) * 100


def get_news():
    global yesterday_close_price, day_before_yesterday_close_price, TRIGGER
    if yesterday_close_price > day_before_yesterday_close_price:
        title = f"({STOCK}): 🔺{TRIGGER}"
    else:
        title = f"({STOCK}): 🔻{TRIGGER}"

    NEWS_API_KEY = "cf57aa178940439c94a677c9ce82ab77"
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    parameters = {
        "apiKey": NEWS_API_KEY,
        "q": "Tesla"
    }

    response = requests.get(NEWS_ENDPOINT, params=parameters)
    response.raise_for_status()
    data = response.json()

    for article in data["articles"][:3]:
        headline = article["title"]
        brief = article["description"]

        account_sid = 'ACb0f9c187be5d5808e409d292040b2ddb'
        auth_token = 'bfe14eb0057be1e56795ed640e11ad8f'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            messaging_service_sid='MGd866751ce2262055d0dd71dbb35ca0b2',
            body=f'{title}\nHeadline: {headline} ({STOCK})\nBrief: {brief}',
            to='+40757739687'
        )

        print(message.status)

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_TRADING
}

r = requests.get(STOCK_ENDPOINT, params=parameters)
r.raise_for_status()
data = r.json()


yesterday = datetime.today() - timedelta(days=1)
yesterday_date_string = datetime.strftime(yesterday, "%Y-%m-%d")

day_after_yesterday = datetime.today() - timedelta(days=2)
day_before_yesterday_date_string = datetime.strftime(day_after_yesterday, "%Y-%m-%d")

yesterday_close = float(data["Time Series (Daily)"][yesterday_date_string]["4. close"])
yesterday_close_price = float(yesterday_close)
print(f"Yesterday's closing price was: {yesterday_close_price}")

day_before_yesterday_close = float(data["Time Series (Daily)"][day_before_yesterday_date_string]["4. close"])
day_before_yesterday_close_price = float(day_before_yesterday_close)
print(f"Yesterday-1's closing price was: {day_before_yesterday_close_price}")

if TRIGGER >= 5:
    get_news()

