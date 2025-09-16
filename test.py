# from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
# from urllib.parse import urlparse, parse_qs

# def extract_video_id(url: str) -> str | None:
#     parsed_url = urlparse(url)
#     query_params = parse_qs(parsed_url.query)
#     video_id = query_params.get("v")
#     return video_id[0] if video_id else None


# def get_transcript_text(video_url: str) -> str:
#     video_id = extract_video_id(video_url)
#     if not video_id:
#         return "Invalid video URL."

#     try:
#         transcript = YouTubeTranscriptApi.list_transcripts(video_id) \
#                                          .find_transcript(['en']) \
#                                          .fetch()
#         return " ".join(entry['text'] for entry in transcript)

#     except NoTranscriptFound:
#         return "No transcript available."

#     except Exception as e:
#         return f"Error fetching transcript: {str(e)}"


# if __name__ == "__main__":
#     url = "https://www.youtube.com/watch?v=FeUA-0G1p5k"
#     transcript = get_transcript_text(url)
#     print(transcript)

# from research_tools.serp_tool import get_youtube_links
# transcript = get_youtube_links("Nikola Tesla")
# print(transcript)
