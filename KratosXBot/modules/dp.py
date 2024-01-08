# KratosXBot/KratosXBot/modules/db.py

from pymongo import MongoClient
import certifi
import os

mongo_uri = os.environ.get('MONGO_DB_URI')
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

# You can now use `client` to interact with your database.
