# Script to download transcripts that have already been made for SED

import os
import re
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import euclidean_distances
import textract

# Connect to DB
envHost = os.environ['MONGO_DB_HOST']
envPort = os.environ['MONGO_DB_PORT']
envDB = os.environ['MONGO_DB_DATABASE']
dbURL = 'mongodb://' + envHost + ':' + envPort + '/' + envDB
client = MongoClient(dbURL)
db = client.get_database()

#TODO some pdfs are wrong, error check them
transcriptBasePath = './transcripts/'

# Download PDF transcripts
for post in db.posts.find():
    transcript_url = ''
    text = post["content"]["rendered"]
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    for url in urls:
        url = str(url)
        if url.find(".pdf") != -1:
            transcript_url = url
            break
    if transcript_url == '':
        continue
    try:
        # Read PDF
        writer = PdfFileWriter()
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        remoteFile = urlopen(Request(transcript_url, headers=hdr)).read()
        memoryFile = StringIO(remoteFile)
        pdfFile = PdfFileReader(memoryFile)
        for pageNum in xrange(pdfFile.getNumPages()):
            currentPage = pdfFile.getPage(pageNum)
            writer.addPage(currentPage)
        outputStream = open(transcriptBasePath + post["slug"] + ".pdf","wb")
        writer.write(outputStream)
        outputStream.close()
    except:
        print("ERROR with " + transcript_url)
        continue