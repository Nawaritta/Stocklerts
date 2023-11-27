from StockPriceState import pricechange
from SendNotification import emailsubject, emailbody, sendmail
from datetime import date
import pandas as pd

STOCK_NAME = "GOOG"
COMPANY_NAME = "Alphabet Inc"




# PRICE_CHANGE = pricechange(STOCK_NAME, COMPANY_NAME)

PRICE_CHANGE = {"fluctuation": 2, "fluc_percent": 7}

if emailsubject(PRICE_CHANGE):
    EmailSubject = emailsubject(PRICE_CHANGE)
    EmailBody = emailbody(EmailSubject)
    client = "Nor.benhaddou@gmail.com"
    sendmail(client, EmailSubject, EmailBody)
