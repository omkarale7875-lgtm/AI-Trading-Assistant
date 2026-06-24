import yfinance as yf
import numpy as np

def get_signal(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)

        if df.empty or len(df) < 14:
            return "NO_DATA", 0.0, 0.0
        
        # RSI calculation
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        current_price = float(df['Close'].iloc[-1])
        current_rsi = float(rsi.iloc[-1])
        
        if current_rsi < 35: return "BUY", current_price, current_rsi
        elif current_rsi > 65: return "SELL", current_price, current_rsi
        else: return "HOLD", current_price, current_rsi
    except:
        return "ERROR", 0.0, 0.0
