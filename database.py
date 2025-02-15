from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://Sana:445457@democluster.vld9i.mongodb.net/?retryWrites=true&w=majority&appName=DemoCluster")
db = client["cryptocurrency_sentiment_analysis"]
collection = db["tweets"]

with open("analyzed_tweets.json", "r", encoding="utf-8") as json_file:
    tweets_data = json.load(json_file)

result = collection.insert_many(tweets_data)
print(f"Inserted {len(result.inserted_ids)} tweets into MongoDB")

collection.create_index([("created_at", 1)])