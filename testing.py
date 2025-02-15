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

print("Loading sentiment analysis pipeline with model: nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
)

def get_sentiment(text):
    try:
        if cached_result := cache.get(text):
            return json.loads(cached_result)
        result = sentiment_pipeline(text)[0]
        # print(f"Tweet: {text} -> Sentiment: {result}")
        cache.set(text, json.dumps(result))
        return result
    except Exception as e:
        print(f"Error during sentiment analysis or caching: {e}")
        return None

tweet_text = "Just bought $BTC! Excited about the future of crypto."
if sentiment := get_sentiment(tweet_text):
    print(f"Sentiment for tweet: {sentiment}")

def analyze_and_cache_tweets(tweets_data):
    for tweet in tweets_data:
        if text := tweet.get("text", ""):
            if sentiment_result := get_sentiment(text):
                tweet["sentiment"] = sentiment_result["label"]
                tweet["confidence"] = sentiment_result["score"]
            else:
                tweet["sentiment"] = "ERROR"
                tweet["confidence"] = 0.0
    return tweets_data

if __name__ == "__main__":
    try:
        with open("fetched_tweets.json", "r", encoding="utf-8") as json_file:
            tweets_data = json.load(json_file)
        analyzed_tweets = analyze_and_cache_tweets(tweets_data)
        with open("analyzed_tweets_with_caching.json", "w", encoding="utf-8") as json_file:
            json.dump(analyzed_tweets, json_file, indent=4, ensure_ascii=False)
            print("Analyzed tweets with caching saved to analyzed_tweets_with_caching.json")
    
    except FileNotFoundError:
        print("Error: 'fetched_tweets.json' not found. Ensure the file exists.")
    except Exception as e:
        print(f"Unexpected error: {e}")