from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SEO Checker API is Running!"}

@app.get("/analyze")
def analyze(url: str):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            "url": url,
            "title": soup.title.string if soup.title else "No title found",
            "h1_count": len(soup.find_all('h1')),
            "status_code": response.status_code
        }
    except Exception as e:
        return {"error": str(e)}
