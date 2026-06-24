import yfinance as yf
import numpy as np

def get_signal(ticker):
    # डेटा डाउनलोड
    df = yf.download(ticker, period="1mo", interval="1d", progress=False)
    
    # डेटा चेक: जर डेटा नसेल किंवा रिकामी असेल तर 'HOLD' पाठवा
    if df.empty or len(df) < 30: 
        return "HOLD", 0.0, 0.0
    
    # RSI कॅल्क्युलेशन (NaN व्हॅल्यूज काढून टाकण्यासाठी dropna वापरा)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # व्हॅल्यूज काढणे आणि ती 'NaN' आहे का हे तपासणे
    rsi_val = rsi_series.iloc[-1]
    current_price = df['Close'].iloc[-1]
    
    # व्हॉल्युम सुरक्षितपणे काढणे
    avg_vol = df['Volume'].rolling(window=5).mean().iloc[-1]
    curr_vol = df['Volume'].iloc[-1]

    # जर कोणतीही व्हॅल्यू NaN असेल, तर HOLD करा
    if np.isnan(rsi_val) or np.isnan(current_price):
        return "HOLD", float(current_price), 0.0
    
    # आता खात्रीशीरपणे float मध्ये रूपांतरित करा
    rsi_float = float(rsi_val)
    price_float = float(current_price)
    vol_avg = float(avg_vol)
    vol_curr = float(curr_vol)
    
    # सिग्नल लॉजिक
    if rsi_float < 35 and vol_curr > vol_avg:
        return "BUY", price_float, rsi_float
    elif rsi_float > 65:
        return "SELL", price_float, rsi_float
    else:
        return "HOLD", price_float, rsi_float
