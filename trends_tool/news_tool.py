from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
load_dotenv()

def get_news_articles_count(query):
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    data = search.get_dict()
    return len(data.get('news_results', []))

# if __name__ == "__main__":
#     res = get_news_articles_count("Nikola Tesla")
#     print(res)