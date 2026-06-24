import streamlit as st
import pandas as pd
from database import get_history

st.title("📊 Professional Analytics Dashboard")

df = get_history()

if not df.empty:
    # 60 दिवसांचा फिल्टर
    df['date'] = pd.to_datetime(df['date'])
    df_60 = df[df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=60))]
    
    # मेनूबार
    menu = st.sidebar.radio("Select View", ["Top 10 Performers", "Full Trade Logs"])
    
    if menu == "Top 10 Performers":
        st.subheader("🏆 Top 10 Profitable Stocks")
        stats = df_60.groupby('stock').agg({'pnl': 'sum', 'result': 'count'})
        stats = stats.sort_values(by='pnl', ascending=False).head(10)
        # रेटिंग सिस्टिम
        stats['Rating'] = stats['pnl'].apply(lambda x: "⭐⭐⭐⭐⭐" if x > 5000 else "⭐⭐⭐⭐" if x > 2000 else "⭐⭐⭐")
        st.dataframe(stats, use_container_width=True) # हे एक्सेलसारखे टेबल दिसेल
        
    elif menu == "Full Trade Logs":
        st.subheader("📑 Detailed Trade Logs")
        st.dataframe(df, use_container_width=True)
        # एक्सेलमध्ये डाउनलोड करण्यासाठी बटण
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as Excel (CSV)", csv, "trades.csv", "text/csv")
else:
    st.warning("Data not found! Please save some trades first.")
