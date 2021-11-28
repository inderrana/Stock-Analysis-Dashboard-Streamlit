import streamlit as st
import yahoo_fin.stock_info as si
from Pages import summary, chart, statistics, financials, analysis, mc, news, market_index

CURRENT_THEME = "light"


PAGES = {
    "Summary": summary,
    "Chart": chart,
    "Statistics": statistics,
    "Financials": financials,
    "Analysis": analysis,
    "Monte Carlo": mc,
    "Twitter Stock Buzz": news,
    "World Indices": market_index,
    
}

def main():
    favicon = "💸"
    st.set_page_config(layout="wide",
    page_title='Stock Analysis Dashboard', page_icon = favicon, initial_sidebar_state = 'auto')
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;
    } 
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)   
    


    
    st.sidebar.title('Navigation')
    selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
    page = PAGES[selection]


    with st.spinner(f'Loading {selection} ...'):
        page.run()


#p_values = ("1d", "5d", "1mo", "6mo", "YTD", "1Y", "5Y", "MAX")
#default_p = p_values.index("MAX")
#select_period = st.sidebar.selectbox("Select a period",p_values, index=default_p )


if __name__ == "__main__":
    main()