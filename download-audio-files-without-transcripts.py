# Script to download mp3 audio files for which we do not have a transcription

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

transcriptBasePath = './transcripts/'
generatedTranscriptBasePath = './generated_transcripts/'

existing_transcripts = []

for filename in os.listdir(transcriptBasePath):
    existing_transcripts.append(filename[:-4])
    
for filename in os.listdir(generatedTranscriptBasePath):
    existing_transcripts.append(filename[:-4])

limit = 10
for post in db.posts.find():
    if(post["slug"] in existing_transcripts):
        continue
    try:
        urllib.urlretrieve (post['mp3'], './raw_mp3_episodes/' + post['slug'] + '.mp3')
    except:
        print "PROBLEM with " + post["title"]["rendered"]
        continue
    limit -= 1
    if limit == 0:
        break