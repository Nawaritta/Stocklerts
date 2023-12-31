from StockPriceState import pricechange
from SendMail import emailsubject, emailbody, sendmail
from app import app
from app import db, Order, User

with app.app_context():
    orders = db.session.query(Order).all()

    for order in orders:
        PRICE_CHANGE = pricechange(order.stock)
        user = db.session.query(User).filter(User.email == order.user_email).first()

        if PRICE_CHANGE is not None:

            EmailSubject = emailsubject(order.stock, PRICE_CHANGE)
            user = db.session.query(User).filter(User.email == order.user_email).first()
            client_name = user.name
            EmailBody = emailbody(EmailSubject, client_name, order.company)
            TO = order.user_email
            sendmail(TO, EmailSubject, EmailBody)
