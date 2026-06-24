import streamlit as st
from strategy import get_signal
from database import init_db, save_trade

st.set_page_config(page_title="AI Trader Pro", layout="wide")
init_db()

st.title("🤖 AI-QUANT TRADER PRO")
ticker = st.selectbox("Select Stock", ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS'])

if st.button("🚀 Analyze Market"):
    signal, price, rsi = get_signal(ticker)
    color = "green" if signal == "BUY" else "red" if signal == "SELL" else "orange"
    st.markdown(f"<h2 style='color:{color};'>Signal: {signal}</h2>", unsafe_allow_html=True)
    st.metric("Price", f"₹{price:.2f}", f"RSI: {rsi:.2f}")

    if signal != "HOLD":
        res = st.radio("Result", ["PROFIT", "LOSS"])
        pnl = st.number_input("Profit/Loss Amount")
        if st.button("Save Trade"):
            save_trade(ticker, res, pnl)
            st.success("Trade Logged!")
