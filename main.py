#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Board Automation - Main Program

Usage:
    python main.py login    - Initial login and save cookies
    python main.py copy     - Copy board using cookies
    python main.py profile  - Copy board using Chrome profile
"""

import sys
import time
import argparse
from config import Config
from logger import PinterestLogger
from driver_manager import DriverManager
from pinterest_auth import PinterestAuth
from pinterest_scraper import PinterestScraper
from pinterest_saver import PinterestSaver

def main():
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}")
        return
    
    # Initialize logger
    logger = PinterestLogger()
    logger.log_info("=" * 60)
    logger.log_info("Pinterest Board Automation Started")
    logger.log_info("=" * 60)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Pinterest Board Copy Automation Tool"
    )
    parser.add_argument(
        "mode",
        choices=["login", "copy", "profile"],
        help="Operation mode: login (initial login), copy (cookie-based), profile (profile-based)"
    )
    
    args = parser.parse_args()
    
    # Create driver manager
    driver_manager = DriverManager(logger)
    
    try:
        if args.mode == "login":
            run_login(driver_manager, logger)
        
        elif args.mode == "copy":
            run_copy_with_cookies(driver_manager, logger)
        
        elif args.mode == "profile":
            run_copy_with_profile(driver_manager, logger)
    
    except KeyboardInterrupt:
        logger.log_warning("Stopped by user (Ctrl+C)")
    
    except Exception as e:
        logger.log_error("Unexpected error", e)
    
    finally:
        driver_manager.quit()
        logger.save_logs()
        logger.log_success(f"Result: {logger.get_summary()}")
        logger.log_info("=" * 60)

def run_login(driver_manager, logger):
    """Authentication mode: login and save cookies"""
    logger.log_info("MODE: Login and Cookie Saving")
    logger.log_info("-" * 60)
    
    driver = driver_manager.create_driver(use_profile=False)
    auth = PinterestAuth(driver, logger)
    
    # Check credentials
    if not Config.PINTEREST_EMAIL or not Config.PINTEREST_PASSWORD:
        logger.log_error("Email or password missing. Check .env file.")
        return
    
    # Login
    if auth.login_with_credentials():
        # Save cookies
        auth.save_cookies()
        logger.log_success("Login completed successfully!")
    else:
        logger.log_error("Login failed!")

def run_copy_with_cookies(driver_manager, logger):
    """Cookie mode: Copy board using saved cookies"""
    logger.log_info("MODE: Cookie-based Board Copy")
    logger.log_info("-" * 60)
    
    driver = driver_manager.create_driver(use_profile=False)
    auth = PinterestAuth(driver, logger)
    scraper = PinterestScraper(driver, logger)
    saver = PinterestSaver(driver, logger)
    
    # Load cookies
    if not auth.load_cookies():
        logger.log_error("Cookie loading failed. Run 'python main.py login' first.")
        return
    
    # Start board copy operation
    copy_board(scraper, saver, logger)

def run_copy_with_profile(driver_manager, logger):
    """Profile mode: Copy board using Chrome profile"""
    logger.log_info("MODE: Chrome Profile-based Board Copy")
    logger.log_info("-" * 60)
    
    if not Config.CHROME_PROFILE_PATH:
        logger.log_error(
            "Chrome profile path not defined. "
            "Set CHROME_PROFILE_PATH environment variable."
        )
        return
    
    driver = driver_manager.create_driver(use_profile=True)
    scraper = PinterestScraper(driver, logger)
    saver = PinterestSaver(driver, logger)
    
    # Start board copy operation
    copy_board(scraper, saver, logger)

def copy_board(scraper, saver, logger):
    """Copy board: collect and save pins - Optimized for hundreds of pins"""
    try:
        logger.log_info("-" * 60)
        logger.log_info(f"Source Board: {Config.SOURCE_BOARD_URL}")
        logger.log_info(f"Target Board: {Config.TARGET_BOARD_NAME}")
        logger.log_info("-" * 60)
        
        # Collect pins
        pin_links = scraper.collect_pin_links(Config.SOURCE_BOARD_URL)
        
        if not pin_links:
            logger.log_error("No pins found!")
            return
        
        total_pins = len(pin_links)
        logger.log_info(f"Total {total_pins} pins to save...")
        logger.log_info("-" * 60)
        
        # Progress tracking
        successful_count = 0
        failed_count = 0
        batch_size = 50  # Report every 50 pins
        start_time = time.time()
        
        # Save each pin
        for idx, pin_url in enumerate(pin_links, 1):
            try:
                # Progress display
                progress = (idx / total_pins) * 100
                logger.log_info(f"[{idx}/{total_pins}] ({progress:.1f}%) Processing...")
                
                # Save pin
                if saver.save_pin_to_board(pin_url, Config.TARGET_BOARD_NAME):
                    logger.add_success_pin(pin_url)
                    successful_count += 1
                else:
                    logger.add_failed_pin(pin_url, "Save failed")
                    failed_count += 1
                
                # Batch progress report
                if idx % batch_size == 0:
                    elapsed_time = time.time() - start_time
                    avg_time_per_pin = elapsed_time / idx
                    remaining_pins = total_pins - idx
                    estimated_remaining = remaining_pins * avg_time_per_pin
                    
                    batch_progress = (idx / total_pins) * 100
                    elapsed_minutes = int(elapsed_time // 60)
                    elapsed_seconds = int(elapsed_time % 60)
                    est_remaining_minutes = int(estimated_remaining // 60)
                    est_remaining_seconds = int(estimated_remaining % 60)
                    
                    logger.log_info("=" * 60)
                    logger.log_success(f"✓ {successful_count}/{total_pins} pins saved successfully ({batch_progress:.1f}%)")
                    logger.log_info(f"  Elapsed time: {elapsed_minutes} min {elapsed_seconds} sec")
                    logger.log_info(f"  Estimated remaining: {est_remaining_minutes} min {est_remaining_seconds} sec")
                    logger.log_info("=" * 60)
                
                # Human-like random delay
                import random
                delay = Config.RANDOM_DELAY_MIN + random.random() * (
                    Config.RANDOM_DELAY_MAX - Config.RANDOM_DELAY_MIN
                )
                logger.log_info(f"[WAIT] Delay: {delay:.1f} seconds")
                time.sleep(delay)
            
            except KeyboardInterrupt:
                logger.log_warning("Stopped by user!")
                logger.log_info(f"Progress: {idx}/{total_pins} pins processed")
                break
            
            except Exception as e:
                logger.log_error(f"Pin processing error: {pin_url}", e)
                logger.add_failed_pin(pin_url, str(e))
                failed_count += 1
        
        # Final summary
        elapsed_total = time.time() - start_time
        elapsed_minutes = int(elapsed_total // 60)
        elapsed_seconds = int(elapsed_total % 60)
        
        logger.log_info("-" * 60)
        logger.log_success("Board copy completed!")
        logger.log_info(f"Total time: {elapsed_minutes} min {elapsed_seconds} sec")
    
    except KeyboardInterrupt:
        logger.log_warning("\n\nOperation stopped by user!")
        logger.log_info(f"So far: {successful_count} successful, {failed_count} failed")
    
    except Exception as e:
        logger.log_error("Unexpected error", e)

if __name__ == "__main__":
    main()
