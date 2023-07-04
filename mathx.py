import pandas as pd
from typing import List

class Mathx :
    def __init__(self, prices : List[float], current : float) :
        self.current = current
        self.prices = prices

    #Long time period curve 200
    def sma(prices, days) :
        return sum(prices[-days:]) / days

    #Signal curve 50
    def ema(prices, days) :
        d = {'prices' : prices}
        df = pd.DataFrame(d)
        return df.ewm(span = days).mean().iloc[-1]['prices']

    def bearMarket(current : float, max_value : float) :
        return current < max_value * 0.8

    def bullMarket(current : float, min_value : float) :
        return current > min_value * 1.2