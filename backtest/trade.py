#!/usr/bin/env python3
from datetime import datetime

class Trade:
    """
    The Trade class encapsulates attributes and methods for a single trade.
    
    Attributes:
      - entry_time: datetime when the trade is entered.
      - entry_price: float entry price.
      - exit_time: datetime when the trade is exited.
      - exit_price: float exit price.
      - side: 'long' or 'short'
      - capital: capital allocated for the trade (optional).
      - stop_loss: optional stop-loss price.
      - profit_target: optional profit target price.
      - slippage_pct: percentage to adjust exit price for slippage.
      - pnl: profit and loss calculated for the trade.
    """
    def __init__(self, entry_time: datetime, entry_price: float, side: str = "long",
                 capital: float = 0.0, stop_loss: float = None, profit_target: float = None,
                 slippage_pct: float = 0.0):
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.exit_time = None
        self.exit_price = None
        self.side = side.lower()  # Must be 'long' or 'short'
        self.capital = capital
        self.stop_loss = stop_loss
        self.profit_target = profit_target
        self.slippage_pct = slippage_pct
        self.pnl = None

    def close_trade(self, exit_time: datetime, exit_price: float):
        """
        Close the trade using the provided exit time and exit price.
        If a slippage percentage is specified, adjust the exit price accordingly.
        Then calculate the PnL for the trade.
        """
        self.exit_time = exit_time
        # Apply slippage: for long trades, a lower exit price reduces profit;
        # for short trades, a higher exit price reduces profit.
        if self.slippage_pct > 0:
            adjustment = self.slippage_pct * exit_price
            if self.side == "long":
                self.exit_price = exit_price - adjustment
            else:
                self.exit_price = exit_price + adjustment
        else:
            self.exit_price = exit_price

        self.calculate_pnl()

    def calculate_pnl(self) -> float:
        """
        Calculate the profit and loss (PnL) for the trade.
        For a long trade: pnl = exit_price - entry_price.
        For a short trade: pnl = entry_price - exit_price.
        Returns the calculated PnL.
        """
        if self.exit_price is None:
            raise ValueError("Trade has not been closed; cannot calculate PnL.")
        if self.side == "long":
            self.pnl = self.exit_price - self.entry_price
        elif self.side == "short":
            self.pnl = self.entry_price - self.exit_price
        else:
            raise ValueError("Invalid trade side. Must be 'long' or 'short'.")
        return self.pnl

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the trade details.
        """
        return {
            "entry_time": self.entry_time,
            "entry_price": self.entry_price,
            "exit_time": self.exit_time,
            "exit_price": self.exit_price,
            "side": self.side,
            "capital": self.capital,
            "stop_loss": self.stop_loss,
            "profit_target": self.profit_target,
            "slippage_pct": self.slippage_pct,
            "pnl": self.pnl
        }

if __name__ == "__main__":
    # Example usage:
    from datetime import timedelta
    entry_time = datetime.now()
    entry_price = 100.0
    # Create a long trade with $10,000 capital and 0.1% slippage.
    trade = Trade(entry_time, entry_price, side="long", capital=10000, slippage_pct=0.001)
    # Simulate the trade closing after 1 day at an exit price of 102.0.
    exit_time = entry_time + timedelta(days=1)
    exit_price = 102.0
    trade.close_trade(exit_time, exit_price)
    print("Trade details:")
    print(trade.to_dict())
