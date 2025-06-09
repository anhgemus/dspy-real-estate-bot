# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

import dspy
import os
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient
from dspy import Tool
from dspy.utils.callback import BaseCallback

# Load environment variables
load_dotenv()

# =============================================================================
# LOGGING AND CALLBACKS
# =============================================================================

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

# =============================================================================
# DSPY SIGNATURE CLASS
# =============================================================================

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

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

# Configure DSPy with callbacks and language model
dspy.configure(callbacks=[AgentLoggingCallback()])
lm = dspy.LM('openai/gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.configure(lm=lm)

# Initialize search client
search_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

# =============================================================================
# TOOL FUNCTIONS
# =============================================================================

def web_search(query: str) -> list[str]:
    """Run a web search and return the content from the top 5 search results"""
    response = search_client.search(query)
    return [r["content"] for r in response["results"]]

def get_current_time() -> str:
    """Get the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_property_tax_data(address: str) -> str:
    """Get property tax assessment data and history for the given address"""
    print(f"🔍 Searching property tax data for: {address}")
    queries = [
        f"{address} property tax assessment",
        f"{address} property tax records",
        f"{address} assessed value tax history"
    ]
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    return "\n".join(all_results)

def get_neighborhood_stats(address: str) -> str:
    """Get neighborhood statistics including median prices and trends"""
    print(f"📊 Getting neighborhood stats for: {address}")
    queries = [
        f"{address} neighborhood median home prices",
        f"{address} area real estate market trends",
        f"{address} housing market statistics"
    ]
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    return "\n".join(all_results)

def get_school_ratings(address: str) -> str:
    """Get school district ratings and test scores for the area"""
    print(f"🏫 Getting school ratings for: {address}")
    queries = [
        f"{address} school district ratings",
        f"{address} elementary middle high school scores",
        f"{address} school quality ratings"
    ]
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    return "\n".join(all_results)

def get_crime_data(address: str) -> str:
    """Get crime statistics for the neighborhood"""
    print(f"🚔 Getting crime data for: {address}")
    queries = [
        f"{address} crime statistics",
        f"{address} neighborhood safety crime rates",
        f"{address} area crime data"
    ]
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    return "\n".join(all_results)

def get_comparable_sales(address: str) -> str:
    """Get recent comparable sales data with multiple search strategies"""
    print(f"🏠 Getting comparable sales for: {address}")
    queries = [
        f"{address} recent sales comparable properties",
        f"{address} recently sold homes similar properties",
        f"{address} comps comparable sales nearby",
        f"{address} sold properties last 6 months",
        f"homes sold near {address} price per square foot",
        f"{address} land assembly sales multiple lots",
        f"{address} development site sales large lots"
    ]
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    return "\n".join(all_results)

# =============================================================================
# AGENT CREATION AND EXECUTION
# =============================================================================

# Create the ReAct agent with all tools
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

# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Example queries (uncomment to test)
    # prediction = agent(question="What is the estimated price of 340 Barneson Avenue San Mateo CA 94402 today?")
    # prediction = agent(question="What is the estimated price of 289A Gaffney Street, Pascoe Vale, VIC 3044 Australia?")
    prediction = agent(question="If I want to sell two houses 289A Gaffney Street, Pascoe Vale, VIC 3044 Australia and 289 Gaffney Street, Pascoe Vale, VIC 3044 Australia, what is the estimated price of the two houses when selling them together?")

    # Display results
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