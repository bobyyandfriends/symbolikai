# utils/config_loader.py

import json
import yaml

def load_json_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def save_json_config(config: dict, path: str):
    with open(path, "w") as f:
        json.dump(config, f, indent=4)

def load_yaml_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_yaml_config(config: dict, path: str):
    with open(path, "w") as f:
        yaml.safe_dump(config, f)
