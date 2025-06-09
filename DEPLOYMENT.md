# 🚀 Railway.app Deployment Guide

Deploy your Telegram real estate bot to Railway.app's free tier for **$0/month**.

## 📋 Prerequisites

1. **GitHub Account** (to connect your repository)
2. **Railway Account** (sign up at [railway.app](https://railway.app))
3. **API Keys Ready**:
   - OpenAI API Key
   - Tavily API Key  
   - Telegram Bot Token

## 🛠️ Step 1: Prepare Your Repository

Your repository is already configured with:
- ✅ `Dockerfile` for containerization
- ✅ `railway.json` for Railway configuration  
- ✅ `requirements.txt` with dependencies
- ✅ Production-ready webhook handling

### Push to GitHub (if not already done):
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

## 🚀 Step 2: Deploy to Railway

### 2.1 Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `dspy` (or whatever you named it)

### 2.2 Configure Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Optional - Cache Settings
ENABLE_CACHE=true
CACHE_MEMORY_MAX_ITEMS=100
CACHE_MEMORY_TTL_HOURS=24
CACHE_DISK_DIR=cache
CACHE_DISK_TTL_DAYS=7
CACHE_ENABLE_DISK=true

# Optional - User Access Control
TELEGRAM_ALLOWED_USERS=your_user_id_1,your_user_id_2
```

### 2.3 Deploy
1. Railway will **automatically deploy** after adding environment variables
2. Wait for deployment to complete (usually 2-3 minutes)
3. You'll get a URL like: `https://your-app-name.railway.app`

## ✅ Step 3: Verify Deployment

### 3.1 Check Logs
- In Railway dashboard, go to **"Deployments"** → **"View Logs"**
- Look for: `"Bot initialized successfully"` and `"Webhook set successfully"`

### 3.2 Test Your Bot
1. Open Telegram
2. Message your bot: `/start`
3. Try a property query: `"What's 123 Main Street worth?"`

## 💰 Free Tier Limits

Railway Free Tier includes:
- ✅ **500 execution hours/month** (~16 hours/day)
- ✅ **1GB RAM** (sufficient for your bot)
- ✅ **Automatic HTTPS** (required for webhooks)
- ✅ **Custom domains** (optional)

## 🔧 Troubleshooting

### Bot Not Responding?
1. **Check logs** in Railway dashboard
2. **Verify environment variables** are set correctly
3. **Test bot token**: Message @BotFather on Telegram

### Webhook Issues?
```bash
# Check webhook status via Bot API
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

### Cache Issues?
- Cache directory is automatically created
- Disk cache disabled if no write permissions

## 📊 Monitoring Usage

### Railway Dashboard:
- **Usage** tab shows execution hours
- **Metrics** tab shows CPU/RAM usage
- **Logs** tab for debugging

### Bot Commands:
- `/stats` - Bot statistics and cache performance
- `/health` - Check if bot is healthy
- `/cache` - View cache information

## 🚀 Going Production

When you outgrow the free tier:
1. **Railway Pro**: $5/month for unlimited hours
2. **Custom domain**: Point your domain to Railway
3. **Environment separation**: Create separate staging/production deployments

## 🔐 Security Best Practices

- ✅ Environment variables stored securely in Railway
- ✅ No secrets in code/repository
- ✅ HTTPS enforced for webhooks
- ✅ Optional user access control via `TELEGRAM_ALLOWED_USERS`

---

**🎉 Your bot is now live 24/7 for FREE!**

Need help? Check Railway's [documentation](https://docs.railway.app) or reach out for support.