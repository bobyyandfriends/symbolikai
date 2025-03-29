#!/usr/bin/env python3
import pandas as pd
import operator

OPERATORS = {
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne
}

def evaluate_rule(df: pd.DataFrame, rule: dict) -> pd.Series:
    """
    Evaluate a rule on the DataFrame and return a boolean Series.
    
    Rule format example:
    {
      "conditions": [
         {"column": "rsi", "operator": "<", "value": 30},
         {"column": "close", "operator": ">", "value": "sma"}  # value can be a constant or another column name
      ],
      "combine": "and"   # or "or"
    }
    """
    conditions = rule.get("conditions", [])
    combine_op = rule.get("combine", "and").lower()
    
    if not conditions:
        raise ValueError("Rule must contain at least one condition.")
    
    result = None
    for cond in conditions:
        col = cond.get("column")
        op_str = cond.get("operator")
        val = cond.get("value")
        if op_str not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op_str}")
        op_func = OPERATORS[op_str]
        # If value is numeric, use it directly; if string, assume it's a column reference.
        if isinstance(val, (int, float)):
            series = op_func(df[col], val)
        elif isinstance(val, str):
            series = op_func(df[col], df[val])
        else:
            raise ValueError("Condition value must be int, float, or str.")
        
        if result is None:
            result = series
        else:
            if combine_op == "and":
                result = result & series
            elif combine_op == "or":
                result = result | series
            else:
                raise ValueError("Combine operator must be 'and' or 'or'.")
    return result

if __name__ == "__main__":
    # Example usage:
    import numpy as np
    df = pd.DataFrame({
        'rsi': np.random.randint(20, 80, size=10),
        'close': np.linspace(100, 110, 10),
        'sma': np.linspace(101, 111, 10)
    })
    rule = {
        "conditions": [
            {"column": "rsi", "operator": "<", "value": 40},
            {"column": "close", "operator": ">", "value": "sma"}
        ],
        "combine": "and"
    }
    condition_met = evaluate_rule(df, rule)
    print("DataFrame:")
    print(df)
    print("Rule condition met:")
    print(condition_met)
