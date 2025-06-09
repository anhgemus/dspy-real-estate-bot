# Telegram Bot Setup Guide

## 🤖 Getting Your Telegram Bot Token

1. **Start a chat with BotFather** on Telegram: [@BotFather](https://t.me/BotFather)

2. **Create a new bot:**
   ```
   /newbot
   ```

3. **Choose a name** for your bot (e.g., "My Real Estate Agent")

4. **Choose a username** for your bot (must end in 'bot', e.g., "my_real_estate_agent_bot")

5. **Copy the token** BotFather gives you (looks like: `123456789:ABCdef-ghijklmnop`)

## 🔧 Environment Setup

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file** and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   TELEGRAM_BOT_TOKEN=123456789:ABCdef-ghijklmnop
   ```

3. **Optional: Set user restrictions** (comma-separated Telegram user IDs):
   ```env
   TELEGRAM_ALLOWED_USERS=12345678,87654321
   ```

## 🚀 Running the Bot

1. **Install dependencies:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Test components** (no API keys needed):
   ```bash
   python test_bot_components.py
   ```

3. **Start the bot:**
   ```bash
   python run_telegram_bot.py
   ```

## 💬 Using Your Bot

1. **Find your bot** on Telegram using the username you chose
2. **Start a conversation:** `/start`
3. **Get help:** `/help`
4. **Send property queries:**
   - "What's 123 Main Street worth?"
   - "Estimate 456 Oak Ave, City, STATE 12345"
   - "Value of 789 Pine St and 791 Pine St together"

## 🛠️ Bot Commands

- `/start` - Welcome message
- `/help` - Usage instructions
- `/stats` - Bot statistics
- `/health` - Check bot status

## 🔒 Security Notes

- Keep your bot token secret
- Use `TELEGRAM_ALLOWED_USERS` to restrict access
- The bot processes property addresses only - no personal data is stored

## 🐛 Troubleshooting

**Bot not responding:**
- Check your `TELEGRAM_BOT_TOKEN` is correct
- Ensure your API keys are valid
- Check the console for error messages

**"Address not found" errors:**
- Use full addresses with city/state/postal code
- Try different address formats
- Check spelling and formatting

**Analysis taking too long:**
- Property analysis can take 30-90 seconds
- Complex queries (multiple properties) take longer
- The bot will show progress indicators

## 📈 Production Deployment

For production use, consider:
- Using webhooks instead of polling
- Setting up proper logging
- Adding rate limiting
- Using a process manager (PM2, systemd)
- Setting up monitoring and alerts