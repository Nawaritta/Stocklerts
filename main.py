from StockPriceState import pricechange
from SendMail import emailsubject, emailbody, sendmail
from app import app
from app import db, Order, User
from datetime import date
import pandas as pd

with app.app_context():
    orders = db.session.query(Order).all()

    for order in orders:
        PRICE_CHANGE = pricechange(order.stock, order.company)

        if emailsubject(PRICE_CHANGE):
            EmailSubject = emailsubject(PRICE_CHANGE)
            user = db.session.query(User).filter(User.email == order.user_email).first()
            client_name = user.name

            EmailBody = emailbody(EmailSubject, client_name)
            TO = order.user_email
            sendmail(TO, EmailSubject, EmailBody)