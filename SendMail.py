#!/usr/bin/python3
from email.message import EmailMessage
from email.utils import formataddr
import requests
import ssl
import smtplib
from Credentials import email_sender, email_password, NEWS_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

"""
Example:
STOCK_NAME = "GOOG"
COMPANY_NAME = "Alphabet Inc"
"""


def emailsubject(STOCK_NAME, PRICE_CHANGE, FLUCTUATION_SET=0.1):
    """
    Specifies the email subject based on the fluctuation nature
    and the emoji to send along with the notification
    """
    if PRICE_CHANGE == None:
        return
    EmailSubject = None
    if abs(PRICE_CHANGE["fluctuation"] >= FLUCTUATION_SET):
        EmailSubject = STOCK_NAME + ' share price: '
        if PRICE_CHANGE["fluctuation"] > 0:
            EmailSubject += "📈 rose by "
        else:
            EmailSubject += "📉 dropped by "

        EmailSubject += str(PRICE_CHANGE["fluc_percent"]) + '%'

    return EmailSubject


def emailbody(EmailSubject, client_name, COMPANY_NAME):
    """
    Get News if the fluctuation percentage is greater than the percentage set by the client
    https://newsapi.org/
    """
    EmailBody = (f"""\
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
</head>
<body style="font-family: 'Times New Roman', sans-serif; font-size: 16px; line-height: 1.6; color: #000; margin: 70px; margin-right: 70px;">
    <p style="margin-bottom: 40px; font-weight: bold; color: #000;">Dear {client_name},</p>
    <p style="margin-bottom: 20px; color: #000;">
        We trust this message finds you well. We are writing to inform you of a significant development regarding the stock market activity
        you have been monitoring closely through our platform.  Notably, {EmailSubject} compared to yesterday's closing price.

    </p>
    <p style="margin-bottom: 20px; color: #000;">
        To further enhance your understanding of the development mentioned above, here are snippets of relevant articles that delve into the
        specifics of this market movement:
    </p>

    """)
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    n = 5
    for article in articles[:n]:
        EmailBody += f"""\
            <p style="color: #016064;">
                <strong>- Headline:</strong> {article['title']}. <br>
                <strong>- Brief:</strong> {article['description']}<br>
                ===================================================
            </p>
        """
    EmailBody += (f"""\
                  <br><p style="margin-bottom: 20px; color: #000;">
            As always, our commitment is to keep you informed and empowered in your investment decisions.
        </p>
        <p style="margin-bottom: 20px; color: #000;">
            Thank you for choosing STOCKLERTS as your trusted partner in navigating the financial markets.
        </p>
        <p style="margin-bottom: 20px; color: #000;">
            Best Regards,<br>STOCKLERTS
        </p>

    </body>
    </html>
    """)
    return EmailBody


def sendmail(client: object, subject: object, body: object) -> object:
    """
    Sends an email to the client containing relevant news about the stock that the client is following
    """
    email = EmailMessage()
    email['From'] = formataddr(("STOCKLERTS", f"{email_sender}"))
    email['To'] = client
    email['subject'] = subject
    email.set_content(body, subtype="html", )

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
        s.login(email_sender, email_password)
        s.sendmail(email_sender, client, email.as_string())
