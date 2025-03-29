# backtest/context.py

from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class SimulationContext:
    """
    Tracks current capital, open positions, and other stateful metrics
    for a backtest simulation.
    """
    initial_capital: float
    current_cash: float
    current_equity: float
    open_positions: Dict[str, dict] = field(default_factory=dict)
    active_trades: list = field(default_factory=list)
    symbol: Optional[str] = None
    timeframe: Optional[str] = None
    simulation_metadata: dict = field(default_factory=dict)

    def reset(self):
        """
        Reset the simulation to the initial state.
        """
        self.current_cash = self.initial_capital
        self.current_equity = self.initial_capital
        self.open_positions.clear()
        self.active_trades.clear()
        self.simulation_metadata.clear()

    def update_equity(self, new_equity: float):
        """
        Update the current equity (e.g., after trade exit).
        """
        self.current_equity = new_equity

    def log_position(self, symbol: str, position_data: dict):
        """
        Log or update an open position.
        """
        self.open_positions[symbol] = position_data

    def close_position(self, symbol: str):
        """
        Remove a position when closed.
        """
        if symbol in self.open_positions:
            del self.open_positions[symbol]
