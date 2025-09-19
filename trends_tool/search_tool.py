from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
load_dotenv()

def get_web_total_results(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv('serp_api')
    }
    search = GoogleSearch(params)
    data = search.get_dict()
    return int(data.get('search_information', {}).get('total_results', 0))

# if __name__ == "__main__":
#     res = get_web_total_results("Nikola Tesla")
#     print(res)
