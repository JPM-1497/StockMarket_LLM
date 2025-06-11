# backend/services/sql_data_fetcher.py

import logging
from sqlalchemy.orm import Session
from models.historical_price import HistoricalPrice
from models.stock import Stock  # ✅ Needed for join
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def get_stock_performance_data(
    db: Session, 
    tickers: List[str], 
    start_date: datetime = None, 
    end_date: datetime = None
) -> Dict[str, Dict]:
    """
    Fetch historical prices for given tickers and date range.
    Returns a dictionary with daily prices, start/end price, and percent change.
    """
    logging.info(f"📥 Fetching price data for tickers: {tickers}")
    logging.info(f"📅 Date range: {start_date} to {end_date}")

    query = (
        db.query(HistoricalPrice)
        .join(HistoricalPrice.stock)
        .filter(Stock.symbol.in_(tickers))
    )

    if start_date:
        query = query.filter(HistoricalPrice.date >= start_date)
    if end_date:
        query = query.filter(HistoricalPrice.date <= end_date)

    records = query.all()
    logging.info(f"📊 Total records fetched: {len(records)}")

    # Group records by symbol
    grouped: Dict[str, List[HistoricalPrice]] = {}
    for record in records:
        symbol = record.stock.symbol
        grouped.setdefault(symbol, []).append(record)

    result: Dict[str, Dict] = {}
    for symbol, entries in grouped.items():
        sorted_entries = sorted(entries, key=lambda r: r.date)
        start_price = sorted_entries[0].close
        end_price = sorted_entries[-1].close
        pct_change = ((end_price - start_price) / start_price) * 100 if start_price else 0

        daily = [
            {
                "date": r.date.isoformat(),
                "close": float(r.close),
                "volume": int(r.volume) if r.volume else None
            }
            for r in sorted_entries
        ]

        result[symbol] = {
            "start_price": float(start_price),
            "end_price": float(end_price),
            "pct_change": round(pct_change, 2),
            "daily": daily
        }

    logging.info(f"✅ Aggregated result for {len(result)} tickers.")
    return result

