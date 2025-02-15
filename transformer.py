from transformers import pipeline
import json

print("Loading sentiment analysis pipeline with model: nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
)

with open("fetched_tweets.json", "r", encoding="utf-8") as json_file:
    tweets_data = json.load(json_file)

for tweet in tweets_data:
    result = sentiment_pipeline(tweet["text"])[0]
    # print(f"Tweet: {tweet['text']} -> Sentiment: {result}")
    tweet["sentiment"] = result["label"]
    tweet["confidence"] = result["score"]

with open("analyzed_tweets.json", "w", encoding="utf-8") as json_file:
    json.dump(tweets_data, json_file, indent=4, ensure_ascii=False)
    print("Analyzed tweets saved to analyzed_tweets.json")