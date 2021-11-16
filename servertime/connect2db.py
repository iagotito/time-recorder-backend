import pymongo

MONGO_URL = "mongodb://localhost:27017/time_recorder"

MONGO_CLIENT = pymongo.MongoClient(MONGO_URL)

BD_NAME = MONGO_CLIENT._MongoClient__default_database_name
TIME_RECORDER_DB = MONGO_CLIENT[BD_NAME]
