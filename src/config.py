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