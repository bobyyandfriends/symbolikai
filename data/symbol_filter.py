#!/usr/bin/env python3
def get_watchlist(name: str) -> list:
    """
    Returns a list of symbols for the given watchlist name. 
    Simple dictionary approach for demonstration.
    """
    watchlists = {
        "tech": ["AAPL", "MSFT", "GOOGL", "AMZN"],
        "auto": ["TSLA", "GM", "F"],
        "finance": ["JPM", "BAC", "C"]
    }
    return watchlists.get(name.lower(), [])

def filter_symbols_by_activity(date: str, symbol_data: dict) -> list:
    """
    Return symbols that had 'date' in their activity list.
    'symbol_data': { 'AAPL':['2025-03-01','2025-03-15'], ... }
    """
    active = []
    for sym, dates in symbol_data.items():
        if date in dates:
            active.append(sym)
    return active

if __name__ == "__main__":
    # example
    w = get_watchlist("tech")
    print("Tech watchlist:", w)
