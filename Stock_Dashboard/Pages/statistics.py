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

int = st.container

@st.cache
def stats_clean(ticker):

    stats = si.get_stats(ticker)
    #split columns to create different df's for each group
    stats_dict = {
    "stock_price_history_list": stats.Attribute[0:7],
    "share_statistics_list": stats.Attribute[7:19],
    "dividends_splits_list": stats.Attribute[19:29],
    "fiscal_year_list": stats.Attribute[29:31],
    "management_effectiveness_list": stats.Attribute[33:35],
    "profitability_list": stats.Attribute[31:33],
    "income_statement_list":  stats.Attribute[35:43],
    "balance_sheet_list": stats.Attribute[43:49],
    "cash_flow_statement_list": stats.Attribute[49:]
    }

    #create different df's for each group
    stock_price_history = stats[stats.Attribute.isin(stats_dict['stock_price_history_list'])]
    share_statistics = stats[stats.Attribute.isin(stats_dict['share_statistics_list'])]
    dividends_splits = stats[stats.Attribute.isin(stats_dict['dividends_splits_list'])]
    fiscal_year = stats[stats.Attribute.isin(stats_dict['fiscal_year_list'])]
    management_effectiveness = stats[stats.Attribute.isin(stats_dict['management_effectiveness_list'])]
    profitability = stats[stats.Attribute.isin(stats_dict['profitability_list'])]
    income_statement = stats[stats.Attribute.isin(stats_dict['income_statement_list'])]
    balance_sheet = stats[stats.Attribute.isin(stats_dict['balance_sheet_list'])]
    cash_flow_statement = stats[stats.Attribute.isin(stats_dict['cash_flow_statement_list'])]

    #rename attribute to actual attribute name
    stock_price_history.rename(columns={"Attribute": "Stock Price History"},inplace=True)
    share_statistics.rename(columns={"Attribute": "Share Statistics"},inplace=True)
    dividends_splits.rename(columns={"Attribute": "Dividends & Splits"},inplace=True)
    fiscal_year.rename(columns={"Attribute": "Fiscal Year"},inplace=True)
    management_effectiveness.rename(columns={"Attribute": "Management Effectiveness"},inplace=True)
    profitability.rename(columns={"Attribute": "Profitability"},inplace=True)
    income_statement.rename(columns={"Attribute": "Income Statement"},inplace=True)
    balance_sheet.rename(columns={"Attribute": "Balance Sheet"},inplace=True)
    cash_flow_statement.rename(columns={"Attribute": "Cash Flow Statement"},inplace=True)

    return stock_price_history, share_statistics, dividends_splits, fiscal_year,management_effectiveness,profitability,income_statement,balance_sheet,cash_flow_statement
    
    
def hover(hover_color="#F1C40F"):
    return dict(selector="tr:hover",
                props=[("background-color", "%s" % hover_color)])

#define the run function
def run():
    
    st.markdown("""<p style="text-align: left;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 26px; color: rgb(44, 130, 201);"><strong>Statastics</strong></span></p>""",
     unsafe_allow_html=True)
    
    ticker_list = ['-'] + si.tickers_sp500()
    # Add selection box
    global ticker    
    global select_period    
    default_t = ticker_list.index("AAPL")
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)

    stock_price_history, share_statistics, dividends_splits, fiscal_year, management_effectiveness, profitability, income_statement,balance_sheet,cash_flow_statement = stats_clean(ticker)
    
    stats_val = si.get_stats_valuation(ticker)
    stats_val.rename(columns={0: "Valuation Measures",1: "Value"},inplace=True)
    
 #set up 2 columns on the page to show the dataframe & the graph side by side
    c1,gap,c2 = st.columns((3,.1, 3))
    
    #show dataframe for quote information
    with c1:
        st.write("Valuation Measures")
        st.table(stats_val)

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Financial Highlights")
        st.table(fiscal_year)
        
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Profitability")
        st.table(profitability)

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Management Effectiveness")
        st.table(management_effectiveness)

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Income Statement")
        st.table(income_statement)

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Balance Sheet")
        st.table(balance_sheet)
        
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Cash Flow Statement")
        st.table(cash_flow_statement)
        
    with c2:
        st.write("Trading Information")
        st.table(stock_price_history)
        
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Share Statistics")
        st.table(share_statistics)
        
        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.write("Dividends & Splits")
        st.table(dividends_splits)
    
