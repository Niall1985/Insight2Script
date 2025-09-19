import google.generativeai as genai
import os
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()

key = os.getenv('gemini_api2')
genai.configure(api_key=key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")


def llm(all_data: dict) -> list:
    prompt = f"""
You are given aggregated data about a topic. 
Analyze it and return only a Python-style list in the exact format below:

[
  main_score,          # overall trendiness score (0–100)
  score_2018,          # estimated score for 2018
  score_2019,
  score_2020,
  score_2021,
  score_2022,
  score_2023,
  score_2024,
  score_2025,
  "short reasoning summary"
]

### Data Provided:
{all_data}

### Important:
- Return only the list, no extra text, no explanation.
- Ensure all scores are integers (0–100).
"""

    response = model.generate_content(prompt)
    
    output = response.text.strip()
    if output.startswith("```"):
        output = output.split("```")[1].strip()
    
    try:
        parsed = eval(output) 
        return parsed
    except Exception as e:
        return [None, f"Parsing error: {e}", output]
