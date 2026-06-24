import yfinance as yf
import numpy as np

def get_signal(ticker):
    # ५ दिवसांचा डेटा घेतला आहे ज्यामुळे ॲप सुपर-फास्ट चालेल
    df = yf.download(ticker, period="5d", interval="1h", progress=False)
    
    if df.empty or len(df) < 14: 
        return "HOLD", 0.0, 0.0
    
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # सुरक्षित व्हॅल्यू काढणे
    rsi_val = rsi_series.iloc[-1]
    current_price = df['Close'].iloc[-1]
    
    # व्हॉल्युम डेटा
    avg_vol = df['Volume'].rolling(window=5).mean().iloc[-1]
    curr_vol = df['Volume'].iloc[-1]

    # NaN चेक
    if np.isnan(rsi_val) or np.isnan(current_price):
        return "HOLD", float(current_price), 0.0
    
    rsi_f = float(rsi_val)
    price_f = float(current_price)
    
    # सिग्नल लॉजिक
    if rsi_f < 35 and curr_vol > avg_vol:
        return "BUY", price_f, rsi_f
    elif rsi_f > 65:
        return "SELL", price_f, rsi_f
    else:
        return "HOLD", price_f, rsi_f
