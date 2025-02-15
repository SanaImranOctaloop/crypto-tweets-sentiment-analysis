import aiohttp
import asyncio
from dotenv import load_dotenv
import os
import json
import nest_asyncio

nest_asyncio.apply()
load_dotenv()

RAPID_API_KEY = os.getenv("TWITTER_API_KEY")
if not RAPID_API_KEY:
    print("Error: TWITTER_API_KEY environment variable is not set.")
    exit(1)

url = "https://twitter-api45.p.rapidapi.com/search.php"
headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
}
keywords = ["$Trump", "$BTC", "$Sol", "$ETH"]
LIST_ID = "1889565942079721519"

async def fetch_tweets(session, keyword):
    params = {
        "query": keyword,
        "list_id": LIST_ID,  
        "limit": 10
    }
    async with session.get(url, headers=headers, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error fetching tweets for keyword {keyword}: {response.status}")
            return None

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_tweets(session, keyword) for keyword in keywords]
        results = await asyncio.gather(*tasks)
        
        tweets_data = []
        for result in results:
            if result and "timeline" in result: 
                for tweet in result["timeline"]:  
                    tweet_info = {
                        "text": tweet.get("text", ""), 
                        "username": tweet.get("screen_name", ""),  
                        "created_at": tweet.get("created_at", "") 
                    }
                    tweets_data.append(tweet_info)
        
        with open("fetched_tweets.json", "w", encoding="utf-8") as json_file:
            json.dump(tweets_data, json_file, indent=4, ensure_ascii=False)
            print("Fetched tweets saved to fetched_tweets.json")

asyncio.run(main())