import google.generativeai as genai
import os
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()

key = os.getenv('gemini_api')
genai.configure(api_key=key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


def llm(link: str) -> str:
    prompt = f"""You are an intelligent content extraction agent.
Your task is to take a YouTube video transcript as input, extract all available textual content from the video 
(including transcript, captions, description, and comments if available), and analyze it to produce the output:
Detailed Summary: A comprehensive, structured summary of the key points and main ideas presented in the video.
Make sure the detailed summary covers the most important topics in logical order, provides context, 
and explains any technical terms clearly. Just return the summary text, nothing else.

Video transcript: {link}
"""
    response = model.generate_content(prompt)
    return response.text
