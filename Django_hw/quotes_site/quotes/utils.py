from pymongo import MongoClient


def get_mongodb():
    client = MongoClient("mongodb://localhost")

    db = client.Quotes_site

    return db
