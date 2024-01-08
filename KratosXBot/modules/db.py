# db.py - Database Configuration

from pymongo import MongoClient
import certifi
import os

# Fetch the MongoDB connection URI from the environment variable
mongo_uri = os.environ.get('MONGO_DB_URI')

# Create a MongoDB client using the certifi CA bundle for SSL
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
