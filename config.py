#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Management Module
Loads and validates environment variables from .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Pinterest automation"""
    
    # Pinterest credentials
    PINTEREST_EMAIL = os.getenv("PINTEREST_EMAIL", "")
    PINTEREST_PASSWORD = os.getenv("PINTEREST_PASSWORD", "")
    
    # Chrome profile path (optional)
    CHROME_PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", "")
    
    # Board settings
    SOURCE_BOARD_URL = os.getenv("SOURCE_BOARD_URL", "")
    TARGET_BOARD_NAME = os.getenv("TARGET_BOARD_NAME", "")
    
    # Selenium settings
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "false").lower() == "true"
    SCROLL_PAUSE_TIME = float(os.getenv("SCROLL_PAUSE_TIME", "0.8"))
    # MAX_SCROLLS removed - now uses smart auto-scroll detection
    
    # Random delay settings (seconds)
    RANDOM_DELAY_MIN = float(os.getenv("RANDOM_DELAY_MIN", "2"))
    RANDOM_DELAY_MAX = float(os.getenv("RANDOM_DELAY_MAX", "5"))
    
    # Logging settings
    LOG_FAILED_PINS = os.getenv("LOG_FAILED_PINS", "true").lower() == "true"

    # Performance settings (NEW in v2.1)
    MAX_PARALLEL_WORKERS = int(os.getenv("MAX_PARALLEL_WORKERS", "1"))  # 1 = single, 2+ = parallel boards
    
    # Cookie file path
    COOKIE_FILE = "pinterest_cookies.json"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.SOURCE_BOARD_URL:
            raise ValueError("SOURCE_BOARD_URL is required in .env file")
        
        if not cls.TARGET_BOARD_NAME:
            raise ValueError("TARGET_BOARD_NAME is required in .env file")
        
        if cls.SCROLL_PAUSE_TIME <= 0:
            raise ValueError("SCROLL_PAUSE_TIME must be positive")

        if cls.RANDOM_DELAY_MIN < 0 or cls.RANDOM_DELAY_MAX < cls.RANDOM_DELAY_MIN:
            raise ValueError("Invalid RANDOM_DELAY settings")
