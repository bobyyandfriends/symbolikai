# 🧰 utils/

The `utils/` folder contains general-purpose utility functions and helper modules that are used across the SymbolikAI codebase. These functions improve modularity and avoid repetitive code by centralizing common logic.

---

## 📁 Folder Structure

```
utils/
├── __init__.py
├── decorators.py
├── time_utils.py
├── logging_utils.py
└── signal_knowledge_base.py
```

---

## 📄 File Descriptions

### ✅ `__init__.py`
- Marks this directory as a Python module for clean imports.

---

### ✅ `decorators.py`
- **Purpose**: Provides useful decorators for timing, caching, error handling, etc.
- **Key Functions**:
  - `@timed`: Print how long a function takes to run.
  - `@retry`: Retry logic for network or file operations.
  - `@memoize`: Lightweight in-memory caching.

---

### ✅ `time_utils.py`
- **Purpose**: Time and date manipulation helpers.
- **Key Functions**:
  - `parse_timestamp()`: Robust timestamp parser (e.g., for signals).
  - `get_market_open_close()`: Return open/close times for market days.
  - `round_to_nearest_bar()`: Useful for aligning entries to 1-min or 5-min data.

---

### ✅ `logging_utils.py`
- **Purpose**: Logging tools for consistent and styled messages.
- **Key Features**:
  - Colored console output.
  - Debug, info, warn, and error levels.
  - Optional log file persistence.

---

### ✅ `signal_knowledge_base.py`
- **Purpose**: Reads from `signal_docs/` to fetch human- and machine-readable logic for signals.
- **Key Functions**:
  - `get_signal_notes(signal_name)`
  - `load_signal_metadata(signal_name)`
  - `get_entry_conditions()`, `get_failure_reasons()`
- Used in ML commentary and strategy refinement.

---

## 🔁 Design Considerations

- All functions are stateless and reusable.
- Decorators can be combined with your custom strategies or model logic.
- The signal knowledge base enables reflection and documentation-based ML insight.

---

## 🧠 Future Enhancements

- Add `file_utils.py` for loading/saving models and configs.
- Extend `logging_utils.py` to include rotating log files and timestamps.
- Consider creating `cli_utils.py` for CLI interface improvements later.

---

This folder enables consistency, clarity, and maintainability throughout the project.