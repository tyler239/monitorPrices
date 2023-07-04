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
            'trend' : '',
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
    
    def updateTrend(self, _token, trend) :
        #Just used when the token is created in the db
        if(trend) :
            self.collection.update_one({'token' : _token}, {'$set' : {'trend' : trend}})
            return
        if(self.getRecord(_token)['trend'] == 'up') :
            self.collection.update_one({'token' : _token}, {'$set' : {'trend' : 'down'}})
        else :
            self.collection.update_one({'token' : _token}, {'$set' : {'trend' : 'up'}})
    