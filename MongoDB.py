import pymongo
from dotenv import dotenv_values

config = dotenv_values('.env')

class MongoDB :
    def __init__(self) :
        self.host = config['MONGO_HOST']
        self.port = int(config['MONGO_PORT'])
        self.password = config['MONGO_PASSWORD']
        self.client = pymongo.MongoClient(host = self.host, port = self.port)
    
    #returns the cursor
    def useDbCollection(self, _db, _collection) :
        self.collection = self.client[_db][_collection]
        return self

    def createRecord(self, _token) :
        record = {
            'values' : [0.0] * 200,
            'max_value' : 0.0, 
            'min_value' : float('inf'),
            'token' : _token
        }
        self.collection.insert_one(record)
        return self
    
    def getRecord(self, _token) :
        return self.collection.find_one({'token' : _token})
    
    def existsRecord(self, _token) :
        return self.getRecord(_token) != None

    def updateValues(self, _token, _value) :
        self.collection.update_one({'token' : _token}, {'$set' : {'values' : _value}})
        return self
    
    def updateMaxValue(self, _token, _value) :
        self.collection.update_one({'token' : _token}, {'$set' : {'max_value' : _value}})
        return self
    
    def updateMinValue(self, _token, _value) :
        self.collection.update_one({'token' : _token}, {'$set' : {'min_value' : _value}})
        return self
    