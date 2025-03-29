#!/usr/bin/env python3
import pandas as pd

class BacktestContext:
    """
    A class to hold and update the simulation state during a backtest.
    This context tracks:
      - initial capital and current cash,
      - a simple equity curve,
      - active (open) positions,
      - and a log of closed trades.
    """
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.equity_curve = [initial_capital]
        self.active_positions = []  # List to hold open trades
        self.trade_log = []         # List to hold closed trades
        self.current_time = None    # Current simulation time

    def open_position(self, trade: dict):
        """
        Register a new open position.
        'trade' is expected to be a dictionary containing trade details (e.g., entry_time, entry_price).
        Optionally, you can deduct capital from cash if your strategy requires.
        """
        self.active_positions.append(trade)
        # Example: Deduct capital for the trade (if needed)
        # self.cash -= trade.get('allocated_capital', 0)

    def close_position(self, trade: dict, profit: float):
        """
        Close an open position.
        Removes the trade from active_positions, logs it, and updates cash and the equity curve.
        'profit' is the profit (or loss) realized from this trade.
        """
        if trade in self.active_positions:
            self.active_positions.remove(trade)
        self.trade_log.append(trade)
        self.cash += profit
        # Update equity: For simplicity, we assume equity equals current cash.
        self.equity_curve.append(self.cash)

    def update_time(self, new_time):
        """
        Update the current simulation time.
        """
        self.current_time = new_time

    def get_equity_curve(self) -> pd.DataFrame:
        """
        Return the equity curve as a DataFrame.
        Here we simply index the equity values sequentially.
        """
        return pd.DataFrame({
            'time_index': range(len(self.equity_curve)),
            'equity': self.equity_curve
        })

if __name__ == "__main__":
    # Example usage:
    context = BacktestContext(initial_capital=100000)
    print("Initial cash:", context.cash)
    
    # Simulate opening a trade
    trade_example = {"entry_time": "2022-01-01", "entry_price": 100, "side": "long"}
    context.open_position(trade_example)
    
    # Simulate closing the trade with a profit of 5
    context.close_position(trade_example, profit=5)
    
    print("Cash after trade:", context.cash)
    print("Equity curve:")
    print(context.get_equity_curve())
