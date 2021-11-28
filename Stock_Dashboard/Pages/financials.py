import pandas as pd
from datetime import datetime, timedelta
import yahoo_fin.stock_info as si
import yfinance as yf
import streamlit as st
import re


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

#function to clean the index text
@st.cache
def format_cols(df):
    loops = len(df) + 1 
    list_index = []
    for i in df.index:  
        list_index.append(re.sub(r"(\w)([A-Z])", r"\1 \2", i).title())
    df.index = list_index


@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

#define the run function
def run():
    
    st.markdown("""
    <p style="text-align: left;"><span style="font-family: Helvetica; color: rgbrgb(44, 130, 201); font-size: 26px;">Financials</span></p>
    """, unsafe_allow_html=True)

    ticker_list = ['-'] + si.tickers_sp500()
    # Add selection box
    global ticker    
    global select_period    
    default_t = ticker_list.index("AAPL")
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)

    if ticker != '-':
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        fin_type = st.radio("", ("Income Statement", "Balance Sheet", "Cash Flow"))
        pulse = st.selectbox("", ("Quarterly", "Annual"))
        
        if fin_type == 'Income Statement' and pulse =="Quarterly":
            inc_stm = si.get_income_statement(ticker, yearly=False)
            format_cols(inc_stm)
            st.table(set_styles(inc_stm))
        elif fin_type == 'Income Statement' and pulse =="Annual":
                inc_stm = si.get_income_statement(ticker, yearly=True)
                format_cols(inc_stm)
                st.table(set_styles(inc_stm))

        elif fin_type == 'Balance Sheet' and pulse =="Quarterly":
            bal_sht = si.get_balance_sheet(ticker, yearly=False)
            format_cols(bal_sht)
            st.table(bal_sht)

        elif fin_type == 'Balance Sheet'  and pulse =="Annual":
            bal_sht = si.get_balance_sheet(ticker, yearly=True)
            format_cols(bal_sht)
            st.table(bal_sht)

        elif fin_type == 'Cash Flow' and pulse =="Quarterly":
            cash_flw = si.get_cash_flow(ticker, yearly=False)
            format_cols(cash_flw)
            st.table(cash_flw)
        
        elif fin_type == 'Cash Flow' and pulse =="Annual":
            cash_flw = si.get_cash_flow(ticker, yearly=True)
            format_cols(cash_flw)
            st.table(cash_flw)

    if fin_type == 'Income Statement':
        csv = convert_df(inc_stm)
    elif fin_type == 'Balance Sheet':
        csv = convert_df(bal_sht)
    elif fin_type == 'Cash Flow':
        csv = convert_df(cash_flw)

    st.download_button("Click to Download",csv,"data.csv","text/csv",key='download-csv')