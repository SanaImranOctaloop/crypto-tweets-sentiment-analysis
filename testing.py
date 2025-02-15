import redis
import json
from transformers import pipeline


try:
    cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

    cache.ping()
except redis.exceptions.ConnectionError as e:
    print("Redis connection failed. Ensure Redis is running and accessible.")
    print(f"Error: {e}")
    exit(1)

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased")

def get_sentiment(text):
    cached_result = cache.get(text)
    if cached_result:
        return json.loads(cached_result)
    
    result = sentiment_pipeline(text)[0]
    cache.set(text, json.dumps(result))
    return result

tweet_text = "Just bought $BTC! Excited about the future of crypto."
sentiment = get_sentiment(tweet_text)
print(sentiment)