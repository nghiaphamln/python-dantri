import pymongo


# kết nối cơ sở dữ liệu
def connect_database(collection):
    my_client = pymongo.MongoClient('mongodb+srv://nghiaph:nghia123@cluster0.szulm.mongodb.net/')
    my_database = my_client['dantri']
    return my_database[collection]


# insert database (nếu tồn tại => cập nhật)
def insert_database(key, value, database):
    database.update_one(key, value, upsert=True)
