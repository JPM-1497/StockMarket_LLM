import pandas as pd
import sys
import os
from datetime import datetime
import logging
from tqdm import tqdm
import yfinance as yf
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# Ensure /app is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.session import SessionLocal
from models.stock import Stock
from models.historical_price import HistoricalPrice

def fetch_historical_prices(ticker: str, start_year="2000-01-01") -> list[dict]:
    try:
        df = yf.download(ticker, start=start_year, interval="1d", auto_adjust=False)
        if df.empty:
            return []

        df.reset_index(inplace=True)
        df.columns = [col[0].title() if isinstance(col, tuple) else col.title() for col in df.columns]
 # Normalize column casing

        prices = []
        for _, row in df.iterrows():
            prices.append({
                "date": row["Date"],
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            })
        return prices
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {e}")
        return []

def save_prices_to_db(db: Session, stock: Stock, price_data: list[dict]):
    for row in price_data:
        db_price = HistoricalPrice(
            stock_id=stock.id,
            date=row["date"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
        )
        db.add(db_price)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logging.warning(f"Duplicate data skipped for {stock.symbol}")

def main():
    db: Session = SessionLocal()
    stocks = db.query(Stock).all()

    logging.info(f"📈 Fetching historical prices for {len(stocks)} stocks since 2000...\n")

    for stock in tqdm(stocks):
        try:
            prices = fetch_historical_prices(stock.symbol)
            if prices:
                save_prices_to_db(db, stock, prices)
        except Exception as e:
            logging.error(f"❌ Failed for {stock.symbol}: {e}")
    db.close()
    logging.info("🎉 All done.")

if __name__ == "__main__":
    main()
