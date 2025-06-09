"""
Agent creation and management for DSPy real estate agent.
Contains functions to create and configure the ReAct agent with all tools.
"""

import dspy
from dspy import Tool

from .signatures import DSPyRealEstateAgent
from .tools import (
    web_search,
    get_current_time,
    get_property_tax_data,
    get_neighborhood_stats,
    get_school_ratings,
    get_crime_data,
    get_comparable_sales
)


def create_real_estate_agent():
    """Create and return a configured ReAct agent for real estate valuation"""
    agent = dspy.ReAct(
        DSPyRealEstateAgent,
        tools=[
            Tool(web_search),
            Tool(get_current_time),
            Tool(get_property_tax_data),
            Tool(get_neighborhood_stats),
            Tool(get_school_ratings),
            Tool(get_crime_data),
            Tool(get_comparable_sales)
        ],
    )
    return agent


def display_results(prediction):
    """Display formatted results from the agent prediction"""
    print("\n" + "="*50)
    print("           PROPERTY VALUATION RESULTS")
    print("="*50)
    print("\n=== PROPERTY DETAILS ===")
    print(prediction.property_details)
    print("\n=== COMPARABLE SALES ===")
    print(prediction.comparable_sales)
    print("\n=== NEIGHBORHOOD ANALYSIS ===")
    print(prediction.neighborhood_analysis)
    print("\n=== MARKET ADJUSTMENTS ===")
    print(prediction.market_adjustments)
    print("\n=== PRICE ANALYSIS ===")
    print(prediction.price_analysis)
    print("\n=== PRICE RANGE ===")
    print(prediction.price_range)
    print("\n=== FINAL ESTIMATE ===")
    print(prediction.final_estimate)
    print(f"\n=== CONFIDENCE: {prediction.confidence} ===")