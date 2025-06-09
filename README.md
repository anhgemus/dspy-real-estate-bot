# DSPy Project

A Python project using the DSPy framework for language model programming.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Command Line Interface
Run the main application:
```bash
python src/main.py
```

### Telegram Bot
1. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Telegram bot:
```bash
python run_telegram_bot.py
```

### Telegram Bot Features
- 🏠 Individual property valuations
- 🏘️ Adjacent property combinations with land assembly premiums
- 📊 Neighborhood analysis and market trends
- 🎯 Confidence scoring
- 📱 User-friendly Telegram interface

### Bot Commands
- `/start` - Welcome message
- `/help` - Show available commands
- `/stats` - Bot usage statistics
- `/health` - Check bot status

### Example Usage
Send messages like:
- "What's 123 Main Street, City worth?"
- "Estimate 456 Oak Avenue, Suburb, STATE 1234"
- "Value of 789 Pine St and 791 Pine St together"

## Project Structure

```
├── src/
│   ├── __init__.py
│   └── main.py          # Main application entry point
├── tests/               # Test files
├── requirements.txt     # Project dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## Dependencies

- `dspy` - DSPy framework for language model programming
- `python-dotenv` - Environment variable management

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Submit a pull request