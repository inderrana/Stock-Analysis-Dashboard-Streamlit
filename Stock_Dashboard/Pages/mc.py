import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas.core.indexes.base import Index
import yahoo_fin.stock_info as si
import yfinance as yf
import streamlit as st
import numpy as np
import numpy as np
import pandas_datareader.data as web
import datetime as dt



class MonteCarlo(object):
    
        def __init__(self, ticker, data_source, start_date, end_date, time_horizon, n_simulation, seed):
            
            # Initiate class variables
            self.ticker = ticker  # Stock ticker
            self.data_source = data_source  # Source of data, e.g. 'yahoo'
            self.start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')  # Text, YYYY-MM-DD
            self.end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')  # Text, YYYY-MM-DD
            self.time_horizon = time_horizon  # Days
            self.n_simulation = n_simulation  # Number of simulations
            self.seed = seed  # Random seed
            self.simulation_df = pd.DataFrame()  # Table of results
            
            # Extract stock data
            self.stock_price = web.DataReader(ticker, data_source, self.start_date, self.end_date)
            
            # Calculate financial metrics
            # Daily return (of close price)
            self.daily_return = self.stock_price['Close'].pct_change()
            # Volatility (of close price)
            self.daily_volatility = np.std(self.daily_return)
            
        def run_simulation(self):
            
            # Run the simulation
            np.random.seed(self.seed)
            self.simulation_df = pd.DataFrame()  # Reset
            
            for i in range(self.n_simulation):

                # The list to store the next stock price
                next_price = []

                # Create the next stock price
                last_price = self.stock_price['Close'][-1]

                for j in range(self.time_horizon):
                    
                    # Generate the random percentage change around the mean (0) and std (daily_volatility)
                    future_return = np.random.normal(0, self.daily_volatility)

                    # Generate the random future price
                    future_price = last_price * (1 + future_return)

                    # Save the price and go next
                    next_price.append(future_price)
                    last_price = future_price

                # Store the result of the simulation
                self.simulation_df[i] = next_price

        def plot_simulation_price(self, width, height):
            
            # Plot the simulation stock price in the future
            fig, ax = plt.subplots(figsize=(width, height))

            plt.plot(self.simulation_df)
            plt.title('Monte Carlo simulation for ' + self.ticker + \
                    ' stock price in next ' + str(self.time_horizon) + ' days')
            plt.xlabel('Day')
            plt.ylabel('Price')

            plt.axhline(y=self.stock_price['Close'][-1], color='red')
            plt.legend(['Current stock price is: ' + str(np.round(self.stock_price['Close'][-1], 2))])
            ax.get_legend().legendHandles[0].set_color('red')

            return plt
        
        def plot_simulation_hist(self):
            
            # Get the ending price of the 200th day
            ending_price = self.simulation_df.iloc[-1:, :].values[0, ]

            # Plot using histogram
            plt.hist(ending_price, bins=50)
            plt.axvline(x=self.stock_price['Close'][-1], color='red')
            plt.legend(['Current stock price is: ' + str(np.round(self.stock_price['Close'][-1], 2))])
            ax.get_legend().legendHandles[0].set_color('red')
            return plt

        def plot_simulation_hist(self):
        
        # Get the ending price of the 200th day
            ending_price = self.simulation_df.iloc[-1:, :].values[0, ]
            # Plot using histogram
            plt.hist(ending_price, bins=50)
            plt.axvline(x=self.stock_price['Close'][-1], color='red')
            plt.legend(['Current stock price is: ' + str(np.round(self.stock_price['Close'][-1], 2))])
            ax.get_legend().legendHandles[0].set_color('red')
            plt.show()
        
        def value_at_risk(self):
            # Price at 95% confidence interval
            future_price_95ci = np.percentile(self.simulation_df.iloc[-1:, :].values[0, ], 5)

            # Value at Risk
            VaR = self.stock_price['Close'][-1] - future_price_95ci
            return('VaR at 95% confidence interval is: ' + str(np.round(VaR, 2)) + ' USD')

def run():

    st.markdown("""
    <p style="text-align: left;"><span style="font-family: Verdana, Geneva, sans-serif; font-size: 26px; color: rgb(44, 130, 201);"><strong>Monte Carlo Simulation</strong></span></p>
    """, unsafe_allow_html=True)

    ticker_list = ['-'] + si.tickers_sp500()
    # Add selection box
    global ticker    
    #global select_period    
    default_t = ticker_list.index("AAPL")
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list, index = default_t)

    # Add select begin-end date
    global start_date, end_date
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start date", datetime.today().date() - timedelta(days=365))
    end_date = col2.date_input("End date", datetime.today())

    th_list = [30,60,90]
    n_simulation_list = [200,500,1000]

    default_th = th_list.index(90)
    default_nsim = n_simulation_list.index(200)

    c1,c2 = st.columns((2))

    with c1:
        time_horizon = st.selectbox("Select time horizon", th_list, index=default_th)
    with c2:    
        n_simulation = st.selectbox("Select number of symulations to run", n_simulation_list, index=default_nsim)

    button_clicked = st.button("Submit")        
    
    width = st.sidebar.slider("plot width", 1, 25, 10)
    height = st.sidebar.slider("plot height", 1, 25, 4)

    # Initiate
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    mc_sim = MonteCarlo(ticker=ticker, data_source='yahoo',
                        start_date=start_date, end_date=end_date,
                        time_horizon=time_horizon, n_simulation=n_simulation, seed=123)
    


    #run simulation
    mc_sim.run_simulation()
    # Plot the results
    st.subheader(mc_sim.value_at_risk())
    st.pyplot(mc_sim.plot_simulation_price(width=width, height=height))
    