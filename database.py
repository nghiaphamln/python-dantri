import pymongo


def connect_database():
    my_client = pymongo.MongoClient('mongodb://localhost:27017/')
    my_database = my_client['dantri']
    my_collection = my_database['news']
    return my_collection


def insert_database(key, value, database):
    database.update_one(key, value, upsert=True)
