import json
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb://localhost")

db = client.Quotes_site

with open("quotes.json", "r", encoding="utf-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    autor = db.authors.find_one({"fullname": quote["author"]})
    if autor:
        db.quotes.insert_one({
            "quote": quote["quote"],
            "tags": quote["tags"],
            "author": ObjectId(autor["_id"])
        })