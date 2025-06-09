#!/usr/bin/env python3
"""
Entry point to run the Telegram bot for real estate valuations.
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.telegram_bot import main


if __name__ == "__main__":
    print("🏠 Starting Real Estate Valuation Telegram Bot...")
    print("Press Ctrl+C to stop the bot")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)