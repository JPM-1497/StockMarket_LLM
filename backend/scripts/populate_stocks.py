import sys
import os
import pandas as pd
import yfinance as yf
from tqdm import tqdm
from sqlalchemy.orm import Session
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

# Make sure /app is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.session import SessionLocal
from models.stock import Stock

def get_sp500_tickers() -> list[str]:
    """Fetch S&P 500 tickers from Wikipedia."""
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)
    df = table[0]
    tickers = df['Symbol'].tolist()

    # Yahoo Finance replaces "." with "-" in tickers
    cleaned_tickers = [ticker.replace('.', '-') for ticker in tickers]
    return cleaned_tickers

def save_stocks_to_db(tickers: list[str]):
    """Save a list of tickers with their company names and summaries to the database, skipping duplicates."""
    db: Session = SessionLocal()

    for ticker_symbol in tqdm(tickers, desc="Saving stocks to DB"):
        try:
            # Skip if stock already exists
            if db.query(Stock).filter_by(symbol=ticker_symbol).first():
                continue

            stock_info = yf.Ticker(ticker_symbol).info
            company_name = stock_info.get('shortName')
            summary = stock_info.get('longBusinessSummary')

            if company_name:
                db_stock = Stock(
                    symbol=ticker_symbol,
                    name=company_name,
                    summary=summary,
                    created_at=datetime.utcnow()
                )
                db.add(db_stock)

        except Exception as e:
            logging.error(f"❌ Error fetching {ticker_symbol}: {e}")

    db.commit()
    db.close()



def main():
    logging.info("🔎 Fetching S&P 500 tickers...")
    tickers = get_sp500_tickers()
    logging.info(f"✅ Fetched {len(tickers)} tickers.")

    logging.info("💾 Saving stocks to database...")
    save_stocks_to_db(tickers)
    logging.info("🎉 Done saving stocks!")

if __name__ == "__main__":
    main()
