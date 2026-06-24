import streamlit as st
from database import get_history

st.title("🏆 TOP 10 PROFITABLE STOCKS")
df = get_history()

if not df.empty:
    # फक्त प्रॉफिट वाले ट्रेड्स फिल्टर करणे
    profit_df = df[df['result'] == 'PROFIT']
    
    # स्टॉकनुसार एकूण प्रॉफिटची बेरीज
    top_stocks = profit_df.groupby('stock')['pnl'].sum().sort_values(ascending=False).head(10)
    
    st.write("### तुझ्या स्ट्रॅटेजीनुसार टॉप १० परफॉर्मर्स:")
    st.table(top_stocks)
else:
    st.info("अजून पुरेसा डेटा नाही. काही ट्रेड्स लॉग कर, मग मी तुला टॉप १० लिस्ट देईन.")
