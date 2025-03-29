# strategies/rule_engine.py

import pandas as pd
import operator

# Supported operators
OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne
}

def evaluate_condition(df: pd.DataFrame, condition: dict) -> pd.Series:
    """
    Evaluates a single rule like:
    {"col": "RSI", "op": "<", "val": 30}
    """
    col, op, val = condition["col"], condition["op"], condition["val"]

    if col not in df.columns:
        raise KeyError(f"Missing column: {col}")

    return OPS[op](df[col], val)


def evaluate_rule(df: pd.DataFrame, rule: list) -> pd.Series:
    """
    Combines multiple conditions using AND logic.

    Example rule:
    [
        {"col": "RSI", "op": "<", "val": 40},
        {"col": "signal_type", "op": "==", "val": "Perfection9Up"}
    ]
    """
    result = pd.Series(True, index=df.index)

    for cond in rule:
        result &= evaluate_condition(df, cond)

    return result
