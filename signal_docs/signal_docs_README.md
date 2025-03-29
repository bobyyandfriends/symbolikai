# 📁 signal_docs/

The `signal_docs/` folder serves as the **knowledge base** for all proprietary and technical signals used within SymbolikAI. This directory contains both **human-readable documentation** and **machine-readable metadata** for every trading signal in the system.

This enables deeper signal introspection, smarter model commentary, debugging, and reasoning-aware trading strategy development.

---

## 📦 Folder Contents

Each signal is represented by:
- A **Markdown file (`.md`)**: Explains the logic, behavior, modifiers, and caveats of the signal.
- A **YAML file (`.yaml`)**: Structured metadata for machine access, used in inference and model commentary.

Additionally:
- `signal_change_log.md`: A changelog for tracking edits and iterations of signal definitions over time.

---

## 🧠 Use Cases

- ✅ **Signal validation**: Compare expected signal logic vs. actual market behavior.
- ✅ **Model interpretability**: Models can reference signal metadata to explain predictions.
- ✅ **Self-reflection**: Signals can log when/why they failed based on known weaknesses.
- ✅ **Feature engineering**: Use signal type or behavior to generate tailored features.

---

## 🗂️ File Example: `C13Up`

### `C13Up.md`
Explains:
- Purpose: "Combo 13 continuation signal"
- Known behaviors: Strength in trending markets, weaknesses in choppy conditions
- Observations from historical trades
- Typical entry/exit conditions

### `C13Up.yaml`
```yaml
signal_name: C13Up
type: trend-following
rules:
  - "Complete a 13-count after a valid setup"
entry_conditions:
  - "Momentum > 0"
  - "RSI between 40–60"
exit_behavior:
  - "Price closes below 21 EMA"
failures:
  - "Triggered in low-volume chop"
strength_modifiers:
  - "Stacked with P9Up"
```

---

## 📘 Sample Files

- `Perfection9Up.md` / `.yaml`
- `TDSTBreakdown.md` / `.yaml`
- `C13Up.md` / `.yaml`
- `SequentialV1B.md` / `.yaml`
- `signal_change_log.md` — tracks revision history and rationale

---

## 🛠️ How It Works in System

- Loaded by: `utils/signal_knowledge_base.py`
- Used by: `ml/self_reflection.py`, `model_commentary.py`
- Provides signal metadata for:
  - Model commentary and justification
  - Entry condition checking
  - Failure reason matching

---

## 🔁 Future Ideas

- Add signal reliability scoring
- Auto-generate YAML metadata from trade outcomes
- Link to charts showing signal behavior

---

## ✅ Summary

The `signal_docs/` folder is a critical reasoning layer for SymbolikAI. It enables contextual understanding of signals by both the developer and the system, supporting smarter trading logic, interpretability, and long-term strategy evolution.