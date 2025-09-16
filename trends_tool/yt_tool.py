from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
load_dotenv()

def get_youtube_videos_count(query, api_key):
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    data = search.get_dict()
    return len(data.get('video_results', []))
