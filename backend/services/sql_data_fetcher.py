# backend/services/sql_data_fetcher.py

from sqlalchemy.orm import Session
from models.historical_price import HistoricalPrice
from typing import List, Dict, Tuple
from datetime import datetime


def fetch_price_data(
    db: Session, 
    tickers: List[str], 
    start_date: datetime = None, 
    end_date: datetime = None
) -> Dict[str, List[Dict]]:
    """
    Fetch historical prices for given tickers and date range.
    Returns a dictionary mapping each ticker to its list of daily prices.
    """
    query = db.query(HistoricalPrice).filter(HistoricalPrice.symbol.in_(tickers))

    if start_date:
        query = query.filter(HistoricalPrice.date >= start_date)
    if end_date:
        query = query.filter(HistoricalPrice.date <= end_date)

    records = query.all()

    result: Dict[str, List[Dict]] = {}
    for record in records:
        if record.symbol not in result:
            result[record.symbol] = []

        result[record.symbol].append({
            "date": record.date.isoformat(),
            "close": float(record.close),
            "volume": int(record.volume) if record.volume else None,
        })

    return result
