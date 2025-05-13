# backend/services/llm_orchestrator.py

from transformers import pipeline
import json

# Load the FLAN-T5 model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

def summarize_stock_comparison(results: dict, user_query: str) -> str:
    """
    Use FLAN-T5 to summarize the comparison results into a human-readable format.
    """

    # Filter only tickers mentioned in user_query
    user_query_lower = user_query.lower()
    filtered = {
        symbol: data
        for symbol, data in results.items()
        if symbol.lower() in user_query_lower
           or data["name"].lower() in user_query_lower
    }

    if not filtered:
        filtered = results  # fallback to include all

    comparison_text = "\n".join(
        f"- {symbol} ({data['name']}): {data['pct_change']}% from {round(data['start_price'], 2)} to {round(data['end_price'], 2)}"
        for symbol, data in filtered.items()
    )

    # Few-shot example prompt
    prompt = f"""
You are an expert financial analyst.

Here are example comparisons:
Example A:
Input:
- AAPL (Apple Inc.): +14.2% from 150.0 to 171.3
- MSFT (Microsoft Corp.): +10.5% from 280.0 to 309.4

Output:
Apple outperformed Microsoft in the given period, showing a stronger price increase of 14.2% vs. 10.5%.

Example B:
Input:
- TSLA (Tesla, Inc.): -18.5% from 300.0 to 244.5
- F (Ford Motor Company): -5.2% from 14.5 to 13.8

Output:
Both Tesla and Ford declined, but Tesla dropped more sharply with an 18.5% loss compared to Ford's 5.2%.

Now analyze this set:

{comparison_text}

Summarize the performance in one or two sentences comparing the stocks clearly and informatively.
"""

    try:
        response = generator(prompt.strip(), max_length=256, do_sample=False)[0]["generated_text"]
        return response.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"
