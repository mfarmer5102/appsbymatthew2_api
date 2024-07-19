import os
import pymongo
import certifi

my_client = pymongo.MongoClient(os.getenv('MONGO_INSTANCE_URL', "mongodb://localhost:27017"), tlsCAFile=certifi.where())
database = my_client["apps_by_matthew"]