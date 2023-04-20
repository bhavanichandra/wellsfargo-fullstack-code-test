from pymongo import MongoClient

from .settings import mongodb_uri

client = MongoClient(mongodb_uri)
db = client["wells_fargo"]


def get_collection(collection: str):
    collection_list = db.list_collection_names()
    if collection in collection_list:
        return db.get_collection(collection)
    else:
        return db.create_collection(collection)
