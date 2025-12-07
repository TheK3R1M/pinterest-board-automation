#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Scraper Test Script
Sadece kaç pin bulunduğunu test eder (kaydetmez)
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from logger import PinterestLogger
from driver_manager import DriverManager
from pinterest_auth import PinterestAuth
from pinterest_scraper import PinterestScraper

def test_scraper():
    """Test scraper - kaç pin bulduğunu göster"""
    logger = PinterestLogger()
    logger.log_info("=" * 60)
    logger.log_info("Pinterest Scraper Test - Pin Sayısı Kontrolü")
    logger.log_info("=" * 60)
    
    driver_manager = DriverManager(logger)
    
    try:
        # Create driver
        driver = driver_manager.create_driver(use_profile=False)
        auth = PinterestAuth(driver, logger)
        
        # Load cookies
        if not auth.load_cookies():
            logger.log_error("Cookie yüklenemedi. Önce 'python main.py login' çalıştırın")
            return
        
        # Create scraper
        scraper = PinterestScraper(driver, logger)
        
        # Test scraping
        logger.log_info(f"Kaynak tablo: {Config.SOURCE_BOARD_URL}")
        logger.log_info("-" * 60)
        
        pin_links = scraper.collect_pin_links(Config.SOURCE_BOARD_URL)
        
        logger.log_info("=" * 60)
        logger.log_success(f"✅ Toplam {len(pin_links)} pin bulundu!")
        logger.log_info("=" * 60)
        
        # İlk 5 pin'i göster
        if pin_links:
            logger.log_info("İlk 5 pin:")
            for i, pin in enumerate(pin_links[:5], 1):
                logger.log_info(f"  {i}. {pin}")
        
    except Exception as e:
        logger.log_error("Test hatası", e)
    
    finally:
        driver_manager.quit()
        logger.save_logs()

if __name__ == "__main__":
    test_scraper()
