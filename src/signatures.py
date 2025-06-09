"""
DSPy signature classes for real estate agent.
Contains the main signature class that defines the agent's behavior and output structure.
"""

import dspy


class DSPyRealEstateAgent(dspy.Signature):
    """You are a real estate agent that helps estimate property values with high accuracy.

        ANALYSIS PROCESS:
        1. Get current date/time to check recent sales timing
        2. Gather property characteristics (size, bed/bath, lot, age, condition, type)
        3. Research comparable sales (3-5 recent sales within 0.5 miles)
        4. Analyze neighborhood factors (schools, crime, amenities, market trends)
        5. Apply market adjustments for unique features and conditions
        6. Calculate price per square foot analysis
        7. Provide price range and final estimate with confidence scoring

        SPECIAL CONSIDERATION FOR MULTIPLE ADJACENT PROPERTIES:
        When valuing multiple adjacent properties sold together, consider:
        - Land assembly premium (10-30% bonus for larger combined lot)
        - Development potential and zoning opportunities
        - Demolition cost savings vs separate sales
        - Market demand for larger plots in the area
        - Compare to recent sales of similar-sized combined lots
        - Factor in buyer pool differences (developers vs individual buyers)

        CONFIDENCE SCORING:
        - High (0.8-1.0): Recent comps, good data quality, stable market
        - Medium (0.5-0.7): Some recent comps, moderate data, normal market
        - Low (0.2-0.4): Few comps, limited data, volatile market

        Use multiple search strategies and comprehensive analysis for accurate estimates.
    """

    question: str = dspy.InputField()
    
    property_details: str = dspy.OutputField(
        desc="Property characteristics found: size, bed/bath, lot size, age, type, condition"
    )
    
    comparable_sales: str = dspy.OutputField(
        desc="3-5 recent comparable sales with addresses, prices, dates, size, and price/sqft"
    )
    
    neighborhood_analysis: str = dspy.OutputField(
        desc="School ratings, crime data, market trends, and area median prices"
    )
    
    market_adjustments: str = dspy.OutputField(
        desc="Adjustments for condition, unique features, lot premium/discount, market timing, land assembly premium if multiple properties"
    )
    
    price_analysis: str = dspy.OutputField(
        desc="Price per square foot comparison and calculation methodology"
    )
    
    price_range: str = dspy.OutputField(
        desc="Estimated price range (min-max) accounting for uncertainty"
    )
    
    final_estimate: str = dspy.OutputField(
        desc="Single best estimate with detailed reasoning in bullet points"
    )
    
    confidence: float = dspy.OutputField(
        desc="Confidence level 0-1 based on data quality, comparables, and market conditions"
    )