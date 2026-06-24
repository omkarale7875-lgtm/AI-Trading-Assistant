import yfinance as yf

def get_signal(ticker):
    # डेटा डाउनलोड
    df = yf.download(ticker, period="1mo", interval="1d", progress=False)
    
    # जर डेटा नसेल तर सुरक्षित एक्झिट
    if df.empty or len(df) < 30: 
        return "HOLD", 0.0, 0.0
    
    # RSI कॅल्क्युलेशन
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # सुरक्षित व्हॅल्यू काढणे (Series मधून एक सिंगल नंबर काढणे)
    rsi_val = float(rsi_series.iloc[-1])
    current_price = float(df['Close'].iloc[-1])
    
    # व्हॉल्युम सुरक्षितपणे काढणे
    avg_vol = float(df['Volume'].rolling(window=5).mean().iloc[-1])
    curr_vol = float(df['Volume'].iloc[-1])
    
    # इथे आता आपण थेट float व्हॅल्यू वापरत आहोत, त्यामुळे ValueError येणार नाही
    if rsi_val < 35 and curr_vol > avg_vol:
        return "BUY", current_price, rsi_val
    elif rsi_val > 65:
        return "SELL", current_price, rsi_val
    else:
        return "HOLD", current_price, rsi_val
