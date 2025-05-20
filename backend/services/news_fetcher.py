import requests
from datetime import datetime
from sqlalchemy.orm import Session
from models.news_article import NewsArticle
from typing import List
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

    if response.status_code != 200:
        print(f"❌ News API error: {response.status_code} - {response.text}")
        return 0

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

        if db.query(NewsArticle).filter_by(url=url).first():
            continue

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


def get_recent_news_for_stock(stock_name: str, db: Session, limit: int = 5) -> List[dict]:
    """Fetch and return recent news for a stock, triggering fetch if none exists."""
    articles = db.query(NewsArticle).filter(
        (NewsArticle.title.ilike(f"%{stock_name}%")) |
        (NewsArticle.description.ilike(f"%{stock_name}%"))
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()

    if not articles:
        fetch_and_store_news(stock_name, db)
        articles = db.query(NewsArticle).filter(
            (NewsArticle.title.ilike(f"%{stock_name}%")) |
            (NewsArticle.description.ilike(f"%{stock_name}%"))
        ).order_by(NewsArticle.published_at.desc()).limit(limit).all()

    return [
        {
            "title": a.title,
            "description": a.description,
            "url": a.url,
            "published_at": a.published_at.isoformat() if a.published_at else None
        }
        for a in articles
    ]
