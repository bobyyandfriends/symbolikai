# strategies/strategy_loader.py

from strategies.demark_perfection_strategy import Perfection9UpStrategy

STRATEGY_REGISTRY = {
    "Perfection9Up": Perfection9UpStrategy,
    # Future strategies can be added here:
    # "ComboStrategy": ComboStrategy,
    # "C13Stacker": C13Stacker,
}

def load_strategy(name: str):
    """
    Loads a strategy by name.
    """
    try:
        return STRATEGY_REGISTRY[name]()
    except KeyError:
        raise ValueError(f"Strategy '{name}' not found. Available: {list(STRATEGY_REGISTRY.keys())}")
