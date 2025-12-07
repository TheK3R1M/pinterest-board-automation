# 📌 Pinterest Board Automation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium 4.x](https://img.shields.io/badge/selenium-4.x-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated Pinterest board-to-board pin copying tool using Python and Selenium. Copy hundreds of pins efficiently with smart board selection, rate limiting, and comprehensive logging.

## ✨ Features

- 🔐 **Cookie-based Authentication** - No API key required, just login once
- 🎯 **Smart Board Selector** - Auto-finds and selects target board with scroll support
- 📊 **Progress Tracking** - Real-time batch reports every 50 pins
- 🔄 **Optimized Scrolling** - Efficiently loads all pins from large boards
- 🤖 **Anti-Bot Protection** - Random delays and human-like behavior
- 📝 **Detailed Logging** - Success/failed pins saved to JSON
- ⚡ **Handles Hundreds of Pins** - Tested and optimized for 100+ pins
- 🌐 **Cross-Platform** - Windows, Linux, macOS support
- 🎮 **Multiple Modes** - Cookie-based, Chrome profile-based, or headless

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

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
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
```bash
python main.py login
```
- Browser opens Pinterest login
- Enter credentials
- Complete 2FA if prompted
- Cookies saved automatically

#### Step 2: Copy Pins
```bash
python main.py copy
```
- Loads saved cookies
- Collects pins from source board
- Saves each pin to target board
- Logs results to JSON

#### Alternative: Use Chrome Profile
```bash
python main.py profile
```
Uses existing Chrome profile (set `CHROME_PROFILE_PATH` in `.env`)

## 📋 Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `PINTEREST_EMAIL` | - | Your Pinterest email |
| `PINTEREST_PASSWORD` | - | Your Pinterest password |
| `SOURCE_BOARD_URL` | - | Full URL of source board |
| `TARGET_BOARD_NAME` | - | Name of destination board |
| `CHROME_PROFILE_PATH` | - | Chrome profile directory (optional) |
| `HEADLESS_MODE` | false | Run without browser window |
| `SCROLL_PAUSE_TIME` | 0.8 | Seconds between scrolls |
| `MAX_SCROLLS` | 200 | Maximum scroll iterations |
| `RANDOM_DELAY_MIN` | 2 | Min delay between pins (seconds) |
| `RANDOM_DELAY_MAX` | 5 | Max delay between pins (seconds) |
| `LOG_FAILED_PINS` | true | Save failed pins to JSON |

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
- Increase `MAX_SCROLLS` for large boards
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

| Board Size | Estimated Time |
|-----------|-----------------|
| 1-50 pins | 2-5 minutes |
| 50-200 pins | 10-20 minutes |
| 200-500 pins | 30-60 minutes |
| 500+ pins | 1-2 hours |

*Times vary based on delay settings and board loading speed*

## 🐛 Issues & Support

When reporting issues, include:
- Python version (`python --version`)
- Operating system
- Error message and logs
- Last successful step

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
