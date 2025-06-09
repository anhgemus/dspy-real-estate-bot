"""
Configuration module for DSPy real estate agent.
Handles environment variables, API clients, and DSPy setup.
"""

import os
import dspy
from dotenv import load_dotenv
from tavily import TavilyClient
from dspy.utils.callback import BaseCallback

# Load environment variables
load_dotenv()


class AgentLoggingCallback(BaseCallback):
    """Custom callback class for logging DSPy agent reasoning and actions"""
    
    def on_module_end(self, call_id, outputs, exception):
        step = "Reasoning" if self._is_reasoning_output(outputs) else "Acting"
        print(f"== {step} Step ===")
        for k, v in outputs.items():
            print(f"  {k}: {v}")
        print("\n")

    def _is_reasoning_output(self, outputs):
        return any(k.startswith("Thought") for k in outputs.keys())


def setup_dspy():
    """Configure DSPy with callbacks and language model"""
    dspy.configure(callbacks=[AgentLoggingCallback()])
    lm = dspy.LM('openai/gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
    dspy.configure(lm=lm)


def get_search_client():
    """Initialize and return Tavily search client"""
    return TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))


def get_telegram_config():
    """Get Telegram bot configuration"""
    return {
        'token': os.getenv('TELEGRAM_BOT_TOKEN'),
        'webhook_url': os.getenv('TELEGRAM_WEBHOOK_URL'),
        'webhook_port': int(os.getenv('TELEGRAM_WEBHOOK_PORT', '8443')),
        'allowed_users': os.getenv('TELEGRAM_ALLOWED_USERS', '').split(',') if os.getenv('TELEGRAM_ALLOWED_USERS') else []
    }


def get_cache_config():
    """Get cache configuration"""
    return {
        'enable_cache': os.getenv('ENABLE_CACHE', 'true').lower() == 'true',
        'memory_max_items': int(os.getenv('CACHE_MEMORY_MAX_ITEMS', '100')),
        'memory_ttl_hours': int(os.getenv('CACHE_MEMORY_TTL_HOURS', '24')),
        'disk_cache_dir': os.getenv('CACHE_DISK_DIR', 'cache'),
        'disk_ttl_days': int(os.getenv('CACHE_DISK_TTL_DAYS', '7')),
        'enable_disk_cache': os.getenv('CACHE_ENABLE_DISK', 'true').lower() == 'true'
    }