# 🧪 Tests Directory

This directory contains test files and utility scripts for the DSPy Real Estate Bot.

## 📁 Files

### Test Scripts
- **`test_cache.py`** - Comprehensive tests for the caching system
- **`test_bot_components.py`** - Tests for bot components and functionality

### Utility Scripts  
- **`check_telegram_token.py`** - Utility to validate Telegram bot token
- **`run_telegram_bot.py`** - Direct bot runner script

## 🚀 Running Tests

### Cache Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run cache tests
python tests/test_cache.py
```

### Bot Component Tests
```bash
# Run bot component tests
python tests/test_bot_components.py
```

### Token Validation
```bash
# Check if your Telegram bot token is valid
python tests/check_telegram_token.py
```

## 📝 Notes

- All tests require the virtual environment to be activated
- Cache tests create temporary directories for testing
- Bot tests may require API keys to be configured
- These tests are separate from the main application deployment