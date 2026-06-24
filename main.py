import streamlit as st
import pandas as pd
from strategy import get_signal
from database import init_db, save_trade, get_history

st.set_page_config(page_title="AI Trader Pro", layout="wide")
init_db()

st.title("🤖 AI-QUANT TRADER PRO")

# १. युजरसाठी डेट सिलेक्शन ऑप्शन्स
date_options = {
    "Last Day": "1d", "2 Days": "2d", "5 Days": "5d", 
    "10 Days": "10d", "15 Days": "15d", "30 Days": "30d", 
    "45 Days": "45d", "60 Days": "60d"
}
selected_range = st.selectbox("Select Analysis Range", list(date_options.keys()))
period = date_options[selected_range]

# २. स्टॉक सिलेक्शन
ticker = st.selectbox("Select Stock", ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS'])

if st.button("🚀 Analyze Market"):
    # आता period सुद्धा आपण पास करत आहोत
    signal, price, rsi = get_signal(ticker, period)
    st.metric("Price", f"₹{price:,.2f}", f"RSI: {rsi:.2f}")
    st.subheader(f"Signal: {signal}")

# ३. एक्सेल स्टाईल परफॉर्मन्स टेबल (Main Dashboard)
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
    
    # टेबल तयार करणे
    display_df = pd.DataFrame({
        'Company Name': summary.index,
        'Stock Symbol': summary.index,
        'Signal Status': [get_signal(i, period)[0] for i in summary.index],
        'Accuracy (%)': summary['Accuracy (%)']
    })
    
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("मार्केट ॲनालाइज करून ट्रेड्स सेव्ह कर, मग इथे टेबल दिसेल.")
