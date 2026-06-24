import streamlit as st
import pandas as pd
from strategy import get_signal
from database import init_db, save_trade, get_history

st.set_page_config(page_title="AI Trader Pro", layout="wide")
init_db()

st.title("🤖 AI-QUANT TRADER PRO")

# १. मुख्य सिग्नल विभाग
ticker = st.selectbox("Select Stock", ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS'])
if st.button("🚀 Analyze Market"):
    signal, price, rsi = get_signal(ticker)
    st.metric("Price", f"₹{price:,.2f}", f"RSI: {rsi:.2f}")
    st.subheader(f"Signal: {signal}")

# २. एक्सेल स्टाईल परफॉर्मन्स टेबल (मुख्य पेजवर)
st.markdown("---")
st.subheader("📊 AI Signal Accuracy Report")

df = get_history()
if not df.empty:
    # डेटा प्रोसेसिंग
    summary = df.groupby('stock').agg(
        Total_Trades=('result', 'count'),
        Wins=('result', lambda x: (x == 'PROFIT').sum())
    )
    summary['Accuracy (%)'] = (summary['Wins'] / summary['Total_Trades'] * 100).round(2)
    
    # एक्सेल स्टाईल टेबल (तुझ्या गरजेनुसार कॉलम्स)
    # कॉलम १: कंपनी (Ticker), कॉलम २: स्टॉक नाव (Ticker), कॉलम ३: सिग्नल, कॉलम ४: ॲक्युरसी
    display_df = pd.DataFrame({
        'Company Name': summary.index,
        'Stock Symbol': summary.index,
        'Last Signal': ['BUY' if get_signal(i)[0] == 'BUY' else 'SELL' for i in summary.index],
        'Accuracy (%)': summary['Accuracy (%)']
    })
    
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("अजून ट्रेड्स नाहीत. मार्केट ॲनालाइज करून ट्रेड्स सेव्ह कर, मग इथे टेबल दिसेल.")
