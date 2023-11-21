from StockPriceState import pricechange
from sendmail import emailsubject, emailbody, sendmail

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

PRICE_CHANGE = pricechange(STOCK_NAME, COMPANY_NAME)

if emailsubject(PRICE_CHANGE):
    EmailSubject = emailsubject(PRICE_CHANGE)
    EmailBody = emailbody()
    client = "Nor.benhaddou@gmail.com"
    sendmail(client, EmailSubject, EmailBody)
