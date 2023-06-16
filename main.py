from requests_html import HTMLSession
from dotenv import dotenv_values
import pandas as pd
from MongoDB import MongoDB


config = dotenv_values('.env')


def str2float(price) :
    a = ''.join([c for c in price if c.isdigit() or c == ','])
    return float(a.replace(',', '.'))


def justTry(func) :
    def wrapper(*args, **kwargs) :
        try :
            return func(*args, **kwargs)
        except Exception as e :
            print(f'Error in the {func.__name__} function. Error : {e}')
    return wrapper


#Long time period curve
def sma(prices, days) :
    return sum(prices[-days:]) / days

#Signal curve
def ema(prices, days) :
    d = {'prices' : prices}
    df = pd.DataFrame(d)
    return df.ewm(span = days).mean().iloc[-1]['prices']



@justTry
def bitcoinPrice(s : HTMLSession) :
    url = 'https://www.google.com/search?q=bitcoin+price'
    r = s.get(url, headers={'User-Agent': config['USER_AGENT']})
    price = r.html.find('div.card-section > div + div > span', first = True).text
    return price
      

@justTry
def ethereumPrice(s : HTMLSession) :
    url = 'https://www.google.com/search?q=ethereum+price'
    r = s.get(url, headers={'User-Agent': config['USER_AGENT']})
    price = r.html.find('div.card-section > div + div > span', first = True).text
    return price

if __name__ == '__main__' :

    s = HTMLSession()
    mongo = MongoDB()

   
   #Bitcoin
    if(mongo.useDbCollection('prices','prices').getRecord('bitcoin') != None) :
        bitcoinRecord = mongo.useDbCollection('prices','prices').getRecord('bitcoin')
        values = bitcoinRecord['values']
        len(values) >= 200 and values.pop(0)

        price = str2float(bitcoinPrice(s))
        values.append(price)

        mongo.useDbCollection('prices','prices').updateValues('bitcoin', values)
        price > bitcoinRecord['max_value'] and mongo.useDbCollection('prices','prices').updateMaxValue('bitcoin', price)
        price < bitcoinRecord['min_value'] and mongo.useDbCollection('prices','prices').updateMinValue('bitcoin', price)
    else : 
        mongo.useDbCollection('prices','prices').createRecord('bitcoin')

    #Ethereum
    if(mongo.useDbCollection('prices','prices').getRecord('ethereum') != None) :
        ethereumRecord = mongo.useDbCollection('prices','prices').getRecord('ethereum')
        values = ethereumRecord['values']
        len(values) >= 200 and values.pop(0)

        price = str2float(ethereumPrice(s))
        values.append(price)

        mongo.useDbCollection('prices','prices').updateValues('ethereum', values)
        price > ethereumRecord['max_value'] and mongo.useDbCollection('prices','prices').updateMaxValue('ethereum', price)
        price < ethereumRecord['min_value'] and mongo.useDbCollection('prices','prices').updateMinValue('ethereum', price)
    else :
        mongo.useDbCollection('prices','prices').createRecord('ethereum')
    
