#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebDriver Manager Module
Handles Chrome WebDriver creation and management
"""

import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

class DriverManager:
    """Manages WebDriver lifecycle and configuration"""
    
    def __init__(self, logger):
        self.logger = logger
        self.driver = None
    
    def create_driver(self, use_profile=False):
        """Create and configure Chrome WebDriver"""
        self.logger.log_info("Downloading/checking ChromeDriver...")
        
        # Chrome options
        chrome_options = Options()
        
        # Use existing Chrome profile (optional)
        if use_profile and Config.CHROME_PROFILE_PATH:
            chrome_options.add_argument(f"user-data-dir={Config.CHROME_PROFILE_PATH}")
            self.logger.log_info(f"Using Chrome profile: {Config.CHROME_PROFILE_PATH}")
        
        # Headless mode
        if Config.HEADLESS_MODE:
            chrome_options.add_argument("--headless=new")
            self.logger.log_info("Running in headless mode")
        
        # Additional options for stability
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Suppress Chrome error logs
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--silent")

        # Exclude automation flags and logging
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option("useAutomationExtension", False)        # Get ChromeDriver path
        try:
            driver_path = ChromeDriverManager().install()
            self.logger.log_info(f"webdriver-manager path: {driver_path}")
            
            # Fix for Windows: webdriver-manager sometimes returns wrong path
            actual_driver_path = self._get_chromedriver_path(driver_path)
            
            # Create service
            service = Service(actual_driver_path)
            
            # Create driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.logger.log_success("WebDriver created successfully")
            
            return self.driver
            
        except Exception as e:
            self.logger.log_error("WebDriver creation failed", e)
            raise
    
    def _get_chromedriver_path(self, installed_path):
        """
        Fix ChromeDriver path on Windows
        webdriver-manager sometimes returns THIRD_PARTY_NOTICES file instead of .exe
        """
        # Check if path is valid executable
        if os.path.isfile(installed_path) and installed_path.endswith('.exe'):
            self.logger.log_success(f"ChromeDriver exe found: {installed_path}")
            return installed_path
        
        # Path is invalid or not exe - search for actual chromedriver.exe
        self.logger.log_warning(f"Path invalid or not exe: {installed_path}")
        
        # Get .wdm directory
        wdm_dir = Path.home() / ".wdm" / "drivers" / "chromedriver"
        
        if not wdm_dir.exists():
            raise FileNotFoundError(f".wdm directory not found: {wdm_dir}")
        
        self.logger.log_info(f".wdm directory found: {wdm_dir}")
        
        # Search for chromedriver.exe recursively
        for exe_path in wdm_dir.rglob("chromedriver.exe"):
            if exe_path.is_file():
                self.logger.log_success(f"ChromeDriver exe found: {exe_path}")
                return str(exe_path)
        
        raise FileNotFoundError(f"chromedriver.exe not found in {wdm_dir}")
    
    def quit(self):
        """Close WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.log_info("WebDriver closed")
            except Exception as e:
                self.logger.log_warning(f"Error closing WebDriver: {e}")
