from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Superior API Active", "owner": "Oday-Eng", "version": "2.0"}

@app.get("/analyze")
def analyze(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. تحليل الكلمات المفتاحية (أكثر 5 كلمات تكراراً)
        words = re.findall(r'\w+', soup.get_text().lower())
        common_words = Counter([w for w in words if len(w) > 3]).most_common(5)

        # 2. فحص الروابط
        links = soup.find_all('a')
        internal_links = [link.get('href') for link in links if link.get('href') and url in link.get('href')]

        # 3. فحص الميتا (Meta Tags)
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        return {
            "target_url": url,
            "security": {"is_https": url.startswith("https")},
            "seo_elements": {
                "title": soup.title.string if soup.title else "Missing Title",
                "meta_description": meta_desc['content'] if meta_desc else "Missing Description",
                "h1_count": len(soup.find_all('h1')),
                "images_count": len(soup.find_all('img'))
            },
            "content_analysis": {
                "top_keywords": common_words,
                "total_links": len(links),
                "internal_links_count": len(internal_links)
            },
            "health_score": "High" if meta_desc and soup.title else "Needs Improvement"
        }
    except Exception as e:
        return {"error": str(e)}
