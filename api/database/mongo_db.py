from api.config.mongo import MongoDB as mongoConnect

class MongoDatabase:

    def __init__(self):
        self.__mongoConnect = mongoConnect().client
        self.__db = self.__mongoConnect.firetest
        self.__questions_collection = self.__db.questions
        self.__users_collection = self.__db.users
        self.__dict_collection = {
            "questions": self.__questions_collection,
            "users": self.__users_collection
        }

    async def insert_one(self, collection_name, inserted_object, return_id=False):
        collection = self.__dict_collection[collection_name]
        return  return_id and collection.insert_one(inserted_object).inserted_id or collection.insert_one(inserted_object)

    async def get_one(self, collection_name, query_object, return_with_id=False):
        collection = self.__dict_collection[collection_name]
        return return_with_id and collection.find_one(query_object) or collection.find_one(query_object, {'_id': 0})

    async def update_one(self, collection_name, query_object, inserted_object):
        collection = self.__dict_collection[collection_name]
        return collection.update_one(query_object, inserted_object)
