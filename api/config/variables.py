import os

variables_enviroment = {
    "mongo_uri": os.environ.get('mongo_uri'),
    "postgres_uri": os.environ.get('postgres_uri')
}