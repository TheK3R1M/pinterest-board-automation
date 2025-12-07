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
        Automatically detects end of board (supports 2000+ pins)
        No manual scroll limit - stops when no new pins load
        """
        pin_urls = set()
        scroll_pause_time = Config.SCROLL_PAUSE_TIME
        no_change_threshold = 20  # INCREASED: Daha sabırlı bekle, Pinterest yavaş yükleyebilir
        
        # Adaptive scroll pause for large boards
        min_scroll_pause = 0.8  # INCREASED: Daha fazla bekleme
        max_scroll_pause = 2.5

        self.logger.log_info("Auto-scroll enabled - will detect board end automatically...")
        self.logger.log_info(f"⏳ Patience threshold: {no_change_threshold} scrolls without new pins")

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
                new_pins_this_scroll = current_pin_count - last_pin_count
                
                # Check if new pins were loaded
                if current_pin_count == last_pin_count:
                    no_change_count += 1
                else:
                    no_change_count = 0
                
                # Report progress every 5 scrolls with more detail
                if scroll_count % 5 == 0:
                    self.logger.log_info(f"📊 Scroll {scroll_count}: {current_pin_count} pins (+{new_pins_this_scroll} new) | No change: {no_change_count}/{no_change_threshold}")

                # If no new pins after threshold, we've reached the end
                if no_change_count >= no_change_threshold:
                    self.logger.log_success(f"✅ Board end detected - total {current_pin_count} pins loaded")
                    self.logger.log_info(f"ℹ️  Scrolled {scroll_count} times to reach the end")
                    break

                last_pin_count = current_pin_count

                # Adaptive scroll pause - DAHA YAVAŞ scroll = daha fazla pin yüklenir
                if current_pin_count > 1000:
                    adaptive_pause = 1.2  # Çok büyük tablolarda daha yavaş
                elif current_pin_count > 500:
                    adaptive_pause = 1.0
                elif current_pin_count > 200:
                    adaptive_pause = 1.5
                else:
                    adaptive_pause = scroll_pause_time

                # Scroll down - daha agresif scroll
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(adaptive_pause)

                # EXTRA: Biraz yukarı kaydır, sonra tekrar aşağı (Pinterest trigger için)
                if scroll_count % 3 == 0:  # Her 3 scrollda bir
                    self.driver.execute_script("window.scrollBy(0, -300);")
                    time.sleep(0.3)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)

                # Wait for render: attempt to detect new pins - DAHA UZUN BEKLEME
                wait_count = 0
                while wait_count < 10:  # 6'dan 10'a çıkardım
                    new_pins = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/pin/')]")
                    if len(new_pins) > current_pin_count:
                        break
                    time.sleep(0.4)  # 0.3'ten 0.4'e
                    wait_count += 1

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
