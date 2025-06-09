"""
Telegram bot for real estate property valuation.
Integrates with DSPy real estate agent to provide property estimates.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional

from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction

from config import get_telegram_config
from message_parser import MessageParser, PropertyQuery
from response_formatter import ResponseFormatter
from async_agent import AsyncRealEstateAgent


# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class RealEstateBot:
    """Telegram bot for real estate valuations"""
    
    def __init__(self):
        self.config = get_telegram_config()
        self.parser = MessageParser()
        self.formatter = ResponseFormatter()
        self.agent = AsyncRealEstateAgent()
        self.app: Optional[Application] = None
        
        # Statistics
        self.requests_processed = 0
        self.start_time = datetime.now()
    
    async def initialize(self):
        """Initialize the bot and agent"""
        if not self.config['token']:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Initialize the agent
        await self.agent.initialize()
        
        # Create application
        self.app = Application.builder().token(self.config['token']).build()
        
        # Add handlers
        await self._setup_handlers()
        
        logger.info("Bot initialized successfully")
    
    async def _setup_handlers(self):
        """Setup command and message handlers"""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("health", self.health_command))
        self.app.add_handler(CommandHandler("cache", self.cache_command))
        self.app.add_handler(CommandHandler("clearcache", self.clear_cache_command))
        
        # Message handler for property queries
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_message
        ))
        
        # Set bot commands
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help message"),
            BotCommand("stats", "Show bot statistics"),
            BotCommand("health", "Check bot health"),
            BotCommand("cache", "Show cache information"),
            BotCommand("clearcache", "Clear all cached data"),
        ]
        await self.app.bot.set_my_commands(commands)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """🏠 *Welcome to Real Estate Valuation Bot!*

I can help you estimate property values using advanced AI analysis.

*How to use:*
Just send me an address like:
• "What's 123 Main Street, City worth?"
• "Estimate 456 Oak Avenue, Suburb, STATE 1234"

*Features:*
✅ Individual property valuations
✅ Adjacent property combinations  
✅ Neighborhood analysis
✅ Confidence scoring

Type /help for more information!"""

        await update.message.reply_text(
            welcome_message,
            parse_mode="Markdown"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_response = self.formatter.format_help_message()
        await update.message.reply_text(
            help_response.text,
            parse_mode=help_response.parse_mode
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        agent_healthy = await self.agent.health_check()
        cache_stats = self.agent.get_cache_stats()
        
        stats_message = f"""📊 *Bot Statistics*

⏰ *Uptime:* {uptime_str}
📈 *Requests Processed:* {self.requests_processed}
🔧 *Agent Status:* {'✅ Healthy' if agent_healthy else '❌ Unhealthy'}

💾 *Cache Performance:*"""

        if cache_stats.get('cache_enabled', False):
            cache_info = cache_stats.get('statistics', {})
            stats_message += f"""
• Hit Rate: {cache_info.get('hit_rate', 0):.1%}
• Total Requests: {cache_info.get('total_requests', 0)}
• Memory Cache: {cache_stats['memory_cache']['size']}/{cache_stats['memory_cache']['max_size']}
• Disk Cache: {cache_stats['disk_cache']['size']} files ({cache_stats['disk_cache']['size_mb']} MB)"""
        else:
            stats_message += "\n• Cache: Disabled"

        stats_message += f"\n\n🕒 *Last Updated:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        await update.message.reply_text(
            stats_message,
            parse_mode="Markdown"
        )
    
    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /health command"""
        agent_healthy = await self.agent.health_check()
        
        if agent_healthy:
            await update.message.reply_text("✅ Bot is healthy and ready!")
        else:
            await update.message.reply_text("❌ Bot is experiencing issues. Please try again later.")
    
    async def cache_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /cache command"""
        cache_stats = self.agent.get_cache_stats()
        
        if not cache_stats.get('cache_enabled', False):
            await update.message.reply_text("💾 Cache is currently disabled.")
            return
        
        cache_info = cache_stats.get('statistics', {})
        memory_cache = cache_stats.get('memory_cache', {})
        disk_cache = cache_stats.get('disk_cache', {})
        
        cache_message = f"""💾 *Cache Information*

📊 *Performance:*
• Hit Rate: {cache_info.get('hit_rate', 0):.1%}
• Total Requests: {cache_info.get('total_requests', 0)}
• Cache Hits: {cache_info.get('hits', 0)}
• Cache Misses: {cache_info.get('misses', 0)}

🧠 *Memory Cache:*
• Entries: {memory_cache.get('size', 0)}/{memory_cache.get('max_size', 0)}
• TTL: {memory_cache.get('ttl_hours', 0)} hours

💿 *Disk Cache:*
• Files: {disk_cache.get('size', 0)}
• Size: {disk_cache.get('size_mb', 0)} MB
• TTL: {disk_cache.get('ttl_days', 0)} days

