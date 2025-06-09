"""
Market intelligence agent for deep property market research.
Provides comprehensive market analysis, trends, and predictions.
"""

import dspy
from signatures import MarketIntelligenceSignature
from tools import (
    get_current_time, get_price_history_analysis, 
    get_market_velocity_analysis, get_market_competition_analysis,
    get_neighborhood_stats
)


def create_market_intelligence_agent():
    """Create and configure the market intelligence agent with tools"""
    
    # Define the agent with market intelligence tools
    agent = dspy.ReAct(
        signature=MarketIntelligenceSignature,
        tools=[
            get_current_time,
            get_price_history_analysis,
            get_market_velocity_analysis, 
            get_market_competition_analysis,
            get_neighborhood_stats
        ],
        max_iters=8  # Allow more iterations for comprehensive analysis
    )
    
    return agent


def display_market_intelligence_results(prediction) -> str:
    """Format and display market intelligence analysis results"""
    
    print("\n" + "="*80)
    print("📊 MARKET INTELLIGENCE ANALYSIS REPORT")
    print("="*80)
    
    print(f"\n📈 PRICE HISTORY & TRENDS:")
    print("-" * 40)
    print(prediction.price_history)
    
    print(f"\n📊 CURRENT MARKET CONDITIONS:")
    print("-" * 40)
    print(prediction.market_trends)
    
    print(f"\n⚡ MARKET VELOCITY:")
    print("-" * 40)
    print(prediction.market_velocity)
    
    print(f"\n🌟 SEASONAL ANALYSIS:")
    print("-" * 40)
    print(prediction.seasonal_analysis)
    
    print(f"\n⚖️ SUPPLY & DEMAND:")
    print("-" * 40)
    print(prediction.supply_demand)
    
    print(f"\n🔮 MARKET PREDICTIONS:")
    print("-" * 40)
    print(prediction.market_predictions)
    
    print(f"\n💡 INVESTMENT INSIGHTS:")
    print("-" * 40)
    print(prediction.investment_insights)
    
    print(f"\n🎯 CONFIDENCE LEVEL: {prediction.confidence:.1%}")
    
    print("\n" + "="*80)
    
    return "Market intelligence analysis completed successfully!"


def run_market_analysis_example():
    """Example function to test market intelligence agent"""
    from config import setup_dspy
    
    # Setup DSPy
    setup_dspy()
    
    # Create agent
    agent = create_market_intelligence_agent()
    
    # Test with example address
    test_address = "289A Gaffney Street, Pascoe Vale, VIC 3044"
    question = f"Provide comprehensive market intelligence analysis for {test_address}"
    
    print(f"🔍 Running market intelligence analysis for: {test_address}")
    
    # Get prediction
    prediction = agent(question=question)
    
    # Display results
    display_market_intelligence_results(prediction)
    
    return prediction


if __name__ == "__main__":
    run_market_analysis_example()