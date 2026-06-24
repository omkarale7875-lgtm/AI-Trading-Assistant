import yfinance as yf
import numpy as np

def get_signal(ticker, period="30d"): # येथे period इनपुट म्हणून घेतला
    try:
        df = yf.download(ticker, period=period, interval="1d", progress=False)
        
        if df.empty: return "NO_DATA", 0.0, 0.0
        
        # RSI Calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi_series = 100 - (100 / (1 + rs))
        
        rsi_val = float(rsi_series.iloc[-1])
        price = float(df['Close'].iloc[-1])
        
        if rsi_val < 35: return "BUY", price, rsi_val
        elif rsi_val > 65: return "SELL", price, rsi_val
        else: return "HOLD", price, rsi_val
    except:
        return "ERROR", 0.0, 0.0
