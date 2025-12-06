#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Logger Module
Handles logging operations and saves success/failed pins to JSON files
"""

import json
import os
from datetime import datetime
from pathlib import Path

class PinterestLogger:
    """Custom logger for Pinterest automation with JSON export"""
    
    def __init__(self):
        self.success_pins = []
        self.failed_pins = []
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
    def log_info(self, message):
        """Log informational message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] [{timestamp}] {message}")
    
    def log_success(self, message):
        """Log success message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[OK] [{timestamp}] {message}")
    
    def log_warning(self, message):
        """Log warning message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[WARN] [{timestamp}] {message}")
    
    def log_error(self, message, exception=None):
        """Log error message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if exception:
            print(f"[ERROR] [{timestamp}] {message}: {str(exception)}")
        else:
            print(f"[ERROR] [{timestamp}] {message}")
    
    def add_success_pin(self, pin_url):
        """Add successful pin to success list"""
        self.success_pins.append({
            "url": pin_url,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_failed_pin(self, pin_url, reason):
        """Add failed pin to failure list"""
        self.failed_pins.append({
            "url": pin_url,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
    
    def save_logs(self):
        """Save success and failed pins to JSON files"""
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save successful pins
        if self.success_pins:
            success_file = self.log_dir / f"success_pins_{timestamp_str}.json"
            with open(success_file, "w", encoding="utf-8") as f:
                json.dump(self.success_pins, f, indent=2, ensure_ascii=False)
            self.log_success(f"Successful pins saved: {success_file}")
        
        # Save failed pins
        if self.failed_pins:
            failed_file = self.log_dir / f"failed_pins_{timestamp_str}.json"
            with open(failed_file, "w", encoding="utf-8") as f:
                json.dump(self.failed_pins, f, indent=2, ensure_ascii=False)
            self.log_warning(f"Failed pins saved: {failed_file}")
    
    def get_summary(self):
        """Get summary of operations"""
        total = len(self.success_pins) + len(self.failed_pins)
        return f"Total: {total} | Successful: {len(self.success_pins)} | Failed: {len(self.failed_pins)}"
