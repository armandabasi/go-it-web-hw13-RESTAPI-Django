import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_site.settings")
django.setup()

from quotes.models import Quote, Tag, Author

client = MongoClient("mongodb://localhost")

db = client.Quotes_site

authors = db.authors.find()

for autor in authors:
    Author.objects.get_or_create(
        fullname=autor["fullname"],
        born_date=autor["born_date"],
        born_location=autor["born_location"],
        description=autor["description"]
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        el, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(el)

    exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))

    if not exist_quote:
        author = db.authors.find_one({"_id": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(
            quote=quote["quote"],
            author=a
        )

        for tag in tags:
            q.tags.add(tag)
