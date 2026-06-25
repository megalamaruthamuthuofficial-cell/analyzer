from pymongo import MongoClient


client = MongoClient(
    "mongodb+srv://megalambsccs7102007_db_user:3XjJnb0X9M3cnSas@cluster0.jzkwgge.mongodb.net/?appName=Cluster0"
)

db = client["sentiment_db"]

reviews_collection = db["reviews"]