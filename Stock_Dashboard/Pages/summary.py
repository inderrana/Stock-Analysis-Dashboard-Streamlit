from operator import truth
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

#define dataframe table hover style
def hover(hover_color="blue"):
        return dict(selector="td:hover",
                    props=[("background-color", "%s" % hover_color)])

#define table style function
def set_styles(results):
    table_styles = [
                hover(),
                dict(selector="th", props=[("visibility", "hidden")])
                ]
    return (
        results.style.set_table_styles(table_styles)
        .set_properties(**{"background-color": "black", "color": "white"
        })

    )

#function to get quote data and show side by side
@st.cache
def get_quote_table(ticker):
    keys_col1 = ("Previous Close", "Open", "Bid", "Ask", "Day's Range", "52 Week Range", "Volume", "Avg. Volume")
    keys_col2 = ("Market Cap", "Beta (5Y Monthly)" , "PE Ratio (TTM)" , "EPS (TTM)" , "Earnings Date" , "Forward Dividend & Yield" , "Ex-Dividend Date" , "1y Target Est")
    summary = si.get_quote_table(ticker)
    summary1 = { your_key: summary[your_key] for your_key in keys_col1 }
    summary1 = pd.DataFrame.from_dict(summary1, orient='index')
    summary1[0] = summary1[0].astype(str)
    summary1.columns= ['']
    summary2 = { your_key: summary[your_key] for your_key in keys_col2 }
    summary2 = pd.DataFrame.from_dict(summary2, orient='index')
    summary2[0] = summary2[0].astype(str)
    summary2.columns= ['']
    summary1.reset_index(inplace=True)
    summary2.reset_index(inplace=True)
    summary3 = pd.concat([summary1, summary2], axis=1)
    summary3.reset_index(drop=True)
    sumarr = np.array(summary3)
    final_summary = pd.DataFrame(data=sumarr)
    final_summary = final_summary
    return set_styles(final_summary)

#function to plot stock price over time
@st.cache
def plot1(ticker):
    plot_data = yf.download(ticker)
    fig1 = px.area(plot_data.Close)
    fig1.update_layout(showlegend=False)
    fig1.update_layout(height=400, width=600)
    fig1.update_xaxes(
    #rangeslider_visible=True, 
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1D", step="day", stepmode="backward"),
            dict(count=5, label="5D", step="day", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ),rangeselector_bgcolor="blue"
)
    return fig1


#define the run function
def run():
   
    st.markdown("""
    <p style="text-align: center;"><span style="font-family: Helvetica;
     color: rgb(44, 130, 201); font-size: 36px;">Stock Analysis Dashboard</span></p>
    """, unsafe_allow_html=True)
    
    ticker_list = ['-'] + si.tickers_sp500()
# Add selection box
    global ticker    
    global select_period    
    default_t = ticker_list.index("")
    if ticker_list:
            ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    else: st.warning("No tickers available.")
    #ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)
    st.sidebar.text("Select a stock and click submit")
    button_clicked = st.sidebar.button("Submit")        

    #set up 2 columns on the page to show the dataframe & the graph side by side
    c1,c2 = st.columns((3,2))
    #show dataframe for quote information
    if button_clicked == False:
            st.markdown("""
    <p style="text-align: center;"><span style="font-family: Helvetica;
     color: rgb(184, 49, 47); font-size: 30px;">**Please select a ticker and click submit**</span></p>
    """, unsafe_allow_html=True)
            st.image("https://www.investors.com/wp-content/uploads/2020/06/Stock-bearbullchart-02-adobe.jpg")
    elif button_clicked == True:
        with c1:
            if ticker != '-':
                st.write("Stock Summary")
                st.markdown("#")
                info = get_quote_table(ticker)
                st.table(info)

        #show graph
        with c2:
            if ticker != '-':
                st.write('Adjusted close price')
                st.plotly_chart(plot1(ticker))            
