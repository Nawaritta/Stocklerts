from StockPriceState import pricechange
from SendMail import emailsubject, emailbody, sendmail
from app import app
from app import db, Order
from datetime import date
import pandas as pd

with app.app_context():
    orders = db.session.query(Order).all()

    for order in orders:
        PRICE_CHANGE = pricechange(order.stock, order.company)

        if emailsubject(PRICE_CHANGE):
            EmailSubject = emailsubject(PRICE_CHANGE)
            EmailBody = emailbody(EmailSubject)
            TO = order.user_email
            sendmail(TO, EmailSubject, EmailBody)