from requests_html import HTMLSession
from mongoDb import MongoDB
from models import assetRecord
from crawlers import bitcoinPrice, ethereumPrice
from mathx import Mathx
import requests
import time

def str2float(price: str) :
    try : 
        a = ''.join([c for c in price if c.isdigit() or c == ','])
    except TypeError :
        return 0.0
    return float(a.replace(',', '.'))

def updateRecord(mongo : MongoDB, token : str, price : float) :
    #Get the record and update the values list
    record = assetRecord(**mongo.useDbCollection('prices','prices').getRecord(token))
    values = record.values
    len(values) >= 200 and values.pop(0)
    values.append(price)
    mongo.useDbCollection('prices','prices').updateValues(record.token, values)

    """
    #Update the trend
    mathx = Mathx(values, price)
    if(record.trend == 'up') :
        if(mathx.sma(200) > mathx.ema(50) and mathx.ema(50) > price) :
            mongo.useDbCollection('prices','prices').updateTrend(record.token)
            #Changing the trend to down
    elif(record.trend == 'down') :
        if(mathx.sma(200) < mathx.ema(50) and mathx.ema(50) < price) :
            mongo.useDbCollection('prices','prices').updateTrend(record.token)
            #Changing the trend to up
    else :
        if(mathx.sma(200) > mathx.ema(50)) : mongo.useDbCollection('prices','prices').updateTrend(record.token, 'down')
        else : mongo.useDbCollection('prices','prices').updateTrend(record.token,  'up')           
        #Setting the trend for the first time
    """

if __name__ == '__main__' :
    mongo = MongoDB()

    with open('tokens.csv', 'r') as file :
        for line in file.readlines() :
            for token in line.split(',') :
                token = token.strip()
                if not mongo.useDbCollection('prices','prices').existsRecord(token) :
                    mongo.useDbCollection('prices','prices').createRecord(token)
                
                for _ in range(3) :
                    r = requests.get(f'https://brapi.dev/api/quote/{token}')
                    if(r.status_code == 200) : 
                        updateRecord(mongo, token, r.json()['results'][0]['regularMarketPrice'])
                        break
                    time.sleep(1)
       