from services.query_parser import extract_comparison_entities
from services.sql_data_fetcher import get_stock_performance_data
from services.vector_context_fetcher import get_company_summaries
from services.llm_orchestrator import generate_comparison_summary

def compare_stocks(user_query: str):
    # Step 1: Extract tickers and date range
    tickers, start_date, end_date = extract_comparison_entities(user_query)
    if not tickers:
        return "Sorry, I couldn't identify any stock symbols to compare."

    # Step 2: Fetch SQL-based stock performance
    performance_data = get_stock_performance_data(tickers, start_date, end_date)

    # Step 3: Get context from vector DB (summaries)
    summaries = get_company_summaries(tickers)

    # Step 4: Generate comparison response using LLM
    response = generate_comparison_summary(user_query, performance_data, summaries)
    return response
