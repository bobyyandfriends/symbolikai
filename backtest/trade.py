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
                 entry_time,
                 entry_price,
                 side,
                 capital=10000,
                 quantity=1.0,
                 stop_loss=None,
                 profit_target=None,
                 slippage_pct=0.0,
                 commission=0.0,
                 synergy_score=0.0,
                 reason_codes=None,
                 commentary="",
                 kelly_fraction=None,
                 **kwargs):
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.side = side.lower()
        self.capital = capital
        self.quantity = quantity
        self.stop_loss = stop_loss
        self.profit_target = profit_target
        self.slippage_pct = slippage_pct
        self.slippage = entry_price * slippage_pct if slippage_pct > 0 else 0.0
        self.commission = commission
        self.synergy_score = synergy_score
        self.reason_codes = reason_codes if reason_codes is not None else ""
        self.commentary = commentary
        self.kelly_fraction = kelly_fraction

        self.exit_time = None
        self.exit_price = None
        self.realized_pnl = None
        self.closed = False

        # Allow custom kwargs for extensibility
        for k, v in kwargs.items():
            setattr(self, k, v)

    def close_trade(self, exit_time: datetime, exit_price: float):
        """
        Close the trade with the specified exit time and price.
        Realized PnL is computed at closure.
        """
        if self.closed:
            return

        self.exit_time = exit_time
        self.exit_price = exit_price
        self.closed = True

        if self.side == "long":
            raw_pnl = (exit_price - self.entry_price) * self.quantity
        else:
            raw_pnl = (self.entry_price - exit_price) * self.quantity

        self.realized_pnl = raw_pnl - (self.slippage + self.commission)

    def calculate_pnl(self, current_price: float = None) -> float:
        if self.closed:
            return self.realized_pnl if self.realized_pnl is not None else 0.0

        if current_price is None:
            return 0.0

        if self.side == "long":
            return (current_price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - current_price) * self.quantity

    def to_dict(self) -> dict:
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
            "slippage_pct": self.slippage_pct,
            "commission": self.commission,
            "kelly_fraction": self.kelly_fraction,
            "realized_pnl": self.realized_pnl,
            "closed": self.closed,
        }


# Example usage
if __name__ == "__main__":
    from datetime import timedelta

    my_trade = Trade(
        entry_time=datetime(2023, 1, 1, 9, 30),
        entry_price=100.0,
        side="long",
        quantity=50,
        synergy_score=2.5,
        reason_codes="Pivot+DeMark",
        commentary="Triggered by synergy alignment",
        kelly_fraction=0.15,
        slippage_pct=0.02,
        commission=1.0
    )

    print("Open PnL:", my_trade.calculate_pnl(103.0))

    my_trade.close_trade(
        exit_time=datetime(2023, 1, 1, 16, 0),
        exit_price=105.0
    )

    print("Realized PnL:", my_trade.realized_pnl)
    print("Trade Dictionary:", my_trade.to_dict())