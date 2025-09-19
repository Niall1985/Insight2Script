import google.generativeai as genai
import os
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()

key = os.getenv('content_api')
genai.configure(api_key=key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


def content_llm(ddg_summary, wiki_summary, youtube_summary):
    prompt = f"""You are an advanced script-generation agent that creates engaging YouTube video scripts based on provided input data and your external general knowledge.
You will receive data from multiple sources about a subject (e.g., DuckDuckGo search results, Wikipedia content, YouTube transcripts) and your task is to combine these inputs with additional information you have been trained on to generate a compelling, structured script.
The final script should be organized and flow smoothly for a YouTube audience, covering the following sections in a logical and engaging order:
1. Hook – An intriguing, attention-grabbing sentence or question that entices viewers to keep watching.
2. Introduction to the Subject – Briefly introduce who or what the subject is.
3. Background: Life, Childhood, or Early History – Provide relevant early life or background information.
4. Major Success – Describe key achievements or turning points.
5. Challenges and Failures – Discuss significant failures or obstacles.
6. Rivalry or Conflicts – Highlight important rivalries, conflicts, or controversies.
7. Connecting the Hook – Tie the hook back to the narrative, emphasizing how success, failure, or rivalry shaped the story.
8. Conclusion and Call to Action – Summarize the key takeaways and provide a strong ending, possibly with a question or suggestion to engage the audience further.

Output Requirements:
Write in a conversational yet professional tone suitable for a YouTube audience.
Make it easy to understand, structured with paragraphs or bullet points where appropriate.
Avoid repeating facts unnecessarily.
Do not include metadata or explain the process, only output the final script.
Example Input:
ddg_results: {ddg_summary}
wiki_results: {wiki_summary}
youtube_results: {youtube_summary}
Generate a high-quality video script that flows naturally, integrating this information along with your general knowledge to create a captivating narrative.
"""
    response = model.generate_content(prompt)
    return response.text
