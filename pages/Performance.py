import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from database import get_history
# बाकीचा तुझा कोड जसा आहे तसा खाली राहू दे...
st.title("📊 Performance & Analytics")
df = get_history()

if not df.empty:
    wins = len(df[df['result'] == 'PROFIT'])
    total = len(df)
    accuracy = (wins / total) * 100
    
    col1, col2 = st.columns(2)
    col1.metric("Total Accuracy", f"{accuracy:.2f}%")
    col2.metric("Total Trades", total)
    
    st.dataframe(df.style.background_gradient(subset=['pnl'], cmap='RdYlGn'))
else:
    st.info("No data yet!")
