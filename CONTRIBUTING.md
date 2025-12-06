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
git clone https://github.com/yourusername/pinterest-board-automation.git
cd pinterest-board-automation
```

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

```bash
# Clone repository
git clone https://github.com/yourusername/pinterest-board-automation.git
cd pinterest-board-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env with your settings
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
- [ ] Implement retry logic for failed pins
- [ ] Add progress bar UI
- [ ] Support for multiple target boards
- [ ] Add duplicate pin detection

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
