import requests
from datetime import datetime
from sqlalchemy.orm import Session
from models.news_article import NewsArticle
import os

API_KEY = os.getenv("NEWSDATA_API_KEY")

def fetch_and_store_news(query: str, db: Session) -> int:
    if not API_KEY:
        raise ValueError("❌ NEWSDATA_API_KEY not set in environment.")

    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": API_KEY,
        "q": query,
        "language": "en",
        "category": "business,technology",
    }

    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get("results", [])

    stored = 0
    for item in articles:
        if not isinstance(item, dict):
            print("⚠️ Skipping non-dict item:", item)
            continue

        url = item.get("link")
        if not url:
            continue

        # Skip duplicates
        if db.query(NewsArticle).filter_by(url=url).first():
            continue

        # Parse and store
        try:
            published_at = None
            if item.get("pubDate"):
                published_at = datetime.fromisoformat(item["pubDate"].replace("Z", "+00:00"))

            article = NewsArticle(
                title=item.get("title", "Untitled"),
                description=item.get("description", ""),
                url=url,
                source=item.get("source_id", "unknown"),
                published_at=published_at,
            )

            db.add(article)
            stored += 1

        except Exception as e:
            print(f"❌ Error storing article: {e}")

    db.commit()
    print(f"✅ Stored {stored} new articles.")
    return stored
