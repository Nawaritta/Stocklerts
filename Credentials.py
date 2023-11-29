import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
email_sender = os.getenv("email_sender")
email_password = os.getenv("email_password")
AlphaVantage_API_key = os.getenv("AlphaVantage_API_key")
NEWS_API_KEY= os.getenv("NEWS_API_KEY")
SECRETKEY= os.getenv("SECRETKEY")