# data/symbol_filter.py

def get_watchlist(name: str) -> list:
    """
    Returns a list of symbols for a given watchlist name.
    For now, this is a stub — you could later extend this to load from a file or database.
    """
    # Example watchlists (you can add more as needed)
    watchlists = {
        "tech": ["AAPL", "MSFT", "GOOGL", "AMZN"],
        "auto": ["TSLA", "GM", "F"],
        "finance": ["JPM", "BAC", "C"]
    }
    return watchlists.get(name.lower(), [])

def filter_symbols_by_activity(date: str, symbol_data: dict) -> list:
    """
    Filters symbols based on activity on a given date.
    'symbol_data' is a dictionary where keys are symbols and values are lists of dates
    when signals or trades occurred.
    
    This stub returns symbols with activity on the specified date.
    """
    active_symbols = []
    for symbol, dates in symbol_data.items():
        if date in dates:
            active_symbols.append(symbol)
    return active_symbols

# Example usage:
if __name__ == "__main__":
    tech_watchlist = get_watchlist("tech")
    print("Tech Watchlist:", tech_watchlist)
    
    # Suppose we have a dummy symbol activity log:
    dummy_activity = {
        "AAPL": ["2025-03-28", "2025-03-27"],
        "MSFT": ["2025-03-26"],
        "GOOGL": ["2025-03-28"]
    }
    active = filter_symbols_by_activity("2025-03-28", dummy_activity)
    print("Active symbols on 2025-03-28:", active)
