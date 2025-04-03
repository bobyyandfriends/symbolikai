#!/usr/bin/env python3
from datetime import datetime

class Trade:
    """
    The Trade class encapsulates a single executed or planned trade.

    Attributes (commonly used):
      - entry_time:    datetime of entry
      - entry_price:   float
      - exit_time:     datetime or None if still open
      - exit_price:    float or None if still open
      - side:          str, 'long' or 'short'
      - quantity:      float, how many shares/lots
      - synergy_score: float, optional synergy or confidence measure
      - reason_codes:  str or list, e.g. "Pivot+DeMark" or ["Pivot","DeMark"]
      - commentary:    str, textual explanation or commentary
      - slippage:      float or None, an estimate of slippage cost
      - commission:    float or None, transaction cost
      - kelly_fraction: float or None, if partial Kelly sizing was used
      - realized_pnl:  float, final realized profit for the trade
      - open_pnl:      float, for ongoing real-time mark-to-market
      - closed:        bool, indicates if trade has been closed
    
    Methods:
      - close_trade(exit_time, exit_price, realized_pnl) -> updates relevant fields, sets closed
      - calculate_pnl(current_price=None) -> optionally compute open_pnl if trade isn't closed
      - to_dict() -> returns a dictionary representation

    You can adapt this blueprint to handle your exact synergy logic,
    advanced risk management, partial close logic, etc.
    """

    def __init__(self,
                 entry_time: datetime,
                 entry_price: float,
                 side: str = "long",
                 quantity: float = 1.0,
                 synergy_score: float = 0.0,
                 reason_codes=None,
                 commentary: str = "",
                 kelly_fraction: float = None,
                 slippage: float = 0.0,
                 commission: float = 0.0):
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.side = side.lower()  # 'long' or 'short'
        self.quantity = quantity

        self.synergy_score = synergy_score
        self.reason_codes = reason_codes if reason_codes else ""
        self.commentary = commentary

        self.kelly_fraction = kelly_fraction
        self.slippage = slippage
        self.commission = commission

        # exit fields
        self.exit_time = None
        self.exit_price = None
        self.realized_pnl = None

        self.closed = False

    def close_trade(self, exit_time: datetime, exit_price: float):
        """
        Close the trade with the specified exit time and price.
        Realized PnL is computed at closure, factoring in side, slippage, commission, etc.
        """
        if self.closed:
            # if the trade is already closed, skip or raise an error
            return

        self.exit_time = exit_time
        self.exit_price = exit_price
        self.closed = True

        # naive PnL calc ignoring partial closes
        raw_pnl = 0.0
        if self.side == "long":
            raw_pnl = (self.exit_price - self.entry_price) * self.quantity
        else:  # short
            raw_pnl = (self.entry_price - self.exit_price) * self.quantity

        # account for slippage + commission
        total_cost = (self.slippage + self.commission)
        self.realized_pnl = raw_pnl - total_cost

    def calculate_pnl(self, current_price: float = None) -> float:
        """
        Calculate open PnL if the trade is not yet closed, or return realized_pnl if closed.
        If current_price is provided for an open trade, we mark to market.
        """
        if self.closed:
            return self.realized_pnl if self.realized_pnl is not None else 0.0

        if current_price is None:
            # if no price, can't do open pnl
            return 0.0

        if self.side == "long":
            open_pnl = (current_price - self.entry_price) * self.quantity
        else:
            open_pnl = (self.entry_price - current_price) * self.quantity

        # we usually don't subtract slippage/commission from open PnL,
        # but if your approach does, handle that here.
        return open_pnl

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of this trade's attributes.
        This is handy for logging or converting to a DataFrame.
        """
        return {
            "entry_time": self.entry_time,
            "entry_price": self.entry_price,
            "exit_time": self.exit_time,
            "exit_price": self.exit_price,
            "side": self.side,
            "quantity": self.quantity,
            "synergy_score": self.synergy_score,
            "reason_codes": self.reason_codes,
            "commentary": self.commentary,
            "slippage": self.slippage,
            "commission": self.commission,
            "kelly_fraction": self.kelly_fraction,
            "realized_pnl": self.realized_pnl,
            "closed": self.closed
        }


if __name__ == "__main__":
    # Example usage:
    from datetime import datetime, timedelta

    # Create a new trade
    my_trade = Trade(
        entry_time=datetime(2023, 1, 1, 9, 30),
        entry_price=100.0,
        side="long",
        quantity=50,
        synergy_score=2.5,
        reason_codes="Pivot+DeMark",
        commentary="Triggered by synergy alignment",
        kelly_fraction=0.15,
        slippage=2.0,
        commission=1.0
    )

    # Check open PnL with a hypothetical current price of 103
    open_pnl = my_trade.calculate_pnl(current_price=103.0)
    print(f"Open PnL: {open_pnl:.2f}")

    # Close the trade
    my_trade.close_trade(
        exit_time=datetime(2023, 1, 1, 16, 0), 
        exit_price=105.0
    )
    # Realized PnL factoring slippage & commission
    print(f"Realized PnL: {my_trade.realized_pnl:.2f}")

    # Dump to dictionary
    trade_dict = my_trade.to_dict()
    print(trade_dict)
