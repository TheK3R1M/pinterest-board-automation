import json
import os
from datetime import datetime

def save_lost_pin(pin_url, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"lost_pins_{date_str}.json")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            pins = json.load(f)
    else:
        pins = []
    if pin_url not in pins:
        pins.append(pin_url)
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(pins, f, ensure_ascii=False, indent=2)
