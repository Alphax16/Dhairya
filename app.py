# app.py

import streamlit as st
import pandas as pd
from analysis_functions_2 import get_historical_data, moving_average_crossover_strategy, predict_stock_prices


st.set_page_config(
    page_icon='🎯',
    page_title="Dhairya - Stock Trading Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a Bug": None,
        "About": None
    },
)

hide_streamlit_style = '''
            <style>
            # [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            '''

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS to center the content horizontally
custom_css = '''
<style>
.centered {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}
</style>
'''

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

VALID_STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# Centered content
st.markdown('<div class="centered">', unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'>🎯 Dhairya- The Stock Trading Analysis Platform</h1>",
    unsafe_allow_html=True
)
# st.title("DHAIRYA- Stock Trading Analysis")

# st.title("MA Stock Trading Analysis Window")
st.markdown(
    "<h2 style='text-align: center;'>MA Stock Trading Analysis Window</h2>",
    unsafe_allow_html=True
)

start_date = st.date_input("Select Start Date:", pd.to_datetime('2022-01-01'))
end_date = st.date_input("Select End Date:", pd.to_datetime('2023-01-01'))
ticker = st.selectbox("Select Stock Symbol:", VALID_STOCK_SYMBOLS)

# Create an empty element for warnings
warning_element = st.empty()

if st.button("Start Analysis"):
    # Display warnings on the fly
    if start_date >= end_date:
        warning_element.warning("Invalid input: End date must be after start date.")
    elif not ticker:
        warning_element.warning("Invalid input: Please select a stock symbol.")
    else:
        try:
            data = get_historical_data(ticker, start_date, end_date)
            if data.empty:
                warning_element.warning("No data available for the selected date range and stock symbol.")
            else:
                signals = moving_average_crossover_strategy(data)
                predicted_prices = predict_stock_prices(data)

                st.write("Moving Average Crossover Signals:")
                st.write(signals)

                st.write("Predicted Stock Prices:")
                st.write(predicted_prices)

                # Plot stock prices, moving averages, and predicted prices
                st.line_chart(data[['Close', 'Short_MA', 'Long_MA']])
                st.line_chart(predicted_prices[['Close', 'Predicted_Close']])

        except Exception as ex:
            warning_element.error(f"An error occurred: {ex}")

# Close centered content div
st.markdown('</div>', unsafe_allow_html=True)
