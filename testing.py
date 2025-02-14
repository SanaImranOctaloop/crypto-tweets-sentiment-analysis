import redis, json
from transformers import pipeline

cache = redis.Redis(host='localhost', port=8000, decode_responses=True)

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