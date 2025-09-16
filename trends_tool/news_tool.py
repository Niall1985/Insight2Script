from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
load_dotenv()

def get_news_articles_count(query, api_key):
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    data = search.get_dict()
    return len(data.get('news_results', []))
