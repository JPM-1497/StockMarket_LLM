
# backend/api/compare.py

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from utils.query_parser import extract_tickers_and_dates
from models.historical_price import HistoricalPrice
from models.stock import Stock
from services.llm_orchestrator import summarize_stock_comparison

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

    # Only fetch and include stocks that were explicitly matched
    comparison_data = {}
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

    return {
        "query": query,
        "tickers": tickers,
        "start_date": start_date,
        "end_date": end_date,
        "results": comparison_data,
        "summary": summarize_stock_comparison(comparison_data, query)
    }
