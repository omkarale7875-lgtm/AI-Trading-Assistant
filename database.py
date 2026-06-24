import sqlite3
import pandas as pd
import os

# डेटाबेस फाईलचे ठिकाण सध्याच्या फोल्डरमध्ये सेट करा
db_path = os.path.join(os.path.dirname(__file__), 'trading.db')

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades 
                 (date TEXT, stock TEXT, result TEXT, pnl REAL)''')
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM trades", conn)
    conn.close()
    return df
