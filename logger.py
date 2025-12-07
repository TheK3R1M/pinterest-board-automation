#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging System for Pinterest Automation
Tracks success/failed pins and generates reports
"""

import json
from pathlib import Path
from datetime import datetime

class PinterestLogger:
    """Logs and reports pin save results"""

    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Log files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.success_pins_file = self.logs_dir / f"success_pins_{timestamp}.json"
        self.failed_pins_file = self.logs_dir / f"failed_pins_{timestamp}.json"
        self.error_log_file = self.logs_dir / f"error_log_{timestamp}.txt"
        
        self.success_pins = []
        self.failed_pins = []

    def log_error(self, message: str, exception=None):
        """Log error"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERROR] [{timestamp}] {message}")
        
        if exception:
            print(f"  Details: {str(exception)}")
            with open(self.error_log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
                f.write(f"  Exception: {str(exception)}\n\n")

    def log_info(self, message: str):
        """Log info"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] [{timestamp}] {message}")

    def log_success(self, message: str):
        """Log success"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[OK] [{timestamp}] {message}")

    def log_warning(self, message: str):
        """Log warning"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[WARN] [{timestamp}] {message}")

    def add_failed_pin(self, pin_url: str, reason: str):
        """Record failed pin"""
        self.failed_pins.append({
            "pin_url": pin_url,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })

    def add_success_pin(self, pin_url: str):
        """Record successful pin"""
        self.success_pins.append({
            "url": pin_url,
            "timestamp": datetime.now().isoformat()
        })

    def save_logs(self):
        """Save all logs to files"""
        if self.failed_pins:
            with open(self.failed_pins_file, "w", encoding="utf-8") as f:
                json.dump(self.failed_pins, f, ensure_ascii=False, indent=2)
            self.log_warning(f"Failed pins saved: {self.failed_pins_file}")
        
        if self.success_pins:
            with open(self.success_pins_file, "w", encoding="utf-8") as f:
                json.dump(self.success_pins, f, ensure_ascii=False, indent=2)
            
            # Also save as "latest" for inventory tracking
            latest_file = self.logs_dir / "success_pins_latest.json"
            with open(latest_file, "w", encoding="utf-8") as f:
                json.dump({
                    "successful_pins": [pin.get("url") for pin in self.success_pins],
                    "count": len(self.success_pins),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
            self.log_success(f"Success pins saved: {self.success_pins_file}")
            self.log_success(f"Latest reference saved: {latest_file}")

    def get_summary(self):
        """Get summary statistics"""
        total = len(self.success_pins) + len(self.failed_pins)
        return f"Total: {total} | Success: {len(self.success_pins)} | Failed: {len(self.failed_pins)}"
