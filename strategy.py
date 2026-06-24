import yfinance as yf
import numpy as np

def get_signal(ticker):
    # ५ दिवसांचा डेटा
    df = yf.download(ticker, period="5d", interval="1h", progress=False)
    
    if df.empty or len(df) < 14: 
        return "HOLD", 0.0, 0.0
    
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # [महत्वाचा बदल]: .iloc[-1] वापरून थेट शेवटची व्हॅल्यू काढून ती float मध्ये बदलली आहे
    try:
        rsi_val = float(rsi_series.iloc[-1])
        current_price = float(df['Close'].iloc[-1])
        avg_vol = float(df['Volume'].rolling(window=5).mean().iloc[-1])
        curr_vol = float(df['Volume'].iloc[-1])
    except:
        return "HOLD", 0.0, 0.0

    # NaN चेक (आता हे float व्हॅल्यूवर होईल, त्यामुळे एरर येणार नाही)
    if np.isnan(rsi_val) or np.isnan(current_price):
        return "HOLD", current_price, 0.0
    
    # सिग्नल लॉजिक
    if rsi_val < 35 and curr_vol > avg_vol:
        return "BUY", current_price, rsi_val
    elif rsi_val > 65:
        return "SELL", current_price, rsi_val
    else:
        return "HOLD", current_price, rsi_val
