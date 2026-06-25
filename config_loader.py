import json
import os

CONFIG_FILE = os.getenv(
    "APP_CONFIG_FILE",
    "db-config.json"
)


def load_config():
    
    if not os.path.exists(CONFIG_FILE):
        raise RuntimeError(
            f"Configuration file not found: {CONFIG_FILE}"
        )
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)