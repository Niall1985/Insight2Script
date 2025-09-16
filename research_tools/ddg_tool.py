from ddgs import DDGS
from research_agent.ddgs_scraper import scrape_site_text

def extract_ddg_results(prompt):
    content = ""
    url_results = []
    results = DDGS().text(prompt, max_results=5)
    for r in results:
        url_results.append(r['href'])
    
    for r in url_results:
        content += scrape_site_text(r)
    
    return content

# if __name__ == "__main__":
#     content = extract_ddg_results("Nikola Tesla")
#     print(content)
    
    
