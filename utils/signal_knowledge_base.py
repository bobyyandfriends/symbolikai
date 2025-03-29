#!/usr/bin/env python3
import os
import yaml

def load_signal_metadata(signal_name: str, docs_dir: str = "signal_docs") -> dict:
    """
    Load the metadata for a given signal from its YAML file.
    The YAML file should be named '<signal_name>.yaml' and be located in the docs_dir.
    
    Parameters:
      signal_name: The canonical name of the signal (e.g., "C13Up").
      docs_dir: Directory where signal documentation files are stored.
      
    Returns:
      A dictionary with the signal metadata.
      
    Raises:
      FileNotFoundError if the file does not exist.
    """
    filename = os.path.join(docs_dir, f"{signal_name}.yaml")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Signal metadata file not found: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)
    return metadata

def get_signal_notes(signal_name: str, docs_dir: str = "signal_docs") -> str:
    """
    Load the human-readable notes for a given signal from its Markdown file.
    The file should be named '<signal_name>.md' and be located in the docs_dir.
    
    Parameters:
      signal_name: The canonical name of the signal (e.g., "C13Up").
      docs_dir: Directory where signal documentation files are stored.
      
    Returns:
      A string containing the notes for the signal.
      
    Raises:
      FileNotFoundError if the file does not exist.
    """
    filename = os.path.join(docs_dir, f"{signal_name}.md")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Signal notes file not found: {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        notes = f.read()
    return notes

def get_entry_conditions(signal_name: str, docs_dir: str = "signal_docs") -> list:
    """
    Extract the entry conditions for a given signal from its metadata.
    
    Parameters:
      signal_name: The canonical name of the signal.
      docs_dir: Directory where the YAML metadata is stored.
      
    Returns:
      A list of entry conditions, or an empty list if none are defined.
    """
    metadata = load_signal_metadata(signal_name, docs_dir)
    return metadata.get("entry_conditions", [])

def get_failure_reasons(signal_name: str, docs_dir: str = "signal_docs") -> list:
    """
    Extract the failure reasons for a given signal from its metadata.
    
    Parameters:
      signal_name: The canonical name of the signal.
      docs_dir: Directory where the YAML metadata is stored.
      
    Returns:
      A list of failure reasons, or an empty list if none are defined.
    """
    metadata = load_signal_metadata(signal_name, docs_dir)
    return metadata.get("failures", [])

if __name__ == "__main__":
    # Example usage:
    signal_name = "C13Up"  # Change this to a valid signal name from your signal_docs folder.
    try:
        notes = get_signal_notes(signal_name)
        metadata = load_signal_metadata(signal_name)
        entry_conditions = get_entry_conditions(signal_name)
        failure_reasons = get_failure_reasons(signal_name)
        
        print(f"Notes for {signal_name}:\n{notes}\n")
        print(f"Metadata for {signal_name}:\n{metadata}\n")
        print(f"Entry Conditions for {signal_name}:\n{entry_conditions}\n")
        print(f"Failure Reasons for {signal_name}:\n{failure_reasons}\n")
    except Exception as e:
        print(e)
