from transformers import pipeline

print("Loading sentiment analysis pipeline with model: nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
)

tweet_text = "don't know about the future of  #SOL crypto."
result = sentiment_pipeline(tweet_text)[0]

print(f"Sentiment for tweet: {result}")