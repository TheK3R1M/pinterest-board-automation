#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Inventory Manager - NEW
Handles duplicate detection, inventory tracking, and smart resume

Key Features:
- Initial board scan creates pins_inventory.json (all pins, scan once)
- Compares inventory with success_pins.json = finds resume point
- Detects duplicates (pins saved multiple times)
- Prevents duplicate saves on restart
- Smart resume: starts from last successful pin
"""

import json
import time
from pathlib import Path
from collections import Counter
from datetime import datetime

class PinterestInventoryManager:
    """Manages pin inventory, duplicates, and resume points"""

    def __init__(self, logger):
        self.logger = logger
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        self.inventory_file = self.logs_dir / "pins_inventory.json"
        self.success_file = self.logs_dir / "success_pins_latest.json"
        self.duplicates_file = self.logs_dir / "duplicates.json"
        self.checkpoint_file = self.logs_dir / "progress_checkpoint.json"

    def create_inventory(self, pin_links):
        """
        Create initial inventory of all pins from board
        Should be done ONCE per board at the start
        
        Returns: inventory data with metadata
        """
        inventory = {
            'created_at': datetime.now().isoformat(),
            'total_pins': len(pin_links),
            'pins': list(pin_links),
            'pin_ids': [self._extract_pin_id(url) for url in pin_links],
            'checksum': self._calculate_checksum(pin_links)
        }
        
        # Save inventory
        with open(self.inventory_file, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)
        
        self.logger.log_success(f"✅ Inventory created: {len(pin_links)} pins")
        return inventory

    def detect_duplicates(self):
        """
        Compare pins_inventory.json with success_pins.json
        Returns duplicates and resume point
        """
        if not self.inventory_file.exists():
            self.logger.log_warning("Inventory not found - create with 'create_inventory()'")
            return None, None, None
        
        # Load inventory
        with open(self.inventory_file, 'r', encoding='utf-8') as f:
            inventory = json.load(f)
        
        # Find all success files
        success_files = sorted(self.logs_dir.glob("success_pins_*.json"))
        
        if not success_files:
            self.logger.log_info("No previous success records found - starting fresh")
            return inventory['pins'], None, None
        
        # Combine all successful pins
        all_saved_pins = set()
        for success_file in success_files:
            try:
                with open(success_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    saved_pins = data.get('successful_pins', [])
                    all_saved_pins.update(saved_pins)
            except:
                pass
        
        # Find duplicates (pins saved multiple times)
        pin_counts = Counter(all_saved_pins)
        duplicates = {pin: count for pin, count in pin_counts.items() if count > 1}
        
        # Find resume point
        remaining_pins = [p for p in inventory['pins'] if p not in all_saved_pins]
        resume_index = None
        
        if remaining_pins:
            try:
                resume_index = inventory['pins'].index(remaining_pins[0])
            except (ValueError, IndexError):
                resume_index = len(all_saved_pins)  # Fallback to count
        else:
            resume_index = len(inventory['pins'])  # All done
        
        # Log report
        self.logger.log_info("-" * 60)
        self.logger.log_info("📊 INVENTORY REPORT:")
        self.logger.log_info(f"  Total in board: {len(inventory['pins'])}")
        self.logger.log_info(f"  Already saved: {len(all_saved_pins)}")
        self.logger.log_info(f"  Remaining: {len(remaining_pins)}")
        
        if duplicates:
            self.logger.log_warning(f"  ⚠️  DUPLICATES FOUND: {len(duplicates)}")
            self._save_duplicates_report(duplicates, inventory)
        else:
            self.logger.log_info("  ✅ No duplicates found")
        
        self.logger.log_info("-" * 60)
        
        return remaining_pins, duplicates, resume_index

    def _extract_pin_id(self, pin_url):
        """Extract pin ID from URL"""
        try:
            return pin_url.split("/pin/")[1].split("/")[0]
        except:
            return None

    def _calculate_checksum(self, pin_links):
        """Calculate checksum to detect inventory changes"""
        import hashlib
        pins_str = "|".join(sorted(pin_links))
        return hashlib.md5(pins_str.encode()).hexdigest()

    def _save_duplicates_report(self, duplicates, inventory):
        """Save detailed duplicates report"""
        report = {
            'detected_at': datetime.now().isoformat(),
            'total_duplicates': len(duplicates),
            'duplicated_pins': [
                {
                    'pin_url': pin,
                    'pin_id': self._extract_pin_id(pin),
                    'saved_count': count,
                    'extra_saves': count - 1
                }
                for pin, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)
            ],
            'action_needed': 'Review and delete duplicate saves from Pinterest boards'
        }
        
        with open(self.duplicates_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.log_warning(f"Duplicates report saved to: {self.duplicates_file}")

    def get_resume_instructions(self, remaining_pins, duplicates, resume_index):
        """Generate resume instructions for user"""
        self.logger.log_info("")
        self.logger.log_info("🔄 RESUME INSTRUCTIONS:")
        self.logger.log_info("-" * 60)
        
        if duplicates:
            self.logger.log_warning(f"⚠️  {len(duplicates)} duplicate pins detected!")
            self.logger.log_warning("   Actions needed:")
            self.logger.log_warning("   1. Check duplicates.json for list of duplicates")
            self.logger.log_warning("   2. Manually remove duplicate saves from Pinterest")
            self.logger.log_warning("   3. Run 'python main.py copy' again after cleanup")
            return False
        
        if not remaining_pins:
            self.logger.log_success("✅ All pins already saved! Nothing to do.")
            return False
        
        # Handle None resume_index
        if resume_index is None:
            resume_index = 0
        
        self.logger.log_info(f"✅ Ready to resume from pin #{resume_index + 1}")
        self.logger.log_info(f"   {len(remaining_pins)} pins remaining to save")
        self.logger.log_info("")
        self.logger.log_success("Run: python main.py copy")
        self.logger.log_info("-" * 60)
        
        return True

    def mark_pin_saved(self, pin_url):
        """Mark pin as saved in real-time checkpoint"""
        try:
            checkpoint = {
                'last_saved_pin': pin_url,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, ensure_ascii=False)
        except:
            pass

    def verify_inventory_integrity(self):
        """Verify inventory hasn't changed (board didn't change)"""
        if not self.inventory_file.exists():
            return True, None
        
        with open(self.inventory_file, 'r', encoding='utf-8') as f:
            inventory = json.load(f)
        
        old_checksum = inventory.get('checksum')
        old_total = inventory.get('total_pins')
        
        self.logger.log_info(f"Previous inventory: {old_total} pins")
        
        return True, old_checksum
