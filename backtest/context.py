#!/usr/bin/env python3

import pandas as pd
from datetime import datetime




class BacktestContext:
    """
    A class to hold and update the simulation state during a backtest.
    This context tracks:
      - initial capital and current cash,
      - a time-indexed equity curve,
      - active (open) positions (dict objects),
      - a log of closed trades (with synergy, commentary, etc.),
      - a running record of key events or reasoning logs.

    USAGE:
    ------
    1. Initialize with an initial_capital amount.
    2. call open_position(trade_dict) whenever a new trade is opened.
       - trade_dict should have fields like:
            {
              'entry_time': datetime or str,
              'entry_price': float,
              'side': 'long' or 'short',
              'quantity': float,
              'synergy_score': float,
              'reason_codes': 'Pivot+DeMark',
              'commentary': 'some text'
              ...
            }
    3. call close_position(...) to finalize a trade, pass the original dict,
       plus realized profit if needed. 
       - The method removes it from active_positions,
         appends it to trade_log with final fields, and updates cash/equity.
    4. call update_time(...) to move simulation time forward if needed,
       e.g. daily or per bar. 
    5. get_equity_curve() returns a DataFrame with time + equity or index + equity.

    Extend or modify as your strategy/engine demands.
    """

    def __init__(self, initial_capital: float = 100_000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital

        # equity_curve can store (datetime, equity) or (index, equity).
        # We'll store as list of dict for flexibility
        self.equity_curve = []
        self.active_positions = []  # List of dict objects for open trades
        self.trade_log = []         # List of dict objects for closed trades
        self.current_time = None    # Current simulation time
        self.reasoning_log = []     # Optional: store summary of significant events

        # record initial equity point
        self._record_equity_point(equity=self.cash, note="Initial")


    def _record_equity_point(self, equity: float, note: str = ""):
        """
        Internal helper to record an equity/time data point in equity_curve.
        If self.current_time is None, we store an integer index approach.
        Otherwise we store actual time for plotting.
        """
        if self.current_time is None:
            # fallback to index
            row = {
                'time': len(self.equity_curve),
                'equity': equity,
                'note': note
            }
        else:
            row = {
                'time': self.current_time,
                'equity': equity,
                'note': note
            }
        self.equity_curve.append(row)


    def open_position(self, trade: dict):
        """
        Register a new open position in self.active_positions.

        trade dict example:
          {
            'entry_time': datetime,
            'entry_price': float,
            'side': 'long' or 'short',
            'quantity': float,
            'synergy_score': float,
            'reason_codes': str or list,
            'commentary': str,
            ...
          }

        If your system requires deducting capital for margin usage or
        some approximate cost, do it here.
        e.g.:
          cost = trade['entry_price'] * trade['quantity']
          self.cash -= cost
        But this depends on your margin/cash flow approach.
        """
        if 'entry_time' in trade:
            # update current_time if you want the context to reflect
            self.current_time = trade['entry_time']
        else:
            # optional fallback
            self.current_time = None

        # If you want to deduct from cash immediately:
        # cost = trade.get('entry_price', 0.0) * trade.get('quantity', 0.0)
        # self.cash -= cost
        # ensure we don't go negative if your rules forbid
        self.active_positions.append(trade)


    def close_position(self, trade: dict, profit: float, exit_time=None):
        """
        Close an open position:
           - remove from active_positions
           - add a final realized trade record to trade_log
           - update self.cash, self.equity_curve

        :param trade: The original trade dict (must exist in active_positions).
        :param profit: realized PnL from this trade.
        :param exit_time: optionally pass datetime or str for final exit time
        """
        if trade in self.active_positions:
            self.active_positions.remove(trade)
        else:
            # If not found, either it's already removed or an error
            # Could raise an exception or log a warning
            pass

        # if your system recovers exit_price from the logic, you can store it:
        # e.g. trade['exit_price'] = ...
        trade['realized_profit'] = profit
        if exit_time is not None:
            trade['exit_time'] = exit_time
            self.current_time = exit_time

        # Possibly adjust self.cash if you do real capital tracking:
        self.cash += profit

        # finalize the trade record in trade_log
        self.trade_log.append(trade)

        # log equity after closing
        self._record_equity_point(equity=self.cash, note="ClosePosition")


    def update_time(self, new_time):
        """
        Update the current simulation time. 
        This can be used to record an equity point at the new_time 
        if desired, or only when trades occur.
        """
        self.current_time = new_time
        # Optionally record an equity data point each time
        # self._record_equity_point(equity=self.cash, note="TimeUpdate")


    def get_equity_curve(self) -> pd.DataFrame:
        """
        Return the equity curve as a DataFrame. 
        Columns: 'time', 'equity', 'note'
        """
        return pd.DataFrame(self.equity_curve)


    def log_reasoning(self, msg: str, time=None):
        """
        Optionally store a text message with optional time.
        This can track important events (like synergy alignment, meta-ml signals, etc.).
        """
        if time is None:
            time = self.current_time
        log_item = {
            'time': time,
            'message': msg
        }
        self.reasoning_log.append(log_item)


    def get_reasoning_log(self) -> pd.DataFrame:
        """
        Return the reasoning log as a DataFrame.
        """
        return pd.DataFrame(self.reasoning_log)


if __name__ == "__main__":
    # Example usage:
    context = BacktestContext(initial_capital=100_000)
    print("Initial cash:", context.cash)

    # Simulate opening a trade
    example_trade = {
        'entry_time': datetime(2022, 1, 1),
        'entry_price': 100.0,
        'side': 'long',
        'quantity': 50.0,
        'synergy_score': 2.0,
        'reason_codes': 'Pivot+DeMark',
        'commentary': "Trade triggered by synergy alignment."
    }
    context.open_position(example_trade)

    # Simulate partial close or time passing
    context.update_time(datetime(2022, 1, 2))

    # Simulate closing the trade with a profit of 250
    context.close_position(
        trade=example_trade,
        profit=250.0,
        exit_time=datetime(2022, 1, 3)
    )

    print("Cash after trade:", context.cash)
    eq_df = context.get_equity_curve()
    print("\nEquity curve:")
    print(eq_df)

    # Show how reasoning logs might be used
    context.log_reasoning("Another day, synergy check done. synergy=2.5", time=datetime(2022, 1, 3))
    reason_df = context.get_reasoning_log()
    print("\nReasoning Log:")
    print(reason_df)
