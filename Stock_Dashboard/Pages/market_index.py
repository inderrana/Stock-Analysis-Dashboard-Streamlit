from bs4 import BeautifulSoup
from matplotlib.pyplot import annotate
import requests
import streamlit as st
import pandas as pd
import yahoo_fin.stock_info as si

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

#Function to get market incides
@st.cache
def get_market_idx():
    website_html = requests.get("https://finance.yahoo.com/world-indices/").text
    soup = BeautifulSoup(website_html)
    table = soup.find("tbody", {"data-reactid": "36"})
    table_text = [[cell.text for cell in row.contents] for row in table.contents]
    mkt_df = pd.DataFrame(table_text, columns=["Symbol","Name","LastPrice","Change","pct_change","Volume", "intraday_high_low","52_week_range","day_chart"])
    filter_mkt_lst = ["S&P 500","Dow 30","Nasdaq","Russell 2000", "NYSE COMPOSITE (DJ)", "Crude Oil", "Gold"]
    mkt_df = mkt_df[mkt_df.Name.isin(filter_mkt_lst)][["Name","LastPrice","Change","pct_change"]]
    return mkt_df

#function top get top/bottom stocks
def top_n(n):
    top_gainers = si.get_day_gainers().head(n)
    top_loosers = si.get_day_losers().head(n)
    return top_gainers, top_loosers

#define the run function
def run():

    st.markdown("""
    <p style="text-align: left;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 26px; color: rgb(44, 130, 201);"><strong>Market Summary</strong></span></p>
    """, unsafe_allow_html=True)

    variable_output = si.get_market_status()


    html_str = f"""
    <style>
    p.a
    </style>
    <p class="a">MARKET STATUS ={variable_output}</p>
    """
    st.markdown(html_str, unsafe_allow_html=True)
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    

    st.write("Incides")
    st.table(set_styles(get_market_idx()))
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


    n = st.sidebar.slider("Select no. of records to show", 1, 25, 5)
    button_submit = st.sidebar.button("Submit") 
    
    top_gainers, top_loosers = top_n(n+1)

    st.write("Top Gainers")
    st.table(set_styles(top_gainers))
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

    st.write("Top Loosers")
    st.table(set_styles(top_loosers))
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


        

