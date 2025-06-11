import os
import ast
import logging
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)

def summarize_stock_comparison(results: dict, user_query: str) -> str:
    """
    Uses OpenAI GPT to summarize stock comparison results using openai>=1.0.0 syntax.
    """
    if not results:
        return "No valid stock data was found for comparison."

    lines = []
    for symbol, data in results.items():
        prices = data.get("daily", [])
        if not prices or len(prices) < 2:
            continue

        sorted_prices = sorted(prices, key=lambda x: x["date"])
        start_price = sorted_prices[0]["close"]
        end_price = sorted_prices[-1]["close"]

        try:
            pct_change = ((end_price - start_price) / start_price) * 100
            lines.append(f"- {symbol}: {pct_change:.2f}%")
        except ZeroDivisionError:
            continue

    if not lines:
        return "No valid data available for meaningful comparison."

    data_text = "\n".join(lines)

    prompt = f"""
You are a financial assistant. A user has asked to compare stock performance.
Here are the results of their request:

User Query: {user_query}

Stock Performance:
{data_text}

Write a short, human-like summary comparing these stocks. Be clear and concise.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
        logging.info("✅ LLM summary generated successfully")
        return summary

    except Exception as e:
        logging.error(f"❌ Error generating summary: {e}")
        return f"Error generating summary: {e}"


def filter_tickers_with_llm(user_query: str, candidate_tickers: list[str]) -> list[str]:
    """
    Uses OpenAI to filter a list of candidate tickers based on the user's intent.
    Returns a refined list of symbols relevant to the prompt.
    """
    if not candidate_tickers:
        return []

    prompt = f"""
User query: "{user_query}"
Candidate tickers: {', '.join(candidate_tickers)}

Which of these are most relevant to the user's question? 
Return only a Python list of stock symbols (e.g., ["TSLA", "NIO", "RIVN"]).
Do not include any explanation or extra text.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=100
        )

        raw_output = response.choices[0].message.content.strip()
        tickers = ast.literal_eval(raw_output)
        if isinstance(tickers, list) and all(isinstance(t, str) for t in tickers):
            return tickers
        else:
            return candidate_tickers  # fallback

    except Exception as e:
        logging.warning(f"⚠️ Error filtering tickers with LLM: {e}")
        return candidate_tickers  # fallback
