# sor_agent/config.py
import json
import os

def load_config(file_path="config.json"):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    full_path = os.path.join(base_path, file_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Config file not found: {full_path}")
    with open(full_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()
