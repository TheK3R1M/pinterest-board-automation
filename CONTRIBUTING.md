# Contributing to Pinterest Board Automation

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error logs (if any)

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Explain the use case
- Describe expected behavior
- Consider implementation complexity

### Pull Requests

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/pinterest-board-automation.git
cd pinterest-board-automation
```

*Note: Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username*

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
- Follow existing code style
- Add comments for complex logic
- Test thoroughly

4. **Commit with clear messages**
```bash
git commit -m "Add feature: description"
```

5. **Push and create PR**
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title and description
- Reference related issues
- Screenshots (if UI changes)

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Google Chrome
- Text editor or IDE (VS Code recommended)

### Step-by-Step Setup

**1. Clone repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/pinterest-board-automation.git
cd pinterest-board-automation
```

*Note: Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username*

**2. Create virtual environment**

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

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
notepad .env  # Edit with Notepad or VS Code
```

**Linux/macOS:**
```bash
cp .env.example .env
nano .env  # Or use your preferred editor
```

Required variables:
```env
PINTEREST_EMAIL=your.email@example.com
PINTEREST_PASSWORD=your_password
SOURCE_BOARD_URL=https://www.pinterest.com/username/source-board/
TARGET_BOARD_NAME=Target Board Name
```

**5. Test the setup**

```bash
# Test login (creates cookies)
python main.py login

# Test copying pins
python main.py copy
```

### Project Structure
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
├── README.md              # User documentation
├── CONTRIBUTING.md        # This file
└── logs/                  # Auto-generated logs
```

### Running the Code

**Full workflow:**
```bash
# 1. Login (one-time or when cookies expire)
python main.py login

# 2. Copy pins
python main.py copy

# 3. Check results
# - View logs/ folder for success_pins_*.json and failed_pins_*.json
# - Check your Pinterest account for copied pins
```

**For troubleshooting:**
```bash
# Run with headless disabled to see browser
# Edit .env and set: HEADLESS_MODE=false
python main.py copy
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## Testing

Before submitting PR:
- Test with small boards (10-20 pins)
- Test with large boards (100+ pins)
- Test both cookie and profile modes
- Verify error handling works
- Check log files are generated correctly

## Areas for Contribution

### High Priority
- [ ] Add support for private boards
- [x] ~~Implement retry logic for failed pins~~ ✅ DONE (v2.0)
- [x] ~~Add progress bar UI~~ ✅ DONE (v2.0)
- [ ] Support for multiple target boards
- [x] ~~Add duplicate pin detection~~ ✅ DONE (v2.0)

### Medium Priority
- [ ] Add configuration via CLI arguments
- [ ] Implement rate limiting options
- [ ] Support for Pinterest collections
- [ ] Add board merge functionality
- [ ] Export board data to CSV

### Low Priority
- [ ] GUI interface (Tkinter/PyQt)
- [ ] Docker support
- [ ] Scheduled automation (cron)
- [ ] Pinterest API integration (if available)
- [ ] Browser extension version

## Questions?

Feel free to open an issue for:
- Questions about the code
- Implementation discussions
- Architecture decisions
- Feature proposals

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on collaboration

Thank you for contributing! 🚀
