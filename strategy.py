import yfinance as yf
import numpy as np

# स्ट्रॅटेजीमध्ये period हे optional ठेवले आहे जेणेकरून एरर येणार नाही
def get_signal(ticker, period="30d"):
    try:
        # डेटा डाउनलोड (Interval 1d)
        df = yf.download(ticker, period=period, interval="1d", progress=False)
        
        if df.empty or len(df) < 20:
            return "HOLD", 0.0, 0.0
        
        # RSI स्ट्रॅटेजी: 30 पेक्षा कमी (Oversold - Buy), 70 पेक्षा जास्त (Overbought - Sell)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        # झिरो डिव्हिजन टाळण्यासाठी
        rs = gain / loss.replace(0, np.nan)
        rsi_series = 100 - (100 / (1 + rs))
        
        rsi_val = float(rsi_series.iloc[-1])
        price = float(df['Close'].iloc[-1])
        
        # [Profit-Focused Logic]
        # जर RSI < 30 असेल तरच BUY, 70 च्या वर असेल तरच SELL
        if rsi_val < 30:
            return "BUY", price, rsi_val
        elif rsi_val > 70:
            return "SELL", price, rsi_val
        else:
            return "HOLD", price, rsi_val
            
    except Exception:
        return "HOLD", 0.0, 0.0
