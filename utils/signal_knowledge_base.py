# utils/signal_knowledge_base.py

import os
import yaml

SIGNAL_DOCS_PATH = "signal_docs/"

def get_signal_notes(signal_name: str) -> str:
    """
    Load human-readable markdown notes for a given signal.
    """
    path = os.path.join(SIGNAL_DOCS_PATH, f"{signal_name}.md")
    if not os.path.exists(path):
        return f"No documentation found for signal: {signal_name}"
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_signal_metadata(signal_name: str) -> dict:
    """
    Load machine-readable metadata (.yaml) for a given signal.
    """
    path = os.path.join(SIGNAL_DOCS_PATH, f"{signal_name}.yaml")
    if not os.path.exists(path):
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_entry_conditions(signal_name: str):
    """
    Return list of known entry conditions from signal metadata.
    """
    metadata = load_signal_metadata(signal_name)
    return metadata.get("entry_conditions", [])


def get_failure_reasons(signal_name: str):
    """
    Return known failure scenarios from signal metadata.
    """
    metadata = load_signal_metadata(signal_name)
    return metadata.get("failures", [])
