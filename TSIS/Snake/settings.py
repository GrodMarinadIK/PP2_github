"""
settings.py – load / save user preferences from settings.json.
"""

import json, os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

DEFAULTS = {
    "snake_color": [0, 200, 80],   # RGB
    "grid":        True,            # show inner grid
    "sound":       True,
}


def load() -> dict:
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        # fill missing keys with defaults
        for k, v in DEFAULTS.items():
            data.setdefault(k, v)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(DEFAULTS)


def save(settings: dict):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"[Settings] save failed: {e}")