#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest Board Automation - Main Program

✨ NEW FEATURES:
- Progress bar (tqdm) for visual feedback
- Auto-resume from checkpoint (perfect for 1000+ pins)
- Retry logic for failed pins
- Duplicate detection
- Smart auto-scroll (no manual MAX_SCROLLS)
- Batch processing with auto-save

Usage:
    python main.py login    - Initial login and save cookies
    python main.py copy     - Copy board using cookies
    python main.py profile  - Copy board using Chrome profile
    python main.py retry    - Retry failed pins from last run
"""

import sys
import time
import json
import random
import argparse
from pathlib import Path
from tqdm import tqdm
from config import Config
from logger import PinterestLogger
from driver_manager import DriverManager
from pinterest_auth import PinterestAuth
from pinterest_scraper import PinterestScraper
from pinterest_saver import PinterestSaver, PinterestBlockError
from pinterest_inventory import PinterestInventoryManager

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
        choices=["login", "copy", "profile", "retry", "multi"],
        help="Operation mode: login, copy, profile, retry, multi (parallel boards)"
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
            
        elif args.mode == "retry":
            run_retry_failed(driver_manager, logger)
            
        elif args.mode == "multi":
            logger.log_warning("⚠️  EXPERIMENTAL: Multi-board mode (parallel copying)")
            logger.log_info("This feature requires 2+ board URLs in .env")
            run_multi_board(driver_manager, logger)

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

def run_retry_failed(driver_manager, logger):
    """Retry mode: Retry only failed pins from last run"""
    logger.log_info("MODE: Retry Failed Pins")
    logger.log_info("-" * 60)
    driver = driver_manager.create_driver(use_profile=False)
    auth = PinterestAuth(driver, logger)
    saver = PinterestSaver(driver, logger)

    # Load cookies
    if not auth.load_cookies():
        logger.log_error("Cookie loading failed. Run 'python main.py login' first.")
        return

    # Load failed pins from last run
    logs_dir = Path("logs")
    failed_files = sorted(logs_dir.glob("failed_pins_*.json"), reverse=True)
    
    if not failed_files:
        logger.log_info("No failed pins found from previous runs!")
        return
    
    latest_failed_file = failed_files[0]
    logger.log_info(f"Loading failed pins from: {latest_failed_file.name}")
    
    with open(latest_failed_file, 'r', encoding='utf-8') as f:
        failed_data = json.load(f)

    # Handle both formats: list or dict with 'failed_pins' key
    if isinstance(failed_data, list):
        failed_pins = failed_data
    else:
        failed_pins = failed_data.get('failed_pins', [])
    
    if not failed_pins:
        logger.log_info("No failed pins to retry!")
        return
    
    logger.log_info(f"Retrying {len(failed_pins)} failed pins...")
    logger.log_info("-" * 60)
    
    # Retry with progress bar
    successful_count = 0
    failed_count = 0
    
    with tqdm(total=len(failed_pins), desc="🔄 Retrying pins", unit="pin") as pbar:
        for pin_data in failed_pins:
            # Handle both string URLs and dict format
            if isinstance(pin_data, str):
                pin_url = pin_data
            else:
                pin_url = pin_data.get('pin_url', pin_data.get('url', ''))
            
            # Skip if no valid URL
            if not pin_url:
                logger.log_warning(f"Skipping invalid pin data: {pin_data}")
                pbar.update(1)
                continue

            block_retry = 0
            while True:
                try:
                    if saver.save_pin_to_board(pin_url, Config.TARGET_BOARD_NAME):
                        logger.add_success_pin(pin_url)
                        successful_count += 1
                        pbar.set_postfix({"✅": successful_count, "❌": failed_count}, refresh=False)
                    else:
                        logger.add_failed_pin(pin_url, "Retry failed")
                        failed_count += 1
                        pbar.set_postfix({"✅": successful_count, "❌": failed_count}, refresh=False)
                    
                    pbar.update(1)
                    
                    # Human-like delay
                    delay = Config.RANDOM_DELAY_MIN + random.random() * (
                        Config.RANDOM_DELAY_MAX - Config.RANDOM_DELAY_MIN
                    )
                    time.sleep(delay)
                    break
                    
                except PinterestBlockError:
                    block_retry += 1
                    wait_plan = [300, 600, 900]
                    wait_seconds = wait_plan[min(block_retry - 1, len(wait_plan) - 1)]
                    logger.log_warning(f"⚠️ Pinterest block during retry | attempt {block_retry}/3 | waiting {wait_seconds//60} min")
                    if block_retry >= 3:
                        logger.add_failed_pin(pin_url, "Block after retries")
                        failed_count += 1
                        pbar.update(1)
                        break
                    time.sleep(wait_seconds)
                    continue

                except Exception as e:
                    logger.log_error(f"Retry error: {pin_url}", e)
                    logger.add_failed_pin(pin_url, str(e))
                    failed_count += 1
                    pbar.update(1)
                    break
    
    logger.log_info("-" * 60)
    logger.log_success(f"Retry completed: {successful_count} successful, {failed_count} failed")

def copy_board(scraper, saver, logger):
    """
    Copy board: collect and save pins
    ✨ v2.1+ Features:
    - Inventory system (detects duplicates + resume point)
    - Auto-resume from checkpoint
    - Duplicate detection
    - Progress bar
    """
    # Initialize counters at the top to avoid undefined errors
    successful_count = 0
    failed_count = 0
    skipped_count = 0
    
    try:
        # Create checkpoint file path
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        progress_file = logs_dir / "progress_checkpoint.json"
        processed_pins = set()  # Track which pins have been processed

        logger.log_info("-" * 60)
        logger.log_info(f"Source Board: {Config.SOURCE_BOARD_URL}")
        logger.log_info(f"Target Board: {Config.TARGET_BOARD_NAME}")
        logger.log_info("-" * 60)

        # Initialize inventory manager
        inventory_mgr = PinterestInventoryManager(logger)

        # Collect pins
        logger.log_info("📍 Step 1: Scanning all pins from board...")
        pin_links = scraper.collect_pin_links(Config.SOURCE_BOARD_URL)

        if not pin_links:
            logger.log_error("No pins found!")
            return

        total_pins = len(pin_links)
        logger.log_info(f"Total {total_pins} pins collected")
        
        # Create or verify inventory
        logger.log_info("📍 Step 2: Creating inventory (to detect duplicates & resume point)...")
        inventory = inventory_mgr.create_inventory(pin_links)
        
        # Check for duplicates and find resume point
        logger.log_info("📍 Step 3: Checking for duplicates and previous progress...")
        remaining_pins, duplicates, resume_index = inventory_mgr.detect_duplicates()
        
        if not inventory_mgr.get_resume_instructions(remaining_pins, duplicates, resume_index):
            logger.log_warning("Cannot proceed - see instructions above")
            return

        if not remaining_pins:
            logger.log_success("✅ All pins already saved!")
            return

        logger.log_info("-" * 60)

        # Progress tracking (counters already initialized at top of function)
        failed_pins_dict = {}
        batch_size = 100
        start_time = time.time()
        
        # Save each pin with progress bar
        print()  # New line for progress bar
        with tqdm(total=len(remaining_pins), desc="💾 Saving pins", unit="pin", 
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
            
            for idx, pin_url in enumerate(remaining_pins, 1):
                block_retry = 0
                while True:
                    try:
                        # Save pin
                        if saver.save_pin_to_board(pin_url, Config.TARGET_BOARD_NAME):
                            logger.add_success_pin(pin_url)
                            successful_count += 1
                            processed_pins.add(pin_url)  # Track processed
                            pbar.set_postfix({"✅": successful_count, "❌": failed_count}, refresh=False)
                            
                            # Mark in inventory (real-time checkpoint)
                            inventory_mgr.mark_pin_saved(pin_url)
                        else:
                            logger.add_failed_pin(pin_url, "Save failed")
                            failed_pins_dict[pin_url] = "Save failed"
                            failed_count += 1
                            processed_pins.add(pin_url)  # Track as processed even if failed
                            pbar.set_postfix({"✅": successful_count, "❌": failed_count}, refresh=False)

                        pbar.update(1)

                        # Auto-save checkpoint every batch_size pins (only if progress_file exists)
                        if idx % batch_size == 0 and progress_file:
                            _save_checkpoint(progress_file, processed_pins, logger)
                        delay = Config.RANDOM_DELAY_MIN + random.random() * (
                            Config.RANDOM_DELAY_MAX - Config.RANDOM_DELAY_MIN
                        )
                        time.sleep(delay)
                        break  # pin done

                    except PinterestBlockError as blk:
                        block_retry += 1
                        wait_plan = [300, 600, 900]  # 5, 10, 15 minutes
                        wait_seconds = wait_plan[min(block_retry - 1, len(wait_plan) - 1)]
                        logger.log_warning(f"⚠️ Pinterest block detected on pin {pin_url} | attempt {block_retry}/3 | waiting {wait_seconds//60} min")
                        if block_retry >= 3:
                            logger.add_failed_pin(pin_url, "Block after retries")
                            failed_pins_dict[pin_url] = "Block after retries"
                            failed_count += 1
                            processed_pins.add(pin_url)
                            pbar.update(1)
                            break
                        time.sleep(wait_seconds)
                        continue  # retry same pin after backoff

                    except KeyboardInterrupt:
                        print()  # New line after progress bar
                        logger.log_warning("⚠️  Stopped by user!")
                        if progress_file:
                            _save_checkpoint(progress_file, processed_pins, logger)
                        logger.log_info(f"Progress saved: {idx}/{len(remaining_pins)} pins processed")
                        logger.log_info("💡 Run 'python main.py copy' again to resume from this point")
                        raise

                    except Exception as e:
                        logger.log_error(f"Pin processing error: {pin_url}", e)
                        logger.add_failed_pin(pin_url, str(e))
                        failed_pins_dict[pin_url] = str(e)
                        failed_count += 1
                        processed_pins.add(pin_url)
                        pbar.update(1)
                        break

        # Clean up checkpoint on successful completion
        print()  # New line after progress bar
        if progress_file and progress_file.exists():
            progress_file.unlink()
            logger.log_info("Checkpoint file deleted (all pins processed)")

        # Final summary
        elapsed_total = time.time() - start_time
        elapsed_minutes = int(elapsed_total // 60)
        elapsed_seconds = int(elapsed_total % 60)

        logger.log_info("-" * 60)
        logger.log_success("🎉 Board copy completed!")
        logger.log_info(f"✅ Successful: {successful_count}")
        logger.log_info(f"❌ Failed: {failed_count}")
        if skipped_count > 0:
            logger.log_info(f"⏭️  Skipped (already processed): {skipped_count}")
        logger.log_info(f"⏱️  Total time: {elapsed_minutes} min {elapsed_seconds} sec")
        
        if failed_count > 0:
            logger.log_info(f"\n💡 TIP: Run 'python main.py retry' to retry failed pins")

    except KeyboardInterrupt:
        logger.log_warning("\n\n⚠️  Operation stopped by user!")
        logger.log_info(f"So far: {successful_count} successful, {failed_count} failed")

    except Exception as e:
        logger.log_error("Unexpected error", e)

def _save_checkpoint(progress_file, processed_pins, logger):
    """Save progress checkpoint to file"""
    try:
        checkpoint = {
            'processed': list(processed_pins),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': len(processed_pins)
        }
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.log_warning(f"Could not save checkpoint: {e}")

def run_multi_board(driver_manager, logger):
    """
    EXPERIMENTAL: Multi-board parallel copying
    Copies from multiple source boards to multiple target boards in parallel
    
    For best performance:
    - Create multiple rows in .env separated by commas:
      SOURCE_BOARD_URL_1=https://...
      TARGET_BOARD_NAME_1=Board1
      SOURCE_BOARD_URL_2=https://...
      TARGET_BOARD_NAME_2=Board2
    """
    logger.log_info("MODE: Multi-Board Parallel Copy (EXPERIMENTAL)")
    logger.log_info("-" * 60)
    
    # Parse multi-board config (future enhancement)
    logger.log_info("❌ Multi-board mode not yet implemented")
    logger.log_info("💡 For now, run 'python main.py copy' multiple times with different .env settings")
    logger.log_warning("Future version will support parallel board copying with 2+ Chrome instances")
    
    return

if __name__ == "__main__":
    main()
