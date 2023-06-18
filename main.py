from requests_html import HTMLSession
import pandas as pd
from mongoDb import MongoDB
from models import assetRecord
from crawlers import bitcoinPrice, ethereumPrice


def str2float(price: str) :
    try : 
        a = ''.join([c for c in price if c.isdigit() or c == ','])
    except TypeError :
        return 0.0
    return float(a.replace(',', '.'))

def updateRecord(mongo : MongoDB, token : str, price : float) :
    record = assetRecord(**mongo.useDbCollection('prices','prices').getRecord(token))
    values = record.values
    len(values) >= 200 and values.pop(0)
    values.append(price)
    mongo.useDbCollection('prices','prices').updateValues(record.token, values)
    price > record.max_value and mongo.useDbCollection('prices','prices').updateMaxValue(record.token, price)
    price < record.min_value and mongo.useDbCollection('prices','prices').updateMinValue(record.token, price)

if __name__ == '__main__' :
    s = HTMLSession()
    mongo = MongoDB()
    assets = {'bitcoin' : bitcoinPrice, 'ethereum' : ethereumPrice}

    for token, crawler in assets.items() :
        if mongo.useDbCollection('prices','prices').existsRecord(token) :
            updateRecord(mongo, token, str2float(crawler(s)))
        else :
            mongo.useDbCollection('prices','prices').createRecord(token)