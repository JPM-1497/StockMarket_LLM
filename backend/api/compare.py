
# backend/api/compare.py

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from utils.query_parser import extract_tickers_and_dates
from models.historical_price import HistoricalPrice
from models.stock import Stock
from services.llm_orchestrator import summarize_stock_comparison
from services.news_fetcher import get_recent_news_for_stock

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/compare_stocks")
def compare_stocks(query: str = Query(...), db: Session = Depends(get_db)):
    try:
        tickers, start_date, end_date = extract_tickers_and_dates(query, db)
    except ValueError as e:
        return {"error": str(e)}

    comparison_data = {}
    news_data = {}  # ✅ Store news per stock

    for ticker in tickers:
        stock = db.query(Stock).filter(Stock.symbol == ticker).first()
        prices = db.query(HistoricalPrice).join(Stock).filter(
            Stock.symbol == ticker,
            HistoricalPrice.date >= start_date,
            HistoricalPrice.date <= end_date
        ).order_by(HistoricalPrice.date).all()

        if stock and prices:
            pct_change = ((prices[-1].close - prices[0].close) / prices[0].close) * 100
            comparison_data[ticker] = {
                "name": stock.name,
                "start_price": prices[0].close,
                "end_price": prices[-1].close,
                "pct_change": round(pct_change, 2)
            }

            # ✅ Add news fetching here
            news_data[ticker] = get_recent_news_for_stock(stock.name, db)

    return {
        "query": query,
        "tickers": tickers,
        "start_date": start_date,
        "end_date": end_date,
        "results": comparison_data,
        "news": news_data,  # ✅ Include news in response
        "summary": summarize_stock_comparison(comparison_data, query)
    }