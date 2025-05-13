from sqlalchemy.orm import Session
from models.historical_price import HistoricalPrice
from datetime import datetime
from typing import List, Tuple

def fetch_price_data(db: Session, tickers: List[str], start_date: datetime, end_date: datetime):
    results = (
        db.query(
            HistoricalPrice.ticker,
            HistoricalPrice.date,
            HistoricalPrice.close
        )
        .filter(
            HistoricalPrice.ticker.in_(tickers),
            HistoricalPrice.date >= start_date,
            HistoricalPrice.date <= end_date
        )
        .order_by(HistoricalPrice.ticker, HistoricalPrice.date)
        .all()
    )

    price_map = {}
    for ticker, date, close in results:
        price_map.setdefault(ticker, []).append({"date": str(date), "close": close})
    return price_map

def summarize_price_data(price_map: dict) -> str:
    lines = []
    for ticker, data in price_map.items():
        if len(data) < 2:
            lines.append(f"{ticker}: Not enough data")
            continue

        start_price = data[0]["close"]
        end_price = data[-1]["close"]
        pct_change = ((end_price - start_price) / start_price) * 100
        lines.append(f"{ticker}: {pct_change:.2f}% from {data[0]['date']} to {data[-1]['date']}")
    return "\n".join(lines)

def build_comparison_prompt(user_question: str, price_summary: str, stock_summaries: dict) -> str:
    lines = [f"User Question: {user_question}", "", "Stock Performance:"]
    lines.append(price_summary)
    lines.append("\nCompany Context:")
    for ticker, summary in stock_summaries.items():
        lines.append(f"{ticker}: {summary}")
    lines.append("\nAnswer in plain English which stock is better and why:")
    return "\n".join(lines)
