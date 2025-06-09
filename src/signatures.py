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
        3. Research comprehensive comparable sales using expanded search strategy:
           - Start with recent sales (3-6 months) in immediate area
           - If recent sales are limited, expand to 12 months and broader geography
           - Include 10-15 comparable properties for robust analysis
           - Prioritize sales with complete data (price, date, size, features)
        4. Analyze neighborhood factors (schools, crime, amenities, market trends)
        5. Apply market adjustments for unique features and conditions
        6. Calculate price per square foot analysis using multiple data points
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
        desc="10-15 comparable sales with addresses, prices, sale dates, property size, and price/sqft. Include recent sales (3-6 months) first, then expand scope if needed for comprehensive analysis."
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


class MarketIntelligenceSignature(dspy.Signature):
    """You are a market research analyst specializing in real estate market intelligence and trends.
    
    MARKET INTELLIGENCE ANALYSIS:
    1. Get current date/time for temporal context
    2. Analyze property-specific price history and trends
    3. Research area-wide market trends (5+ years of data)
    4. Evaluate market velocity (days on market, sale speed)
    5. Assess seasonal patterns and optimal timing
    6. Examine supply/demand dynamics and competition
    7. Forecast future market conditions and predictions
    8. Identify economic factors affecting property values
    
    ANALYSIS FOCUS AREAS:
    - Historical price appreciation/depreciation rates
    - Market cycle analysis (peak, trough, recovery)
    - Seasonal buying/selling patterns
    - Days on market trends and velocity
    - Supply levels and inventory analysis
    - Buyer competition and bidding patterns
    - Economic indicators and employment impact
    - Infrastructure and development impact on values
    
    CONFIDENCE SCORING:
    - High (0.8-1.0): Rich historical data, clear trends, stable market
    - Medium (0.5-0.7): Some historical data, moderate trends
    - Low (0.2-0.4): Limited data, volatile market, unclear trends
    
    Provide actionable insights for buyers, sellers, and investors.
    """
    
    question: str = dspy.InputField()
    
    price_history: str = dspy.OutputField(
        desc="Property-specific and area price history, appreciation rates, historical trends over 3-5 years"
    )
    
    market_trends: str = dspy.OutputField(
        desc="Current market conditions, price growth trends, market cycle position (peak/trough/recovery)"
    )
    
    market_velocity: str = dspy.OutputField(
        desc="Average days on market, sale timeframes, market activity levels, buyer competition intensity"
    )
    
    seasonal_analysis: str = dspy.OutputField(
        desc="Seasonal market patterns, best times to buy/sell, monthly trends, seasonal price variations"
    )
    
    supply_demand: str = dspy.OutputField(
        desc="Current inventory levels, supply/demand balance, competition analysis, market tightness"
    )
    
    market_predictions: str = dspy.OutputField(
        desc="Future market outlook, price predictions, economic factors, growth potential, risk factors"
    )
    
    investment_insights: str = dspy.OutputField(
        desc="Key insights for buyers/sellers/investors, optimal timing, market positioning, strategic recommendations"
    )
    
    confidence: float = dspy.OutputField(
        desc="Confidence level 0-1 based on data availability, trend clarity, and market stability"
    )