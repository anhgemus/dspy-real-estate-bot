#!/usr/bin/env python3
"""
Entry point for running the Telegram bot.
Handles both development (polling) and production (webhook) modes.
"""

import os
import asyncio
import logging
from telegram_bot import main

# Configure logging for production
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Check if we're running in production (Railway sets PORT environment variable)
    port = os.getenv('PORT')
    if port:
        logger.info(f"Production mode detected (PORT={port})")
        # Set webhook URL based on Railway's domain
        railway_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN')
        if railway_domain:
            webhook_url = f"https://{railway_domain}/webhook"
            os.environ['TELEGRAM_WEBHOOK_URL'] = webhook_url
            os.environ['TELEGRAM_WEBHOOK_PORT'] = port
            logger.info(f"Setting webhook URL to: {webhook_url}")
    else:
        logger.info("Development mode detected (using polling)")
    
    # Run the bot
    asyncio.run(main())