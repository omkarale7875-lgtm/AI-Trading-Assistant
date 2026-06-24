import streamlit as st
import pandas as pd
from database import get_history

st.set_page_config(page_title="Advanced Analytics", layout="wide")

# Sidebar Menu
menu = st.sidebar.selectbox("Select View", ["Top 10 Performers", "Daily Trade Stats", "Overall P&L"])
df = get_history()

if df.empty:
    st.info("No trade data available yet!")
else:
    if menu == "Top 10 Performers":
        st.title("🏆 Top 10 Profitable Stocks")
        # 60 दिवसांचा फिल्टर
        df['date'] = pd.to_datetime(df['date'])
        last_60_days = df[df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=60))]
        
        # ग्रुपिंग आणि रेटिंग
        stats = last_60_days.groupby('stock').agg({'pnl': 'sum', 'result': 'count'})
        stats['rating'] = stats['pnl'].apply(lambda x: "⭐⭐⭐⭐⭐" if x > 5000 else "⭐⭐⭐⭐" if x > 2000 else "⭐⭐⭐")
        
        top_10 = stats.sort_values(by='pnl', ascending=False).head(10)
        st.table(top_10)

    elif menu == "Daily Trade Stats":
        st.title("📈 Daily Buy/Sell Signals")
        df['date'] = pd.to_datetime(df['date'])
        daily = df.groupby(['date', 'result']).size().unstack(fill_value=0)
        st.bar_chart(daily)
        st.table(daily)

    elif menu == "Overall P&L":
        st.title("💰 Profit & Loss Summary")
        total_profit = df[df['pnl'] > 0]['pnl'].sum()
        total_loss = df[df['pnl'] < 0]['pnl'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Profit", f"₹{total_profit:,.2f}")
        col2.metric("Total Loss", f"₹{abs(total_loss):,.2f}")
        col3.metric("Net Profit", f"₹{total_profit + total_loss:,.2f}")
