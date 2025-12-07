#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Pin Saver Module
Handles saving pins to target boards with smart board selection
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config

class PinterestSaver:
    """Saves pins to Pinterest boards"""
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)
    
    def save_pin_to_board(self, pin_url, target_board_name):
        """Save pin to specified board"""
        try:
            # Open pin
            self.logger.log_info(f"Opening pin: {pin_url}")
            self.driver.get(pin_url)
            time.sleep(2)
            
            # Check if already saved
            if self._is_already_saved():
                self.logger.log_info("[INFO] Pin already saved")
                # Try selecting board anyway
                if not self._click_saved_button():
                    return False
            else:
                # Click Save button
                if not self._click_save_button():
                    return False
            
            # Select target board from dialog
            if self._select_board(target_board_name):
                self.logger.log_success(f"Pin saved: {pin_url}")
                return True
            else:
                self.logger.log_error(f"Board selection failed: {target_board_name}")
                return False
                
        except Exception as e:
            self.logger.log_error(f"Error saving pin: {pin_url}", e)
            return False
    
    def _is_already_saved(self):
        """Check if pin is already saved"""
        try:
            saved_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(., 'Saved') or contains(., 'Kaydedildi')]"
            )
            return True
        except:
            return False
    
    def _click_saved_button(self):
        """Click 'Saved' button to change board"""
        try:
            saved_selectors = [
                (By.XPATH, "//button[contains(., 'Saved') or contains(., 'Kaydedildi')]"),
                (By.XPATH, "//div[@role='button' and (contains(., 'Saved') or contains(., 'Kaydedildi'))]"),
            ]
            
            for by, selector in saved_selectors:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    element.click()
                    time.sleep(2)
                    self.logger.log_info("[OK] 'Saved' button clicked")
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
            
            return False
        except Exception:
            return False
    
    def _click_save_button(self):
        """Click Save button"""
        try:
            save_selectors = [
                (By.XPATH, "//button[contains(@aria-label, 'Save') or contains(@aria-label, 'Kaydet')]"),
                (By.XPATH, "//button[contains(., 'Save') or contains(., 'Kaydet')]"),
                (By.CSS_SELECTOR, "[data-test-id='save-button']"),
                (By.XPATH, "//button[contains(@title, 'Save') or contains(@title, 'Kaydet')]"),
            ]
            
            for by, selector in save_selectors:
                try:
                    element = self.wait.until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    element.click()
                    time.sleep(1)
                    self.logger.log_info("[OK] Save button clicked")
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
            
            self.logger.log_warning("Save button selectors failed, trying alternative method...")
            return self._click_save_button_fallback()
            
        except Exception as e:
            self.logger.log_error("Save button click error", e)
            return False
    
    def _click_save_button_fallback(self):
        """Alternative method to click save button"""
        try:
            # Try finding by text content
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                try:
                    if "save" in button.text.lower() or "kaydet" in button.text.lower():
                        button.click()
                        time.sleep(2)
                        self.logger.log_info("[OK] Save button clicked (fallback)")
                        return True
                except:
                    continue
            
            return False
        except Exception as e:
            self.logger.log_error("Save button fallback error", e)
            return False
    
    def _select_board(self, target_board_name):
        """Select target board from save dialog"""
        try:
            time.sleep(3)  # Extra wait for dialog
            
            # Wait for dialog to open
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@role='dialog']"))
                )
                self.logger.log_info("Dialog opened")
            except TimeoutException:
                self.logger.log_warning("Dialog timeout - might not be a dialog, continuing...")
            
            time.sleep(2)
            
            # Scroll dialog to load more boards
            try:
                dialog = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                for _ in range(3):
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                    time.sleep(1)
                self.logger.log_info("Dialog scrolled")
            except Exception:
                pass
            
            # Click "See all boards" / "All boards" button if exists
            try:
                see_all_buttons = [
                    "//button[contains(text(), 'All') or contains(text(), 'See all')]",
                    "//div[contains(@role, 'button') and (contains(text(), 'All') or contains(text(), 'See all'))]",
                    "//span[contains(text(), 'All boards') or contains(text(), 'See all')]"
                ]
                for selector in see_all_buttons:
                    try:
                        btn = self.driver.find_element(By.XPATH, selector)
                        btn.click()
                        time.sleep(2)
                        self.logger.log_info("'See all boards' button clicked")
                        break
                    except:
                        continue
            except Exception:
                pass
            
            # Find target board
            self.logger.log_info(f"Searching for board: '{target_board_name}'")
            
            # Method 1: Direct selectors
            selectors = [
                (By.XPATH, f"//button[contains(text(), '{target_board_name}')]"),
                (By.XPATH, f"//div[contains(@role, 'button') and contains(text(), '{target_board_name}')]"),
                (By.XPATH, f"//span[contains(text(), '{target_board_name}')]"),
                (By.XPATH, f"//label[contains(text(), '{target_board_name}')]"),
                (By.CSS_SELECTOR, f"[data-test-id*='board-{target_board_name}']"),
            ]
            
            for by, selector in selectors:
                try:
                    elements = self.driver.find_elements(by, selector)
                    for elem in elements:
                        if elem.is_displayed():
                            self.logger.log_info(f"Selector found: {selector}")
                            elem.click()
                            time.sleep(2)
                            self.logger.log_info(f"[OK] Board selected: {target_board_name}")
                            return True
                except Exception:
                    continue
            
            # Method 2: Text search fallback
            self.logger.log_warning("Direct selectors failed, starting text search...")
            all_text_elements = self.driver.find_elements(By.XPATH, "//*[text()]")
            found_boards = []
            
            for elem in all_text_elements[:150]:
                try:
                    text = elem.text.strip()
                    if text and 1 < len(text) < 50:
                        found_boards.append(text)
                        if target_board_name.lower() in text.lower():
                            self.logger.log_info(f"Board match found: '{text}'")
                            try:
                                # Scroll into view
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                                time.sleep(1)
                                
                                # Click
                                elem.click()
                                time.sleep(2)
                                self.logger.log_info(f"[OK] Board selected: {target_board_name}")
                                return True
                            except Exception as click_err:
                                self.logger.log_warning(f"Click error: {click_err}")
                                # Try parent element
                                try:
                                    parent = elem.find_element(By.XPATH, "..")
                                    parent.click()
                                    time.sleep(2)
                                    self.logger.log_info(f"[OK] Board selected (via parent): {target_board_name}")
                                    return True
                                except Exception:
                                    continue
                except Exception:
                    continue
            
            # Debug: show found boards
            if found_boards:
                self.logger.log_warning(f"Found {len(set(found_boards))} boards: {', '.join(set(found_boards)[:10])}")
            
            # Final fallback
            self.logger.log_warning("Direct match failed, trying fallback...")
            return self._select_board_fallback(target_board_name)
        
        except Exception as e:
            self.logger.log_error("Board selection error", e)
            return False
    
    def _select_board_fallback(self, target_board_name):
        """Fallback method for board selection"""
        try:
            self.logger.log_info("Scanning all page elements...")
            
            # Search all page elements for board name
            all_elements = self.driver.find_elements(By.XPATH, "//*")
            
            for element in all_elements[:200]:
                try:
                    text = element.text.strip()
                    if text and target_board_name.lower() in text.lower():
                        # Try to click element or its parent
                        try:
                            element.click()
                            time.sleep(2)
                            self.logger.log_success(f"[OK] Board selected (fallback): {target_board_name}")
                            return True
                        except:
                            try:
                                parent = element.find_element(By.XPATH, "..")
                                parent.click()
                                time.sleep(2)
                                self.logger.log_success(f"[OK] Board selected (fallback parent): {target_board_name}")
                                return True
                            except:
                                continue
                except:
                    continue
            
            self.logger.log_error(f"Target board not found: {target_board_name}")
            return False
            
        except Exception as e:
            self.logger.log_error("Fallback selection error", e)
            return False
