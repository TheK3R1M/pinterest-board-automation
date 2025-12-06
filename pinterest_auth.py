#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Authentication Module
Handles login, cookie management, and session persistence
"""

import json
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import Config

class PinterestAuth:
    """Handles Pinterest authentication and cookies"""
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.cookie_file = Path(Config.COOKIE_FILE)
        self.wait = WebDriverWait(driver, 10)
    
    def login_with_credentials(self):
        """Login to Pinterest using email and password"""
        try:
            self.logger.log_info("Opening Pinterest login page...")
            self.driver.get("https://www.pinterest.com/login/")
            time.sleep(3)
            
            # Enter email
            self.logger.log_info("Entering email...")
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_input.send_keys(Config.PINTEREST_EMAIL)
            
            # Enter password
            self.logger.log_info("Entering password...")
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(Config.PINTEREST_PASSWORD)
            
            # Click login button
            self.logger.log_info("Clicking login button...")
            login_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit']"
            )
            login_button.click()
            
            # Wait for 2FA or redirect
            self.logger.log_info("Waiting for login (2FA supported - complete if prompted)...")
            time.sleep(5)
            
            # Check if 2FA is required
            try:
                two_fa_element = self.driver.find_element(
                    By.XPATH, "//*[contains(text(), 'verification') or contains(text(), 'code')]"
                )
                self.logger.log_warning("2FA detected! Please complete verification in browser...")
                self.logger.log_info("Waiting up to 120 seconds for 2FA completion...")
                time.sleep(120)  # Wait 2 minutes for user to complete 2FA
            except:
                pass  # No 2FA, continue
            
            # Verify login success
            time.sleep(5)
            if self._is_logged_in():
                self.logger.log_success("Login successful!")
                return True
            else:
                self.logger.log_error("Login failed - not redirected to homepage")
                return False
                
        except Exception as e:
            self.logger.log_error("Login error", e)
            return False
    
    def _is_logged_in(self):
        """Check if successfully logged in"""
        try:
            # Check if we're on Pinterest homepage or have user menu
            current_url = self.driver.current_url
            return "pinterest.com" in current_url and "/login" not in current_url
        except:
            return False
    
    def save_cookies(self):
        """Save cookies to file"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookie_file, "w") as f:
                json.dump(cookies, f)
            self.logger.log_success(f"Cookies saved: {self.cookie_file}")
            return True
        except Exception as e:
            self.logger.log_error("Cookie save error", e)
            return False
    
    def load_cookies(self):
        """Load cookies from file"""
        try:
            if not self.cookie_file.exists():
                self.logger.log_error(f"Cookie file not found: {self.cookie_file}")
                return False
            
            # Navigate to Pinterest first
            self.logger.log_info("Opening Pinterest...")
            self.driver.get("https://www.pinterest.com/")
            time.sleep(2)
            
            # Load cookies
            with open(self.cookie_file, "r") as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    # Some cookies might fail to add, that's okay
                    pass
            
            # Refresh page with cookies
            self.driver.refresh()
            time.sleep(3)
            
            # Verify cookies worked
            if self._is_logged_in():
                self.logger.log_success("Cookies loaded successfully")
                return True
            else:
                self.logger.log_warning("Cookies loaded but login verification failed")
                return False
                
        except Exception as e:
            self.logger.log_error("Cookie load error", e)
            return False
