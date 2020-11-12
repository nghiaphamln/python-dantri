import pymongo


def connect_database():
    # mongodb+srv://nghiaph:nghia123@cluster0.szulm.mongodb.net/
    # mongodb://localhost:27017/
    my_client = pymongo.MongoClient('mongodb+srv://nghiaph:nghia123@cluster0.szulm.mongodb.net/')
    my_database = my_client['dantri']
    my_collection = my_database['news']
    return my_collection


def insert_database(key, value, database):
    database.update_one(key, value, upsert=True)
