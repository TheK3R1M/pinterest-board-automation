# 📌 Pinterest Board Automation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium 4.x](https://img.shields.io/badge/selenium-4.x-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![1000+ Pins Supported](https://img.shields.io/badge/pins-1000+-brightgreen.svg)
![Auto Resume](https://img.shields.io/badge/resume-auto-orange.svg)

Automated Pinterest board-to-board pin copying tool using Python and Selenium. Copy **1000+ pins** efficiently with **auto-resume**, **progress bar**, **smart scrolling**, and **retry logic**.

## ✨ Features

- 🔐 **Cookie-based Authentication** - No API key required, just login once
- 🎯 **Smart Board Selector** - Auto-finds and selects target board with scroll support
- 📊 **Visual Progress Bar** - Real-time tqdm progress bar with ETA
- 🔄 **Smart Auto-Scroll** - Automatically detects board end (no manual limit!)
- 💾 **Auto-Resume Capability** - Interrupted? Resume from checkpoint
- 🔁 **Retry Failed Pins** - One-command retry for failed pins
- 🤖 **Anti-Bot Protection** - Random delays and human-like behavior
- 📝 **Detailed Logging** - Success/failed pins saved to JSON
- ⚡ **Handles 1000+ Pins** - Tested and optimized for large boards
- 🚫 **Duplicate Detection** - Skips already processed pins
- 🌐 **Cross-Platform** - Windows, Linux, macOS support
- 🔀 **Multiple Modes** - Cookie-based, Chrome profile-based, or headless

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Pinterest account

### Installation

1. **Clone repository**
```bash
git clone https://github.com/TheK3R1M/pinterest-board-automation.git
cd pinterest-board-automation
```

2. **Create virtual environment** (optional but recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
PINTEREST_EMAIL=your.email@example.com
PINTEREST_PASSWORD=your_password
SOURCE_BOARD_URL=https://www.pinterest.com/username/source-board/
TARGET_BOARD_NAME=Target Board Name
```

### Usage

#### Step 1: Initial Login (One-time)

**Windows (PowerShell):**
```powershell
python main.py login
```

**Linux/macOS:**
```bash
python3 main.py login
```

- Browser opens Pinterest login page
- Enter your email and password
- Complete 2FA if prompted (2-factor authentication)
- Cookies are saved automatically to `pinterest_cookies.json`

#### Step 2: Copy Pins

**Windows (PowerShell):**
```powershell
python main.py copy
```

**Linux/macOS:**
```bash
python3 main.py copy
```

- Loads saved cookies from previous login
- **Smart auto-scroll** - automatically detects board end
- Collects all pins from source board
- Saves each pin with **visual progress bar**
- **Auto-saves checkpoint** every 100 pins
- Logs results to JSON files in `logs/` directory
- Press Ctrl+C to pause - run again to **resume from checkpoint**

#### Alternative: Use Chrome Profile

**Windows (PowerShell):**
```powershell
python main.py profile
```

**Linux/macOS:**
```bash
python3 main.py profile
```

Uses existing Chrome profile (first set `CHROME_PROFILE_PATH` in `.env`)

#### Step 3: Retry Failed Pins (Optional)

If some pins failed, retry them with one command:

**Windows (PowerShell):**
```powershell
python main.py retry
```

**Linux/macOS:**
```bash
python3 main.py retry
```

- Automatically loads failed pins from last run
- Retries with visual progress bar
- Perfect for network issues or temporary errors

#### Check Your Results

After copying, check the `logs/` folder for:
- `success_pins_TIMESTAMP.json` - Successfully saved pins
- `failed_pins_TIMESTAMP.json` - Pins that failed (with reasons)
- `progress_checkpoint.json` - Resume checkpoint (auto-deleted when complete)

## 📋 Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `PINTEREST_EMAIL` | - | Your Pinterest email |
| `PINTEREST_PASSWORD` | - | Your Pinterest password |
| `SOURCE_BOARD_URL` | - | Full URL of source board |
| `TARGET_BOARD_NAME` | - | Name of destination board |
| `CHROME_PROFILE_PATH` | - | Chrome profile directory (optional) |
| `HEADLESS_MODE` | false | Run without browser window |
| `SCROLL_PAUSE_TIME` | 0.8 | Seconds between scrolls (adaptive for large boards) |
| `RANDOM_DELAY_MIN` | 2 | Min delay between pins (seconds) |
| `RANDOM_DELAY_MAX` | 5 | Max delay between pins (seconds) |
| `LOG_FAILED_PINS` | true | Save failed pins to JSON |

**Note:** `MAX_SCROLLS` removed - now uses smart auto-scroll detection that automatically stops when board end is reached.

## 📁 Project Structure

```
pinterest-board-automation/
├── main.py                 # Entry point & CLI
├── config.py              # Configuration loader
├── logger.py              # Logging system
├── driver_manager.py      # WebDriver management
├── pinterest_auth.py      # Authentication & cookies
├── pinterest_scraper.py   # Pin collection
├── pinterest_saver.py     # Pin saving logic
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
├── README.md              # This file
├── CONTRIBUTING.md        # Contributing guide
└── logs/                  # Auto-generated logs
    ├── success_pins_*.json
    └── failed_pins_*.json
```

## 🔧 Troubleshooting

### "Cookie loading failed"
- Run `python main.py login` first
- Verify `pinterest_cookies.json` exists
- Cookies expire after ~30 days, re-login if needed

### "No pins found"
- Check `SOURCE_BOARD_URL` is correct and accessible
- Smart auto-scroll will detect all pins automatically
- Verify board is public

### "Target board not found"
- Ensure board exists in your account
- Add at least 1 pin to board (Pinterest requirement)
- Verify exact spelling in `TARGET_BOARD_NAME`

### "ChromeDriver version mismatch"
- Script auto-downloads correct driver
- Update Chrome to latest version
- Check internet connection

### Browser opens but nothing happens
- Set `HEADLESS_MODE=false` to see browser
- Check if Pinterest is blocking automation
- Verify credentials are correct

## ⚠️ Important Notes

- **Legal:** Use responsibly and comply with Pinterest's Terms of Service
- **Rate Limiting:** Script includes delays to avoid detection
- **Target Board:** Must exist and have ≥1 pin before copying
- **Privacy:** Never commit `.env` or `pinterest_cookies.json` to Git
- **2FA:** Supported - complete verification when prompted
- **Session Expiry:** Cookies valid for ~30 days

## 📊 Performance

### v2.1 Optimizations (NEW!)
- ⚡ **70% faster board selection** - reduced dialog wait from 3s to 1s, eliminated duplicate searches
- ✅ **Fixed scroll bug** - now scrolls correct element (dialog vs page)
- 🎯 **Better pin detection** - catches more pin variations (now detects ~2.2k instead of 1.8k)
- 🚀 **Reduced element searches** - from 150+ to 50 elements per iteration

### Speed Improvements:
- Per-pin time: **~10-15 seconds** (down from 30+)
- 1000 pins: **~3-4 hours** (down from 8+ hours)
- 500 pins: **~2 hours** (down from 4+ hours)

### Estimated Times by Board Size:
| Board Size | Old Time | New Time | Improvement |
|-----------|----------|----------|------------|
| 50 pins | 25 min | 10-15 min | **60% faster** |
| 200 pins | 90 min | 30-40 min | **60% faster** |
| 500 pins | 4-5 hours | 1.5-2 hours | **65% faster** |
| 1000+ pins | 8-10 hours | 3-4 hours | **65% faster** |

*Times vary based on network, delays, and system performance*

**Note:** Set `SCROLL_PAUSE_TIME=0.5` in `.env` for even faster performance if your internet is stable!

## 🐛 Troubleshooting

### Problem: Stops at 100 pins

**Possible causes:**
1. **Pinterest rate limiting** - Pinterest may block after too many saves
   - **Solution:** Wait 5-10 minutes, then run retry mode: `python main.py retry`
   - Use higher `RANDOM_DELAY_MIN` and `RANDOM_DELAY_MAX` (e.g., 3-7 seconds)

2. **Captcha/Bot detection**
   - **Solution:** Run with `HEADLESS_MODE=false` to manually solve captcha
   - Clear browser cache: delete `pinterest_cookies.json` and login again

3. **Session timeout**
   - **Solution:** Login again: `python main.py login`

### Problem: Finds fewer pins than expected (e.g., 1600 instead of 2202)

**Causes:**
- Pinterest's lazy loading not completing
- Scroll timeout too aggressive

**Solutions:**
1. **Test scraping first:**
   ```bash
   python test_scraper.py
   ```
   This shows how many pins are actually collected

2. **Adjust scroll settings in `.env`:**
   ```env
   SCROLL_PAUSE_TIME=1.5  # Increase from 0.8 to 1.5
   ```

3. **Run in non-headless mode** to watch the scroll:
   ```env
   HEADLESS_MODE=false
   ```

4. **Check the logs** in `logs/` folder for scroll statistics

### Problem: Board not found

**Solutions:**
- Make sure `TARGET_BOARD_NAME` matches **exactly** (case-sensitive)
- Try shortening the board name if it's too long
- Create the target board manually first on Pinterest

### Problem: Chrome driver issues

**Solutions:**
```bash
pip install --upgrade selenium webdriver-manager
```

## 🐛 Issues & Support

When reporting issues, include:
- Python version (`python --version`)
- Operating system
- Error message and logs
- Last successful step
- Output from `python test_scraper.py`

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Help
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔍 Review pull requests
- ⭐ Star this project

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📚 Related Resources

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pinterest URL Format](https://help.pinterest.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## ⭐ Support

If this project helped you, please:
- ⭐ Give it a star on GitHub
- 🐦 Share with others
- 📝 Provide feedback

---

**Disclaimer:** This tool is for educational purposes. Users are responsible for complying with Pinterest's Terms of Service and applicable laws. The authors are not liable for misuse or violations.

Built with ❤️ using Python and Selenium
