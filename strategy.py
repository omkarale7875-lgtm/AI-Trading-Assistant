import yfinance as yf

def get_signal(ticker):
    df = yf.download(ticker, period="1mo", interval="1d", progress=False)
    if df.empty: return "HOLD", 0, 0
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    
    rsi_val = float(rsi_series.iloc[-1]) # इथे एरर येत होती, ती फिक्स केली
    current_price = float(df['Close'].iloc[-1])
    avg_vol = float(df['Volume'].rolling(window=5).mean().iloc[-1])
    curr_vol = float(df['Volume'].iloc[-1])
    
    if rsi_val < 35 and curr_vol > avg_vol:
        return "BUY", current_price, rsi_val
    elif rsi_val > 65:
        return "SELL", current_price, rsi_val
    return "HOLD", current_price, rsi_val
