from google.protobuf.symbol_database import Default
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas.core.indexes.base import Index
import yahoo_fin.stock_info as si
import yfinance as yf
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def StockCurrentWeek(ticker, days, interval):
    # Get the current date
    current_date = datetime.now().date()
    #calculate end date
    to_date = current_date - timedelta(days=days)
    
    # Get the stock close price of this week
    #stock_price = yf.Ticker("aapl").history(start=end_date, interval="1mo")
    stock_price = si.get_data(ticker, start_date=to_date, end_date=current_date, interval = interval)
    return stock_price

def chart_line(ticker, start_date, end_date, interval):
    plot_data = si.get_data(ticker, start_date = start_date, end_date=end_date, interval=interval)
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
  
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, subplot_titles=('Trend', 'Volume'), 
                    row_width=[0.2, 0.7])
    #add line plot for close price
    
    fig.add_trace(
        go.Scatter(x=plot_data.index,y =plot_data.close,
        #add df text for tooltips
        text = plot_data.round()
        ), row=1,col=1)
   
    #add bar chart for volume
    fig.add_trace(
        go.Bar(
            x=plot_data.index,y =plot_data.volume,
            text = plot_data.round()), row=2, col=1)       
    fig.update_layout(height=600, width=1000)     
    #add tooltips
    fig.update_traces(
        hovertemplate="<br>".join([
            "Date: %{x}",
            "Open: %{text[0]}",
            "High: %{text[1]}",
            "Low: %{text[2]}",
            "Close: %{text[3]}",
            "Adj Close: %{text[4]}",
            "Volume: %{text[5]}",
        ])
    )    
    fig.update_layout(showlegend=False)
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(height=600, width=1000)
    fig.update_xaxes(
    rangeslider_visible=False, 
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ),rangeselector_bgcolor="blue"
)
    return fig

#def Chart2(ticker, period):
def Candle(ticker, start_date, end_date, interval):
    #plot_data = yf.download(ticker, period = "MAX")
    plot_data = si.get_data(ticker, start_date = start_date, end_date=end_date, interval=interval)

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Create subplots and mention plot grid size
    fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('Trend', 'Volume'), 
                row_width=[0.2, 0.7])


    # include candlestick with rangeselector
    fig2.add_trace(go.Candlestick(x=plot_data.index,
                    open=plot_data.open, high=plot_data.high,
                    low=plot_data.low, close=plot_data.close, name="OHLC"), 
                    row=1, col=1)

    # include a go.Bar trace for volumes
    fig2.add_trace(go.Bar(x=plot_data.index, y=plot_data.volume, showlegend=False), row=2, col=1)
    
    fig2.add_trace(go.Scatter(x=plot_data.index,y=plot_data['close'].rolling(window=50).mean(),marker_color='blue',name='MA50'))
    
    fig2.update(layout_xaxis_rangeslider_visible=False)
    fig2.update_layout(height=600, width=1000)
    fig2.update_xaxes(
    rangeslider_visible=False, 
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ),rangeselector_bgcolor="blue"
)
    return fig2


def run():

    st.markdown("""
    <p style="text-align: left;"><span style="font-family: Helvetica; color: rgbrgb(44, 130, 201); font-size: 26px;">OLHC Charts</span></p>
    """, unsafe_allow_html=True)

    ticker_list = ['-'] + si.tickers_sp500()
    # Add selection box
    global ticker    
    #global select_period    
    default_t = ticker_list.index("AAPL")
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)

    global interval    
    #global select_period    
    interval_list = ["1d", "1wk", "1mo"] 
    default_i = interval_list.index("1d")
    interval = st.sidebar.selectbox("Select an interval", interval_list, index = default_i)

    # Add select begin-end date
    global start_date, end_date
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=365))
    end_date = col2.date_input("End date", datetime.today())
    

    if ticker != '-':
                chart_type = st.selectbox("", ("Candlestick", "Line Chart"))
                if chart_type == 'Candlestick':
                    st.plotly_chart(Candle(ticker, start_date = start_date,end_date=end_date, interval=interval))
                else:
                 st.plotly_chart(chart_line(ticker, start_date = start_date,end_date=end_date, interval=interval))