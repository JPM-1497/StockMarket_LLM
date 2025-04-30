def generate_stock_insights(strategy):
    """
    Simple first version of AI stock insights.
    Later, replace this with LLM calls.
    """
    return (
        f"Analyzing strategy '{strategy.name}'...\n\n"
        f"This strategy targets the following stocks: {strategy.stocks}.\n"
        f"Entry Criteria: {strategy.entry_criteria}\n"
        f"Exit Criteria: {strategy.exit_criteria}\n\n"
        f"Notes: {strategy.notes}\n\n"
        f"✅ Recommendation: Monitor trading volume and earnings reports for these stocks."
    )
