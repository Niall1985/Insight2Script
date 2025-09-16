from serpapi import GoogleSearch
import json
import os
from dotenv import load_dotenv
load_dotenv()

def get_youtube_links(query, num_results=5):
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    video_links = []
    for video in results.get('video_results', [])[:num_results]:
        video_links.append({
            # "title": video.get('title'),
            "link": video.get('link')
        })

    return video_links

# if __name__ == "__main__":
#     query = "Nikola Tesla"
#     videos = get_youtube_links(query)
#     print(videos)
