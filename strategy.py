import yfinance as yf

def get_signal(ticker):
    df = yf.download(ticker, period="1mo", interval="1d", progress=False)
    if df.empty: return "HOLD", 0, 0
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    current_price = df['Close'].iloc[-1]
    avg_vol = df['Volume'].rolling(window=5).mean().iloc[-1]
    curr_vol = df['Volume'].iloc[-1]
    
    if rsi.iloc[-1] < 35 and curr_vol > avg_vol:
        return "BUY", float(current_price), float(rsi.iloc[-1])
    elif rsi.iloc[-1] > 65:
        return "SELL", float(current_price), float(rsi.iloc[-1])
    return "HOLD", float(current_price), float(rsi.iloc[-1])
