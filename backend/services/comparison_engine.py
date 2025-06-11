# backend/services/comparison_engine.py

import logging
from fastapi.responses import JSONResponse
from utils.query_parser import extract_tickers_and_dates
from services.sql_data_fetcher import get_stock_performance_data
# from services.vector_context_fetcher import get_company_summaries
from services.llm_orchestrator import summarize_stock_comparison, filter_tickers_with_llm

# Qdrant + sentence-transformers setup
from services.qdrant_client import qdrant
from services.embedding_encoder import sentence_encoder
from db.session import get_db
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)

def compare_stocks(user_query: str):
    logging.info("✅ compare_stocks() triggered")

    # Step 1: Extract tickers and date range using alias + semantic fallback
    db: Session = next(get_db())
    try:
        tickers, start_date, end_date = extract_tickers_and_dates(
            query=user_query,
            db=db,
            qdrant_client=qdrant,
            encoder=sentence_encoder
        )
    except ValueError as e:
        return str(e)

    if not tickers:
        logging.warning("⚠️ No tickers were extracted.")
        return "Sorry, I couldn't identify any stock symbols to compare."

    logging.info(f"🔍 Initial extracted tickers: {tickers}")

    # Step 2: Refine tickers using LLM
    refined_tickers = filter_tickers_with_llm(user_query, tickers)
    logging.info(f"✅ LLM-filtered tickers: {refined_tickers}")
    tickers = refined_tickers

    # Step 3: Fetch SQL-based stock performance
    performance_data = get_stock_performance_data(db, tickers, start_date, end_date)

    # ✅ Check type and content BEFORE summary generation
    if not isinstance(performance_data, dict) or not performance_data:
        logging.warning("⚠️ No valid stock performance data retrieved.")
        return "No valid stock data was found for comparison."

    logging.info(f"📊 Retrieved performance data for {len(performance_data)} tickers")

    # Step 4: Get context from vector DB (optional)
    summaries = {}  # get_company_summaries(tickers) — disabled for now
    logging.info("📚 Skipping vector summaries (none provided)")

    # Step 5: Generate LLM summary
    response = summarize_stock_comparison(performance_data, user_query)
    logging.info("✅ LLM summary generated successfully")

    return JSONResponse(content={
        "summary": response,
        "results": performance_data
    })
