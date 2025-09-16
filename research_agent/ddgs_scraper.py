import requests
from bs4 import BeautifulSoup
import re


def scrape_site_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        paragraphs = soup.find_all('p')
        text = '\n\n'.join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        text = re.sub(r'\n\s*\n', '\n\n', text).strip()
        return text[:5000]
    
    except Exception as e:
        return f"Error Scraping {url}: {e}"
    