import streamlit as st
import pandas as pd
from strategy import get_signal
from database import init_db, save_trade, get_history

st.set_page_config(page_title="AI-Quant Trader", layout="wide")
init_db()

st.title("🤖 AI-QUANT TRADER PRO")

# १. डेट रेंज सिलेक्शन
date_map = {"1 Day": "1d", "2 Days": "2d", "5 Days": "5d", "10 Days": "10d", "15 Days": "15d", "30 Days": "30d", "45 Days": "45d", "60 Days": "60d"}
selected_days = st.selectbox("Select Analysis Range", list(date_map.keys()))
period = date_map[selected_days]

# २. स्टॉक सिलेक्शन
ticker = st.selectbox("Select Stock", ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS'])

if st.button("🚀 Analyze Market"):
    with st.spinner('AI मार्केट ॲनालाइज करत आहे...'):
        signal, price, rsi = get_signal(ticker, period=period)
        
    if price == 0.0:
        st.error("डेटा मिळाला नाही. टीकर सिम्बॉल तपासा.")
    else:
        st.metric("Current Price", f"₹{price:,.2f}", f"RSI: {rsi:.2f}")
        st.subheader(f"Signal: {signal}")

# ३. एक्सेल-स्टाईल परफॉर्मन्स टेबल
st.markdown("---")
st.subheader("📊 AI Signal Accuracy Report")
df = get_history()

if not df.empty:
    summary = df.groupby('stock').agg(Total_Trades=('result', 'count'), Wins=('result', lambda x: (x == 'PROFIT').sum()))
    summary['Accuracy (%)'] = (summary['Wins'] / summary['Total_Trades'] * 100).round(2)
    
    display_df = pd.DataFrame({
        'Company Name': summary.index,
        'Stock Symbol': summary.index,
        'Accuracy (%)': summary['Accuracy (%)']
    })
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("डेटा नाही. मार्केट ॲनालाइज करून ट्रेड्स सेव्ह करा.")
