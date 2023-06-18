import pandas as pd

#Long time period curve
def sma(prices, days) :
    return sum(prices[-days:]) / days

#Signal curve
def ema(prices, days) :
    d = {'prices' : prices}
    df = pd.DataFrame(d)
    return df.ewm(span = days).mean().iloc[-1]['prices']

def bearMarket(current : float, max_value : float) :
    return current < max_value * 0.8

def bullMarket(current : float, min_value : float) :
    return current > min_value * 1.2