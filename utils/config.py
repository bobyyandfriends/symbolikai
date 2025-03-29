#!/usr/bin/env python3
import yaml
import os

def load_config(config_file: str = "config.yaml") -> dict:
    """
    Load configuration settings from a YAML file.
    
    Parameters:
      config_file (str): Path to the configuration file.
      
    Returns:
      dict: Configuration dictionary.
      
    Raises:
      FileNotFoundError: If the configuration file is not found.
      yaml.YAMLError: If there is an error parsing the YAML file.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    return config

if __name__ == "__main__":
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(config)
    except Exception as e:
        print(f"Error loading configuration: {e}")
