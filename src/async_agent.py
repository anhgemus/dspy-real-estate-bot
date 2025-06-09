"""
Async wrapper for DSPy real estate agent.
Provides async interface for use with Telegram bot.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional
from config import setup_dspy
from agent import create_real_estate_agent
from message_parser import PropertyQuery


class AsyncRealEstateAgent:
    """Async wrapper for the DSPy real estate agent"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.agent = None
        self._setup_complete = False
    
    async def initialize(self):
        """Initialize the agent asynchronously"""
        if not self._setup_complete:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._sync_setup)
            self._setup_complete = True
    
    def _sync_setup(self):
        """Synchronous setup method"""
        setup_dspy()
        self.agent = create_real_estate_agent()
    
    async def analyze_property(self, query: PropertyQuery) -> Any:
        """Analyze property valuation asynchronously"""
        if not self._setup_complete:
            await self.initialize()
        
        # Prepare the question based on query type
        question = self._build_question(query)
        
        # Run the agent in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        prediction = await loop.run_in_executor(
            self.executor, 
            self._run_agent_sync, 
            question
        )
        
        return prediction
    
    def _run_agent_sync(self, question: str) -> Any:
        """Run the agent synchronously"""
        return self.agent(question=question)
    
    def _build_question(self, query: PropertyQuery) -> str:
        """Build the appropriate question based on query type"""
        if query.query_type == "multiple" and len(query.addresses) == 2:
            # Adjacent properties
            return (f"If I want to sell two houses {query.addresses[0]} and "
                   f"{query.addresses[1]}, what is the estimated price of the "
                   f"two houses when selling them together?")
        
        elif query.query_type == "compare" and len(query.addresses) >= 2:
            # Comparison
            return (f"Compare the estimated values of {query.addresses[0]} "
                   f"and {query.addresses[1]}. What are their individual values "
                   f"and how do they differ?")
        
        elif len(query.addresses) >= 1:
            # Single property
            return f"What is the estimated price of {query.addresses[0]} today?"
        
        else:
            return "I need a valid property address to provide an estimate."
    
    async def get_quick_estimate(self, address: str) -> dict:
        """Get a quick estimate for a single property"""
        try:
            if not self._setup_complete:
                await self.initialize()
            
            question = f"What is the estimated price of {address} today?"
            
            loop = asyncio.get_event_loop()
            prediction = await loop.run_in_executor(
                self.executor,
                self._run_agent_sync,
                question
            )
            
            # Extract key information for quick response
            return {
                "address": address,
                "estimate": prediction.final_estimate.split('\n')[0] if hasattr(prediction, 'final_estimate') else "Estimate unavailable",
                "confidence": prediction.confidence if hasattr(prediction, 'confidence') else 0.5,
                "success": True
            }
            
        except Exception as e:
            return {
                "address": address,
                "estimate": "Analysis failed",
                "confidence": 0.0,
                "success": False,
                "error": str(e)
            }
    
    async def health_check(self) -> bool:
        """Check if the agent is healthy and responding"""
        try:
            if not self._setup_complete:
                await self.initialize()
            return self.agent is not None
        except Exception:
            return False
    
    def cleanup(self):
        """Cleanup resources"""
        self.executor.shutdown(wait=False)