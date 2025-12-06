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
        Scroll page to load all pins
        Uses improved algorithm for large boards (hundreds of pins)
        """
        pin_urls = set()
        scroll_pause_time = Config.SCROLL_PAUSE_TIME
        max_scrolls = Config.MAX_SCROLLS
        no_change_threshold = 5  # Increased from 3 to 5 for better detection
        
        self.logger.log_info(f"Maximum {max_scrolls} scrolls will be performed...")
        
        no_change_count = 0
        scroll_count = 0
        last_pin_count = 0
        
        while scroll_count < max_scrolls:
            # Get all pin links on page
            try:
                pin_elements = self.driver.find_elements(
                    By.XPATH,
                    "//a[contains(@href, '/pin/')]"
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
                
                # Report progress every 5 scrolls
                if scroll_count % 5 == 0:
                    self.logger.log_info(f"Scroll {scroll_count}: {current_pin_count} pins loaded")
                
                # If no new pins after threshold, we've reached the end
                if no_change_count >= no_change_threshold:
                    self.logger.log_info(f"Scroll stopped - total {current_pin_count} pins loaded")
                    break
                
                last_pin_count = current_pin_count
                
                # Scroll down
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(scroll_pause_time)
                scroll_count += 1
                
            except Exception as e:
                self.logger.log_warning(f"Scroll error: {e}")
                break
        
        self.logger.log_info(
            f"Scroll completed: {scroll_count} iterations | Total pins: {len(pin_urls)}"
        )
        
        # Extract pin links
        pin_links = list(pin_urls)
        self.logger.log_info(f"Extracted pin links: {len(pin_links)}")
        
        return pin_links
