from pymongo import MongoClient
from .variables import variables_enviroment

class MongoDB:

    def __init__(self):
        self.client = MongoClient(variables_enviroment['mongo_uri'])