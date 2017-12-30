# Script to generate CSV of slug, mp3

import os
import urllib
from pymongo import MongoClient

# Connect to DB
envHost = os.environ['MONGO_DB_HOST']
envPort = os.environ['MONGO_DB_PORT']
envDB = os.environ['MONGO_DB_DATABASE']
dbURL = 'mongodb://' + envHost + ':' + envPort + '/' + envDB
client = MongoClient(dbURL)
db = client.get_database()

lines = []

for post in db.posts.find():
    try:
        slug = post["slug"]
        mp3 = post["mp3"]
        lines.append(slug + ',' + mp3 + '/n')
    except:
        "failed on " + post["slug"]

print lines