🧠 Overview of DeMark Signals for the SymbolikAI Project
This project integrates several proprietary technical indicators developed by Tom DeMark. These indicators aim to identify trend exhaustion, reversals, or continuation points using price action patterns. The signals we're using are extracted from a system called Symbolik, and they serve as one of the key layers in our strategy engine.

Here’s a breakdown of the core signals we are tracking in the Excel sheet:

🔢 1. Sequential 13 (S13)
Goal: Identify trend exhaustion points that may precede a reversal.

This signal is generated after a sequence of 13 price bars that meet specific rules involving the relationship between the current bar and a bar four periods earlier.

Once 13 qualifying bars have printed, the market is considered to be exhausted in the current direction.

A buy setup (S13Down) usually occurs after a prolonged downtrend; sell setup (S13Up) appears after an extended uptrend.

Not always predictive on their own but stronger when layered with other signals like TDST or Combo.

🔁 2. Combo 13 (C13)
Goal: Similar to Sequential, but uses slightly different criteria to track exhaustion and potential reversals.

Focuses on closes instead of highs/lows (used in Sequential).

Often prints earlier than Sequential, offering a potentially earlier signal.

Useful when both Combo and Sequential 13 trigger around the same time — these events are often higher-conviction.

🧪 3. Combo 13 V1B (C13V1B)
Goal: A variation of Combo13 that includes refinements to make it more selective.

This version typically filters out weaker setups and prints fewer signals than base Combo13.

The "V1B" refers to Version 1 Beta – Symbolik exposes it as a toggle.

In backtests, this version often has higher quality at the cost of signal frequency.

🔹 4. Perfection 9 (P9)
Goal: Detects early signs of potential trend exhaustion before a full Sequential 13.

Generated when a Setup 9 (a 9-bar condition) completes and meets “perfection” rules.

Perfection means the final bar exceeds the highs/lows of several earlier bars, indicating a spike or climax move.

Usually signals a short-term reversal or pullback.

Great for timing entries — especially when stacked with higher-timeframe C13 or S13 signals.

⛓ Signal Format in the Excel Sheet
The signals in the sheet are labeled with:

Symbol: e.g., AAPL, MSFT

Signal: e.g., Perfection9Up, S13Down, C13V1BUp

Timeframe: Daily or 240 (i.e., 240-minute)

Date: Date/time the signal occurred

These signals will later be mapped to price data and used in feature generation, backtesting, and model training.