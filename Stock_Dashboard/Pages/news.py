#from google.protobuf.symbol_database import Default
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas.core.indexes.base import Index
import yahoo_fin.stock_info as si
import yfinance as yf
import streamlit as st
import numpy as np
import plotly.express as px
from IPython.display import display_html
import plotly.graph_objects as go
import tweepy
import requests
#import config

import tweepy

TWITTER_CONSUMER_KEY = st.secrets['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = st.secrets['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = st.secrets['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = st.secrets['TWITTER_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

def run():
    
    ticker_list = ['-'] + si.tickers_sp500()
    # Add selection box
    global ticker
    default_t = ticker_list.index("AAPL")
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)

    tweets = api.user_timeline()

    st.image(f"https://finviz.com/chart.ashx?t={ticker}")

    for tweet in tweets:
        if '$' in tweet.text:
            words = tweet.text.split(' ')
            for word in words:
                if word.startswith('$') and word[1:].isalpha():
                    symbol = word[1:]
                    st.write(symbol)
                    st.write(tweet.text)
                    st.image(f"https://finviz.com/chart.ashx?t={ticker}")


    r = requests.get("https://api.stocktwits.com/api/2/streams/symbol/" + ticker + ".json")

    data = r.json()
    
    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['body'])
        st.write(message['created_at'])
        st.write(message['body'])