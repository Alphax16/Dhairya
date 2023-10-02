import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler


try:
    st.markdown(
        """
        <style>
            .reportview-container .main {
                max-width: 100%;
            }
            .reportview-container .main .block-container {
                max-width: 100%;
                padding-left: 0px;
                padding-right: 0px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load the LSTM model and scaler
    model = load_model("./weights-pickles/Stock_Market_Analysis.h5")
    scaler = MinMaxScaler(feature_range=(0, 1))

    st.title('Stock Price Forecast')
    st.sidebar.header('User Input')

    # stock_symbol = st.sidebar.selectbox('Select Stock Name', ['AAPL'])
    # Fetch list of stock symbols
    # Fetch a list of all available stock symbols
    all_stock_symbols = yf.Tickers('AAPL MSFT GOOGL AMZN').tickers  # Replace with your preferred list

    # Create a dropdown to select the stock symbol
    stock_symbol = st.sidebar.selectbox('Select Stock Name', all_stock_symbols)
    end_date = st.sidebar.date_input('Select Prediction Date', datetime.now() + timedelta(days=1))

    end_date_str = end_date.strftime('%Y-%m-%d')
    start_date = end_date - timedelta(days=365)
    start_date_str = start_date.strftime('%Y-%m-%d')
    data = yf.download(stock_symbol, start=start_date_str, end=end_date_str)
    print(data)

    # Check if there are enough data points for prediction
    if len(data) >= 60-17:
        # Prepare data for prediction
        dataset = data['Close'].values.reshape(-1, 1)
        scaled_data = scaler.fit_transform(dataset)

        # Prepare X_test data
        x_test = []
        for i in range(len(scaled_data) - 60-17, len(scaled_data)):
            x_test.append(scaled_data[i - 60-17:i, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        # Make prediction
        predicted_price = model.predict(x_test)
        predicted_price = scaler.inverse_transform(predicted_price)

        # Prepare dates for prediction results
        prediction_dates = pd.date_range(start=end_date - timedelta(days=59-17), end=end_date, freq='B')[:len(predicted_price)]

        # Display the predicted stock price
        st.subheader('Predicted Stock Price')
        st.line_chart(pd.DataFrame(predicted_price, index=prediction_dates, columns=['Predicted']))

        # Display the actual stock price
        st.subheader('Actual Stock Price')
        st.line_chart(data['Close'])

        # Show the details of the prediction
        st.subheader('Prediction Details')
        st.write(f"Stock Symbol: {stock_symbol}")
        st.write(f"Prediction Date: {end_date_str}")
        st.write(f"Predicted Closing Price: {predicted_price[-1][0]:.2f}")
    else:
        st.error("Not enough historical data points available for prediction. Please select a different date range.")

except Exception as ex:
    print('Exception:', ex)
