import yfinance as yf
import streamlit as st 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import datetime

st.set_page_config(page_title="Stock Prediction", page_icon=":bar_chart:", layout="wide")
st.title(":chart_with_upwards_trend: Stock Prediction Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

#tickr symbol
tickerSymbol = st.text_input("Enter Stock ticker Symbol: ","GOOGL")
start_date = st.date_input("Start Date", datetime.date(2010, 5, 31))
end_date = st.date_input("End Date", datetime.date(2020, 5, 31))


#get data
tickerData = yf.Ticker(tickerSymbol)

tickerdf= tickerData.history(period='1d',start=start_date, end = end_date)

#Display stock data and statistics
st.subheader(f"Stock Data for {tickerSymbol}")
st.write(f"Showing data from {start_date} to {end_date}")


#RAW DATA
st.subheader(":clipboard: Raw Stock data")
st.dataframe(tickerdf.tail(10))
#show last 10 rows


st.subheader(":chart_with_upwards_trend: Line Chart Analysis ")
st.line_chart(tickerdf.Close)
st.line_chart(tickerdf.Volume)

st.subheader(":bulb: Stock Prediction (Coming Soon)")

st.subheader(f"Information on {tickerSymbol}")
info = tickerData.info
st.write(info)



