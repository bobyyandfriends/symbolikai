#!/usr/bin/env python3
import os
import sys

# Dynamically add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_strategy(name: str):
    name = name.lower()
    if name == "simplestrategy":
        from strategies.simple_strategy import SimpleStrategy
        return SimpleStrategy()
    elif name == "demarkperfection":
        from strategies.demark_perfection_strategy import DemarkPerfectionStrategy
        return DemarkPerfectionStrategy()
    elif name == "combo":
        from strategies.combo_strategy_example import ComboStrategyExample
        return ComboStrategyExample()
    else:
        raise ValueError(f"Strategy '{name}' is not recognized. Available options: simplestrategy, demarkperfection, combo.")

if __name__ == "__main__":
    strat = load_strategy("simplestrategy")
    print(f"Loaded strategy: {strat.name}")
