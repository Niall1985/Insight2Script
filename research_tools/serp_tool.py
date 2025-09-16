import time
import os
import json
from serpapi import GoogleSearch
from research_agent.serp_content_extractor import llm
from dotenv import load_dotenv
from requests.exceptions import HTTPError
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

load_dotenv()

def extract_video_id(url : str) -> str:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v")
    if video_id:
        return video_id[0] 
    return None

def get_transcript(video_id: str) -> str:
    try:
        video_content = ""
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        for snippet in fetched_transcript:
            video_content += snippet.text
        return video_content
    except Exception as e:
        return f"Error: Could not retrieve transcript. {e}"
    
def safe_llm_call(link: str, max_retries: int = 3, backoff_factor: int = 2) -> str:
    attempt = 0
    wait_time = 1 

    while attempt < max_retries:
        try:
            return llm(link)

        except HTTPError as e:
            print(f"[HTTPError] Attempt {attempt + 1} for link {link}: {str(e)}")

        except Exception as e:
            print(f"[Error] Attempt {attempt + 1} for link {link}: {str(e)}")

        attempt += 1
        time.sleep(wait_time)
        wait_time *= backoff_factor  

    return f"Failed to fetch content from {link} after {max_retries} attempts.\n"


def get_youtube_links(query: str) -> str:
    serp_content = ""
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    video_links = []
    for video in results.get('video_results', [])[:5]:
        video_links.append({"link": video.get('link')})

    print(video_links)
    for video in video_links:
        video_id = extract_video_id(video["link"])
        transcript = get_transcript(video_id)
        # serp_content += safe_llm_call(transcript)
        time.sleep(1)  

    return transcript


