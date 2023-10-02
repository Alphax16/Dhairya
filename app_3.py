# app.py

import streamlit as st
import pandas as pd
from analysis_functions_2 import get_historical_data, moving_average_crossover_strategy


VALID_STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

st.title("Moving Average Crossover Stock Trading App")

start_date = st.date_input("Select Start Date:", pd.to_datetime('2022-01-01'))
end_date = st.date_input("Select End Date:", pd.to_datetime('2023-01-01'))
ticker = st.selectbox("Select Stock Symbol:", VALID_STOCK_SYMBOLS)

if st.button("Generate Signals"):
    if start_date < end_date and ticker:
        data = get_historical_data(ticker, start_date, end_date)
        signals = moving_average_crossover_strategy(data)

        st.write(signals)

        # Plot stock prices and moving averages
        st.line_chart(data[['Close', 'Short_MA', 'Long_MA']])  # Updated column names: 'Short_MA' and 'Long_MA'
    else:
        st.warning("Invalid input. Please ensure the start date is before the end date and a stock symbol is selected.")
