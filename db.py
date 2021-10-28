
import pymongo


CLIENT = pymongo.MongoClient("mongodb://localhost:27017/")
DB = CLIENT["scheduling"]
