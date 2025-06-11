import sys
import os
import pandas as pd
import yfinance as yf
from tqdm import tqdm
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import time

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
    """Save a list of tickers with their company names, sectors, and summaries to the database, skipping duplicates."""
    db: Session = SessionLocal()

    for ticker_symbol in tqdm(tickers, desc="Saving stocks to DB"):
        try:
            # Skip if stock already exists
            existing = db.query(Stock).filter_by(symbol=ticker_symbol).first()
            
            if existing and existing.sector and existing.summary:
                continue

            stock_info = yf.Ticker(ticker_symbol).info
            company_name = stock_info.get('shortName')
            summary = stock_info.get('longBusinessSummary')
            sector = stock_info.get('sector')

            if not sector:
                logging.warning(f"⚠️  Missing sector for {ticker_symbol}")
            if not summary:
                logging.warning(f"⚠️  Missing summary for {ticker_symbol}")

            if company_name:
                db_stock = Stock(
                    symbol=ticker_symbol,
                    name=company_name,
                    summary=summary,
                    sector=sector,
                    created_at=datetime.utcnow()
                )
                db.add(db_stock)

            time.sleep(0.5)  # Be respectful to Yahoo API

        except Exception as e:
            logging.error(f"❌ Error fetching {ticker_symbol}: {e}")

    db.commit()
    db.close()

def update_all_sectors_and_summaries():
    db: Session = SessionLocal()
    all_stocks = db.query(Stock).all()

    logging.info(f"🔁 Rechecking all {len(all_stocks)} stocks for sector/summary...")

    for stock in tqdm(all_stocks, desc="Refreshing sector/summary"):
        try:
            yf_data = yf.Ticker(stock.symbol).info
            updated = False

            if yf_data.get("sector"):
                stock.sector = yf_data["sector"]
                updated = True
            if yf_data.get("longBusinessSummary"):
                stock.summary = yf_data["longBusinessSummary"]
                updated = True

            if updated:
                logging.info(f"✅ Updated {stock.symbol}")
            else:
                logging.warning(f"⚠️ Still no data for {stock.symbol}")

            time.sleep(0.5)

        except Exception as e:
            logging.error(f"❌ Error updating {stock.symbol}: {e}")

    db.commit()
    db.close()
    logging.info("🎯 Finished full recheck of all stocks.")



def main():
    logging.info("🔎 Fetching S&P 500 tickers...")
    tickers = get_sp500_tickers()
    logging.info(f"✅ Fetched {len(tickers)} tickers.")

    logging.info("💾 Saving stocks to database...")
    save_stocks_to_db(tickers)
    logging.info("🎉 Done saving stocks!")

    logging.info("🔄 Attempting to fill in missing sector/summary values...")
    update_all_sectors_and_summaries()



if __name__ == "__main__":
    main()