⏱️ *Uptime:* {cache_info.get('uptime', 'Unknown')}"""

        await update.message.reply_text(
            cache_message,
            parse_mode="Markdown"
        )
    
    async def clear_cache_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clearcache command"""
        result = self.agent.clear_cache()
        
        if result.get('cleared', False):
            message = f"""🗑️ *Cache Cleared*

Removed:
• Memory entries: {result.get('memory_entries', 0)}
• Disk files: {result.get('disk_entries', 0)}

Cache has been completely cleared."""
        else:
            message = f"❌ Cache clear failed: {result.get('reason', 'Unknown error')}"
        
        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages"""
        try:
            # Check if user is allowed (if restrictions are set)
            if self.config['allowed_users'] and str(update.effective_user.id) not in self.config['allowed_users']:
                await update.message.reply_text(
                    "❌ Sorry, you're not authorized to use this bot."
                )
                return
            
            message_text = update.message.text
            logger.info(f"Processing message from {update.effective_user.username}: {message_text[:50]}...")
            
            # Parse the message
            query = self.parser.parse_message(message_text)
            
            # Validate addresses
            if not query.addresses:
                await update.message.reply_text(
                    "❌ I couldn't find any valid addresses in your message.\n\n"
                    "Please include a full address like:\n"
                    "• 123 Main Street, City, STATE 1234\n"
                    "• 456 Oak Avenue, Suburb\n\n"
                    "Type /help for more examples."
                )
                return
            
            valid_addresses, invalid_addresses = self.parser.validate_addresses(query.addresses)
            
            if not valid_addresses:
                await update.message.reply_text(
                    "❌ The addresses you provided don't appear to be valid.\n\n"
                    "Please check the format and try again.\n"
                    "Type /help for examples."
                )
                return
            
            # Update query with only valid addresses
            query.addresses = valid_addresses
            
            # Send processing message
            processing_response = self.formatter.format_processing_message(valid_addresses)
            processing_message = await update.message.reply_text(
                processing_response.text,
                parse_mode=processing_response.parse_mode
            )
            
            # Show typing indicator
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING
            )
            
            # Process the request
            await self._process_property_request(update, query, processing_message)
            
            # Update statistics
            self.requests_processed += 1
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            error_response = self.formatter._format_error_response(str(e))
            await update.message.reply_text(
                error_response.text,
                parse_mode=error_response.parse_mode
            )
    
    async def _process_property_request(self, update: Update, query: PropertyQuery, processing_message):
        """Process the property valuation request"""
        try:
            # Get the analysis from the agent
            prediction = await self.agent.analyze_property(query)
            
            # Format the response
            if query.query_type == "multiple":
                response = self.formatter.format_multiple_properties(prediction)
            else:
                response = self.formatter.format_property_valuation(prediction)
            
            # Delete processing message and send results
            await processing_message.delete()
            await update.message.reply_text(
                response.text,
                parse_mode=response.parse_mode
            )
            
            logger.info(f"Successfully processed request for {len(query.addresses)} properties")
            
        except Exception as e:
            logger.error(f"Error processing property request: {e}")
            
            # Delete processing message
            try:
                await processing_message.delete()
            except:
                pass
            
            # Send error response
            error_response = self.formatter._format_error_response(str(e))
            await update.message.reply_text(
                error_response.text,
                parse_mode=error_response.parse_mode
            )
    
    async def start_polling(self):
        """Start the bot with polling"""
        if not self.app:
            await self.initialize()
        
        logger.info("Starting bot with polling...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        try:
            # Keep the bot running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            await self.stop()
    
    async def start_webhook(self, webhook_url: str, port: int = 8080):
        """Start the bot with webhook"""
        if not self.app:
            await self.initialize()
        
        logger.info(f"Starting bot with webhook: {webhook_url} on port {port}")
        await self.app.initialize()
        await self.app.start()
        
        # Set webhook URL with Telegram
        await self.app.bot.set_webhook(webhook_url)
        logger.info(f"Webhook set successfully: {webhook_url}")
        
        # Start webhook server
        await self.app.updater.start_webhook(
            listen="0.0.0.0",
            port=int(port),
            webhook_url=webhook_url,
            url_path="/webhook"
        )
        
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the bot and cleanup resources"""
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
        
        self.agent.cleanup()
        logger.info("Bot stopped")


async def main():
    """Main function to run the bot"""
    bot = RealEstateBot()
    
    # Check if webhook configuration is provided
    webhook_url = bot.config.get('webhook_url')
    
    if webhook_url:
        # Run with webhook
        webhook_port = bot.config.get('webhook_port', 8443)
        await bot.start_webhook(webhook_url, webhook_port)
    else:
        # Run with polling
        await bot.start_polling()


if __name__ == "__main__":
    asyncio.run(main())