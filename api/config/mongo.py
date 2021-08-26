from pymongo import MongoClient


class MongoDB:

    def __init__(self):
        self.client = MongoClient("mongodb+srv://firetest-api:4sUY2oJLIeBtyHxY@mdz-document.gpkdw.mongodb.net/firetest?retryWrites=true&w=majority")