import yfinance as yf
import numpy as np

def get_signal(ticker, period="30d"):
    try:
        # NSE डेटासाठी अधिक स्टेबल पद्धत
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(period=period, interval="1d")
        
        if df.empty or len(df) < 14:
            return "NO_DATA", 0.0, 0.0
        
        # RSI Calculation
        close = df['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        rs = gain / loss.replace(0, np.nan)
        rsi_series = 100 - (100 / (1 + rs))
        
        rsi_val = float(rsi_series.iloc[-1])
        price = float(close.iloc[-1])
        
        # स्ट्रॅटेजी (RSI < 30: BUY, > 70: SELL)
        if rsi_val < 30: return "BUY", price, rsi_val
        elif rsi_val > 70: return "SELL", price, rsi_val
        else: return "HOLD", price, rsi_val
            
    except Exception as e:
        return f"ERROR", 0.0, 0.0
