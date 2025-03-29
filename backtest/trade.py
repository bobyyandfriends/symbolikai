# backtest/trade.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    side: str  # "long" or "short"
    signal: str = None
    capital: float = 1.0  # Default to $1 for normalized return
    slippage: float = 0.0  # In % (e.g., 0.001 = 0.1%)

    def calculate_pnl(self) -> float:
        if self.side == "long":
            gross_return = (self.exit_price - self.entry_price) / self.entry_price
        else:
            gross_return = (self.entry_price - self.exit_price) / self.entry_price

        net_return = gross_return - self.slippage
        return net_return * self.capital

    def get_return_pct(self) -> float:
        return self.calculate_pnl() / self.capital

    def get_duration(self) -> int:
        return (self.exit_time - self.entry_time).days

    def to_dict(self) -> dict:
        return {
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "side": self.side,
            "signal": self.signal,
            "capital": self.capital,
            "pnl": self.calculate_pnl(),
            "return_pct": self.get_return_pct(),
            "duration_days": self.get_duration()
        }

    @staticmethod
    def from_row(row: dict) -> "Trade":
        return Trade(
            entry_time=row["entry_time"],
            exit_time=row["exit_time"],
            entry_price=row["entry_price"],
            exit_price=row["exit_price"],
            side=row["side"],
            signal=row.get("signal", None),
            capital=row.get("capital", 1.0),
            slippage=row.get("slippage", 0.0)
        )
