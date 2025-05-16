import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_stock_comparison(results: dict, user_query: str) -> str:
    """
    Uses OpenAI GPT to summarize stock comparison results using openai>=1.0.0 syntax.
    """

    if not results:
        return "No valid stock data was found for comparison."

    lines = []
    for symbol, data in results.items():
        pct = data.get("pct_change")
        name = data.get("name")
        if pct is not None and name:
            lines.append(f"- {name} ({symbol}): {pct:.2f}%")

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
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating summary: {e}"
