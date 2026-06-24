import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('trading.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades 
                 (date TEXT, stock TEXT, result TEXT, pnl REAL)''')
    conn.commit()
    conn.close()

def save_trade(stock, result, pnl):
    conn = sqlite3.connect('trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO trades VALUES (date('now'), ?, ?, ?)", (stock, result, pnl))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('trading.db')
    df = pd.read_sql_query("SELECT * FROM trades", conn)
    conn.close()
    return df
