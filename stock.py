import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.title("Interactive Stock Candlestick Chart")

# User input for ticker symbol and date range
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL").upper()
start_date = st.date_input("Start Date", value=pd.to_datetime("2006-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("today"))

try:
    # Fetch data using yfinance
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
      st.warning(f"No data found for ticker {ticker} within the specified date range.")
    else:
        # Create candlestick chart using Plotly
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])

        # Customize layout
        fig.update_layout(title=f"{ticker} Stock Price",
                          xaxis_title="Date",
                          yaxis_title="Price",
                          xaxis_rangeslider_visible=False) # Hide range slider for cleaner look

        # Add moving averages (optional)
        ma_days = st.slider("Moving Average Days", 5, 200, 20)  # Slider for MA period
        data[f'MA{ma_days}'] = data['Close'].rolling(window=ma_days).mean()
        fig.add_trace(go.Scatter(x=data.index, y=data[f'MA{ma_days}'], mode='lines', name=f'MA {ma_days}'))


        # Volume bars (optional)
        show_volume = st.checkbox("Show Volume", value=False)
        if show_volume:
            fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', yaxis='y2'))
            fig.update_layout(yaxis2=dict(title='Volume', overlaying='y', side='right')) # Configure secondary y-axis

        st.plotly_chart(fig)

        # Display data as a table (optional)
        if st.checkbox("Show Data Table"):
            st.dataframe(data)

except Exception as e:
    st.error(f"An error occurred: {e}. Please check the ticker symbol and date range.")