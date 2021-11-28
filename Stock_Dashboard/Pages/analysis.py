import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yahoo_fin.stock_info as si
import yfinance as yf
import streamlit as st



#define dataframe table hover style
def hover(hover_color="blue"):
        return dict(selector="td:hover",
                    props=[("background-color", "%s" % hover_color)])

#define table style function
def set_styles(results):
    table_styles = [
                hover(),
                dict(selector="th", props=[("visibility", "show")])
                ]
    return (
        results.style.set_table_styles(table_styles)
        .set_properties(**{"background-color": "black", "color": "white"
        })

    )


#function to get quote data
@st.cache
def analyst(ticker):
    analyst = si.get_analysts_info(ticker)
    analyst_ee = analyst['Earnings Estimate']
    analyst_re = analyst['Revenue Estimate']
    analyst_eh = analyst['Earnings History']
    analyst_et = analyst['EPS Trend']
    analyst_er = analyst['EPS Revisions']
    analyst_ge = analyst['Growth Estimates']
    return analyst_ee, analyst_re, analyst_eh, analyst_et, analyst_er, analyst_ge


#define the run function
def run():
    st.markdown("""
    <p style="text-align: left;"><span style="font-family: Helvetica; color: rgbrgb(44, 130, 201); font-size: 26px;">Analysis Info</span></p>
    """, unsafe_allow_html=True)

    ticker_list = ['-'] + si.tickers_sp500()
    # Add selection box
    global ticker    
    global select_period    
    default_t = ticker_list.index("AAPL")
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)

    analyst_ee, analyst_re, analyst_eh, analyst_et, analyst_er , analyst_ge  = analyst(ticker)
    dfs = [analyst_ee, analyst_re, analyst_eh, analyst_et, analyst_er , analyst_ge]

    for k in dfs:
        st.table(set_styles(k))
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    
    

