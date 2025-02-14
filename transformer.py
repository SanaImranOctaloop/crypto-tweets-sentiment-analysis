from transformers import pipeline
import json


sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")

with open("fetched_tweets.json", "r", encoding="utf-8") as json_file:
    tweets_data = json.load(json_file)

tweet_texts = [tweet["text"] for tweet in tweets_data]

results = sentiment_pipeline(tweet_texts)

for i, tweet in enumerate(tweets_data):
    tweet["sentiment"] = results[i]["label"]
    tweet["confidence"] = results[i]["score"]

with open("analyzed_tweets.json", "w", encoding="utf-8") as json_file:
    json.dump(tweets_data, json_file, indent=4, ensure_ascii=False)
    print("Analyzed tweets saved to analyzed_tweets.json")
    
