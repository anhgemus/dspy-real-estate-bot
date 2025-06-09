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

Run the main application:
```bash
python src/main.py
```

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