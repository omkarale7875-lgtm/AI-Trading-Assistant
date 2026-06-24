import streamlit as st
import pandas as pd

def init_db():
    if 'trades_df' not in st.session_state:
        # सुरुवातीला रिकामा डेटा फ्रेम
        st.session_state['trades_df'] = pd.DataFrame(columns=['date', 'stock', 'result', 'pnl'])

def save_trade(stock, result, pnl):
    new_trade = pd.DataFrame({'date': [pd.Timestamp.now().strftime('%Y-%m-%d')], 
                              'stock': [stock], 'result': [result], 'pnl': [pnl]})
    st.session_state['trades_df'] = pd.concat([st.session_state['trades_df'], new_trade], ignore_index=True)

def get_history():
    if 'trades_df' not in st.session_state:
        init_db()
    return st.session_state['trades_df']
