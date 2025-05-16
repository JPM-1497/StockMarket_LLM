from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.session import SessionLocal
from services.news_fetcher import fetch_and_store_news
from models.news_article import NewsArticle

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/fetch_news")
def fetch_news(query: str = Query(...), db: Session = Depends(get_db)):
    stored_count = fetch_and_store_news(query, db)
    return {"message": f"Stored {stored_count} new articles."}

@router.get("/news")
def get_news(
    keyword: str = Query(..., description="Keyword to search in title or description"),
    db: Session = Depends(get_db)
):
    # Step 1: Try fetching existing news from DB
    articles = db.query(NewsArticle).filter(
        (NewsArticle.title.ilike(f"%{keyword}%")) |
        (NewsArticle.description.ilike(f"%{keyword}%"))
    ).order_by(NewsArticle.published_at.desc()).limit(10).all()

    # Step 2: If none, trigger a fetch and retry
    if not articles:
        fetch_and_store_news(keyword, db)
        articles = db.query(NewsArticle).filter(
            (NewsArticle.title.ilike(f"%{keyword}%")) |
            (NewsArticle.description.ilike(f"%{keyword}%"))
        ).order_by(NewsArticle.published_at.desc()).limit(10).all()

    return [
        {
            "title": a.title,
            "description": a.description,
            "url": a.url,
            "source": a.source,
            "published_at": a.published_at.isoformat() if a.published_at else None
        }
        for a in articles
    ]