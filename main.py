import streamlit as st
from strategy import get_signal
from database import init_db, save_trade

st.set_page_config(page_title="AI Trader Pro", layout="wide")
init_db()

st.title("🤖 AI-QUANT TRADER PRO")
ticker = st.selectbox("Select Stock", ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS', 'WIPRO.NS', 'HDFCBANK.NS'])

if st.button("🚀 Analyze Market"):
    # लोडिंग इंडिकेटर
    with st.spinner('AI मार्केट स्कॅन करत आहे...'):
        signal, price, rsi = get_signal(ticker)
    
    # रिझल्ट डिस्प्ले
    color = "green" if signal == "BUY" else "red" if signal == "SELL" else "orange"
    st.markdown(f"<h2 style='color:{color};'>Signal: {signal}</h2>", unsafe_allow_html=True)
    st.metric("Price", f"₹{price:,.2f}", f"RSI: {rsi:.2f}")

    if signal != "HOLD":
        st.subheader("Log your trade")
        res = st.radio("Result", ["PROFIT", "LOSS"])
        pnl = st.number_input("Profit/Loss Amount")
        if st.button("Save Trade"):
            save_trade(ticker, res, pnl)
            st.success("Trade Logged Successfully!")

# डॅशबोर्ड लिंक
st.sidebar.markdown("---")
st.sidebar.write("तुमचा परफॉरमन्स पाहण्यासाठी 'Performance' पेजवर जा.")
