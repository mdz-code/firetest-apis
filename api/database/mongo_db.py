from ..config.mongo import MongoDB as mongoConnect
from ..database.schemas import SimulateBase


class MongoDatabase:

    def __init__(self):
        self.__mongoConnect = mongoConnect().client
        self.__db = self.__mongoConnect.firetest
        self.__questions_collection = self.__db.questions
        self.__users_collection = self.__db.users,
        self.__simulates_collection = self.__db.simulates
        self.__dict_collection = {
            "questions": self.__questions_collection,
            "users": self.__users_collection,
            "simulates": self.__simulates_collection
        }

    async def insert_one(self, collection_name, inserted_object, return_id=False):
        collection = self.__dict_collection[collection_name]
        return return_id and collection.insert_one(inserted_object).inserted_id or collection.insert_one(inserted_object)

    async def get_one(self, collection_name, query_object, return_with_id=False) -> SimulateBase:
        collection = self.__dict_collection[collection_name]
        return return_with_id and collection.find_one(query_object) or collection.find_one(query_object, {'_id': 0})

    async def complex_query(self, collection_name, **kwargs):
        pipelines = await self.__build_pipeline(kwargs)
        collection = self.__dict_collection[collection_name]
        # return collection.find_one(pipelines)
        return {
            "selected_questions": True
        }

    async def __build_pipeline(self, kwargs):
        pipeline_dict = {
            "$and": []
        }

        for k in kwargs:
            if k != "questions":
                appended_dict = { "$or": []}
                for value in kwargs[k]:
                    appended_dict["$or"].append({ k: value })

                    if len(appended_dict["$or"]) > 0:
                        pipeline_dict["$and"].append(appended_dict)


            if k == "questions":
                appended_dict = { "$or": []}
                for value in kwargs[k]:
                    appended_dict["$or"].append({ k: { "$not": value }})

                    if len(appended_dict["$or"]) > 0:
                        pipeline_dict["$and"].append(appended_dict)

        return pipeline_dict

    async def update_one(self, collection_name, query_object, inserted_object):
        collection = self.__dict_collection[collection_name]
        return collection.update_one(query_object, { "$set": inserted_object})
