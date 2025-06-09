#!/usr/bin/env python3
"""
Simple script to test Telegram bot token validity.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_token():
    """Test if the Telegram bot token is valid"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        print("💡 Make sure you have a .env file with TELEGRAM_BOT_TOKEN=your_token")
        return False
    
    print(f"🔍 Testing token: {token[:10]}...{token[-10:] if len(token) > 20 else token}")
    
    try:
        # Import here to avoid issues if telegram not installed
        from telegram import Bot
        
        bot = Bot(token=token)
        
        # Test the token by getting bot info
        me = await bot.get_me()
        
        print("✅ Token is valid!")
        print(f"🤖 Bot name: {me.first_name}")
        print(f"📛 Bot username: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Token test failed: {e}")
        
        if "401" in str(e) or "Unauthorized" in str(e):
            print("\n💡 This means your bot token is invalid. Here's how to fix it:")
            print("1. Go to @BotFather on Telegram")
            print("2. Send /token")
            print("3. Select your bot")
            print("4. Copy the new token to your .env file")
            print("5. Or create a new bot with /newbot")
        
        return False

def main():
    """Main function"""
    print("🔐 Telegram Bot Token Validator\n")
    
    try:
        result = asyncio.run(test_token())
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())