from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from pytube import YouTube
from googleapiclient.discovery import build
import os
from urllib.parse import urlparse, parse_qs

load_dotenv()


api_key = os.getenv("yt_api")
youtube = build("youtube", "v3", developerKey=api_key)

def extract_video_id(url : str) -> str:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v")
    if video_id:
        return video_id[0] 
    return None

def get_video_info(video_id):
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        if not response["items"]:
            return {"error": "Video not found"}
        
        item = response["items"][0]
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        return {
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published": snippet["publishedAt"],
            "views": stats.get("viewCount"),
            "likes": stats.get("likeCount", "Hidden")
        }
    except Exception as e:
        return {"error": str(e)}


def get_youtube_video_links(query):
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    data = search.get_dict()

    video_results = data.get('video_results', [])
    links = [video.get('link') for video in video_results if 'link' in video]
    
    return links

def yt_tool_main(query):
    result_arr = []
    videos = get_youtube_video_links(query)

    for video in videos:
        video_id = extract_video_id(video)
        result = get_video_info(video_id)
        result_arr.append(result)

    output_lines = []
    for i, res in enumerate(result_arr, start=1):
        if "error" in res:
            output_lines.append(f"Video {i}: Error - {res['error']}")
        else:
            output_lines.append(
                f"Video {i}:\n"
                f"Title: {res['title']}\n"
                f"Channel: {res['channel']}\n"
                f"Published: {res['published']}\n"
                f"Views: {res['views']}\n"
                f"Likes: {res['likes']}\n"
                f"{'-'*50}"
            )
    
    return "\n".join(output_lines)

    
