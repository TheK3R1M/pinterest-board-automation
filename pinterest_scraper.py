#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Board Scraper Module
Collects pin links from Pinterest boards using optimized scrolling
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

class PinterestScraper:
    """Scrapes pin links from Pinterest boards"""
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)
    
    def collect_pin_links(self, board_url):
        """
        Collect all pin links from board
        Optimized for hundreds of pins with improved scrolling
        """
        self.logger.log_info(f"Collecting pins: {board_url}")
        
        # Navigate to board
        self.driver.get(board_url)
        time.sleep(3)
        
        # Scroll and collect pins
        pin_links = self._scroll_to_load_all()
        
        self.logger.log_success(f"Total pins collected: {len(pin_links)}")
        return pin_links
    
    def _scroll_to_load_all(self):
        """
        Scroll page to load all pins with smart auto-detection
        Automatically detects end of board (supports 1000+ pins)
        No manual scroll limit - stops when no new pins load
        """
        pin_urls = set()
        scroll_pause_time = Config.SCROLL_PAUSE_TIME
        no_change_threshold = 8  # Increased to 8 for better reliability on large boards
        
        # Adaptive scroll pause for large boards
        min_scroll_pause = 0.5
        max_scroll_pause = 2.0

        self.logger.log_info("Auto-scroll enabled - will detect board end automatically...")

        no_change_count = 0
        scroll_count = 0
        last_pin_count = 0
        consecutive_errors = 0

        while True:  # Infinite scroll until end detected
            # Get all pin links on page
            try:
                # OPTIMIZATION: Use multiple selectors to catch all pin variations
                pin_elements = self.driver.find_elements(
                    By.XPATH,
                    "//a[contains(@href, '/pin/') or contains(@data-test-id, 'pin') or ancestor::*[@data-test-id and contains(@data-test-id, 'Pin')]]"
                )
                
                for element in pin_elements:
                    try:
                        href = element.get_attribute("href")
                        if href and "/pin/" in href:
                            # Extract clean pin URL
                            pin_id = href.split("/pin/")[1].split("/")[0]
                            clean_url = f"https://tr.pinterest.com/pin/{pin_id}/"
                            pin_urls.add(clean_url)
                    except:
                        continue
                
                current_pin_count = len(pin_urls)
                
                # Check if new pins were loaded
                if current_pin_count == last_pin_count:
                    no_change_count += 1
                else:
                    no_change_count = 0
                
                # Report progress every 10 scrolls
                if scroll_count % 10 == 0:
                    self.logger.log_info(f"Scroll {scroll_count}: {current_pin_count} pins loaded")

                # If no new pins after threshold, we've reached the end
                if no_change_count >= no_change_threshold:
                    self.logger.log_success(f"Board end detected - total {current_pin_count} pins loaded")
                    break

                last_pin_count = current_pin_count

                # Adaptive scroll pause (faster for large boards)
                if current_pin_count > 500:
                    adaptive_pause = min_scroll_pause
                elif current_pin_count > 200:
                    adaptive_pause = (min_scroll_pause + scroll_pause_time) / 2
                else:
                    adaptive_pause = scroll_pause_time

                # Scroll down
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(adaptive_pause)
                scroll_count += 1
                consecutive_errors = 0  # Reset on success

            except Exception as e:
                consecutive_errors += 1
                self.logger.log_warning(f"Scroll error ({consecutive_errors}/3): {e}")
                if consecutive_errors >= 3:
                    self.logger.log_error("Too many scroll errors, stopping...")
                    break
                time.sleep(2)  # Wait before retry
        
        self.logger.log_info(
            f"Scroll completed: {scroll_count} iterations | Total pins: {len(pin_urls)}"
        )
        
        # Extract pin links
        pin_links = list(pin_urls)
        self.logger.log_info(f"Extracted pin links: {len(pin_links)}")
        
        return pin_links
