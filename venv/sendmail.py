from email.message import EmailMessage
import requests
import ssl
import smtplib
from credentials import email_sender, email_password, AlphaVantage_API_key, NEWS_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

def emailsubject(PRICE_CHANGE, FLUCTUATION_SET):
    '''
    Specifies the email subject based on the fluctuation nature
    and the emoji to send along with the notification
    '''
    EmailSubject=None
    if abs(PRICE_CHANGE["fluctuation"]) > FLUCTUATION_SET:    
        EmailSubject = STOCK_NAME + ' share price: '
        if PRICE_CHANGE["fluctuation"] > 0:
            EmailSubject += "📈 rose by "
        else:
            EmailSubject += "📉 dropped by "
        
        EmailSubject += str(PRICE_CHANGE["fluc_percent"]) + '%'
        
    return EmailSubject

def emailbody():
    '''
    Get News if the fluctuation percentage is greater than the percentage set by the client
    https://newsapi.org/
    '''
    news_params = {
         "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
        }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    EmailBody = ''
    n=4
    for article in articles[:n]:
        EmailBody += f"Headline: {article['title']}. \nBrief: {article['description']}\n -------------\n"
        
    return EmailBody
    
def sendmail(client, subject, body):
    email = EmailMessage()
    email['From'] = email_sender
    email['To'] = client
    email['subject'] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
        s.login(email_sender, email_password)
        s.sendmail(email_sender, client, email.as_string())