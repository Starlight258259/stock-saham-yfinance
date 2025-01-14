import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Inisialisasi session state untuk login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Fungsi Login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "123":
            st.session_state["authenticated"] = True
            st.success("Login berhasil!")
        else:
            st.error("Username atau password salah.")

# Fungsi Logout
def logout():
    st.session_state["authenticated"] = False
    st.info("Anda telah logout.")

# Aplikasi Utama
if not st.session_state["authenticated"]:
    login()
else:
    if st.sidebar.button("Logout"):
        logout()

    st.title("Bapak Mangde Candlestick Saham Interaktif")

    # Input pengguna
    ticker = st.text_input("Masukkan Ticker Saham (contoh: AAPL)", "AAPL").upper()
    start_date = st.date_input("Tanggal Mulai", value=pd.to_datetime("2006-01-01"))
    end_date = st.date_input("Tanggal Akhir", value=pd.to_datetime("today"))

    if start_date > end_date:
        st.error("Tanggal mulai harus sebelum tanggal akhir.")
        st.stop()

    try:
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            st.warning(f"Tidak ada data untuk ticker {ticker} dalam rentang tanggal yang dipilih.")
        else:
            # Tabs untuk setiap bagian
            tab1, tab2, tab3, tab4 = st.tabs(["Grafik Utama", "RSI", "MACD", "Data"])

            with tab1:  # Grafik Utama
                fig = go.Figure(data=[go.Candlestick(x=data.index,
                                                      open=data['Open'],
                                                      high=data['High'],
                                                      low=data['Low'],
                                                      close=data['Close'])])

                fig.update_layout(title=f"Harga Saham {ticker}",
                                  xaxis_title="Tanggal",
                                  yaxis_title="Harga",
                                  xaxis_rangeslider_visible=False,
                                  template="plotly_dark")

                # Rata-rata Bergerak (MA)
                ma_days = st.slider("Periode Rata-Rata Bergerak", 5, 200, 20)
                data[f'MA{ma_days}'] = data['Close'].rolling(window=ma_days).mean()
                fig.add_trace(go.Scatter(x=data.index, y=data[f'MA{ma_days}'], mode='lines', name=f'MA {ma_days}'))

                # Bollinger Bands
                bb_window = st.slider("Periode Bollinger Bands", 5, 200, 20)
                data['MA'] = data['Close'].rolling(window=bb_window).mean()
                data['Std'] = data['Close'].rolling(window=bb_window).std()
                data['Upper Band'] = data['MA'] + (data['Std'] * 2)
                data['Lower Band'] = data['MA'] - (data['Std'] * 2)
                fig.add_trace(go.Scatter(x=data.index, y=data['Upper Band'], mode='lines', name='Upper Band', line=dict(color='red', width=1)))
                fig.add_trace(go.Scatter(x=data.index, y=data['Lower Band'], mode='lines', name='Lower Band', line=dict(color='red', width=1)))

                st.plotly_chart(fig)

            with tab2:  # RSI
                rsi_period = st.slider("Periode RSI", 2, 20, 14)
                delta = data['Close'].diff()
                up = delta.clip(lower=0)
                down = -1 * delta.clip(upper=0)
                avg_up = up.rolling(window=rsi_period).mean()
                avg_down = down.rolling(window=rsi_period).mean()
                rs = avg_up / avg_down.replace(0, np.nan)
                data['RSI'] = 100 - (100 / (1 + rs))

                fig_rsi = go.Figure(data=[go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI')])
                fig_rsi.update_layout(title=f"RSI {ticker}", yaxis_title="Nilai RSI", template="plotly_dark", yaxis_range=[0, 100])
                st.plotly_chart(fig_rsi)

            with tab3:  # MACD
                exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                macd = exp1 - exp2
                signal = macd.ewm(span=9, adjust=False).mean()
                data['MACD'] = macd
                data['Signal Line'] = signal

                fig_macd = go.Figure()
                fig_macd.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'))
                fig_macd.add_trace(go.Scatter(x=data.index, y=data['Signal Line'], mode='lines', name='Signal Line'))
                fig_macd.update_layout(title=f"MACD {ticker}", template="plotly_dark")
                st.plotly_chart(fig_macd)

            with tab4:  # Data
                if st.checkbox("Tampilkan Tabel Data"):
                    st.dataframe(data)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}. Silakan periksa simbol ticker dan rentang tanggal.")
