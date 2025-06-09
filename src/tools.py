"""
Tool functions for DSPy real estate agent.
Contains all specialized search and data gathering tools.
"""

from datetime import datetime
from config import get_search_client

# Initialize search client
search_client = get_search_client()


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
    """Get comprehensive comparable sales data with expanded search for more properties"""
    print(f"🏠 Getting comparable sales for: {address}")
    
    # Extract location components for targeted searches
    location_parts = address.split(',')
    street_area = location_parts[0].strip() if location_parts else address
    suburb_city = location_parts[1].strip() if len(location_parts) > 1 else ""
    state_region = location_parts[2].strip() if len(location_parts) > 2 else ""
    
    # Comprehensive search queries to capture more properties
    queries = [
        # Recent sales - primary searches
        f"{address} recent sales comparable properties",
        f"{address} recently sold homes similar properties",
        f"{address} comps comparable sales nearby",
        f"{address} sold properties last 6 months",
        f"{address} sold properties last 12 months",
        
        # Neighborhood-based searches
        f"homes sold near {address} price per square foot",
        f"{suburb_city} recent home sales similar properties",
        f"{suburb_city} property sales comparable to {street_area}",
        f"properties sold {suburb_city} {state_region} recent",
        f"{suburb_city} area home sales last year",
        
        # Broader geographic searches
        f"similar homes sold {state_region} near {suburb_city}",
        f"{state_region} property sales comparable to {address}",
        f"home sales {suburb_city} {state_region} market data",
        
        # Development and land value searches
        f"{address} land assembly sales multiple lots",
        f"{address} development site sales large lots",
        f"{suburb_city} development property sales",
        f"land value sales {suburb_city} {state_region}",
        
        # Property type specific searches
        f"residential sales near {address} comparable",
        f"house sales {suburb_city} similar to {street_area}",
        f"property transactions {suburb_city} recent sales data"
    ]
    
    all_results = []
    print(f"  🔍 Running {len(queries)} comprehensive searches...")
    
    for i, query in enumerate(queries, 1):
        response = search_client.search(query)
        # Increased from 2 to 4 results per query for more comprehensive data
        results = [r["content"] for r in response["results"][:4]]
        all_results.extend(results)
        
        if i % 5 == 0:  # Progress indicator
            print(f"    ✓ Completed {i}/{len(queries)} searches...")
    
    print(f"  ✅ Collected {len(all_results)} comparable sales data points")
    return "\n".join(all_results)


def get_price_history_analysis(address: str) -> str:
    """Get comprehensive price history and market trends for the property and area"""
    print(f"📈 Analyzing price history and market trends for: {address}")
    
    # Extract location components for targeted searches
    location_parts = address.split(',')
    street_area = location_parts[0].strip() if location_parts else address
    suburb_city = location_parts[1].strip() if len(location_parts) > 1 else ""
    state_region = location_parts[2].strip() if len(location_parts) > 2 else ""
    
    # Comprehensive market intelligence queries
    queries = [
        # Property-specific price history
        f"{address} sale history price changes over time",
        f"{address} property price history previous sales",
        f"{address} historical sale prices trends",
        
        # Area price trends
        f"{suburb_city} {state_region} property price trends last 5 years",
        f"{suburb_city} median house prices historical data",
        f"{suburb_city} property market trends price growth",
        f"{suburb_city} real estate price appreciation rates",
        
        # Market velocity and timing
        f"{suburb_city} average days on market properties",
        f"{suburb_city} how long properties take to sell",
        f"{suburb_city} property sale timeframes market velocity",
        
        # Seasonal trends
        f"{suburb_city} {state_region} seasonal property market trends",
        f"{suburb_city} best time to sell buy property seasonal data",
        f"{suburb_city} property prices by season monthly trends",
        
        # Market predictions and outlook
        f"{suburb_city} {state_region} property market forecast 2024 2025",
        f"{suburb_city} future property price predictions",
        f"{suburb_city} real estate market outlook growth potential",
        
        # Economic indicators
        f"{suburb_city} {state_region} population growth property demand",
        f"{suburb_city} economic growth employment property market",
        f"{suburb_city} infrastructure development property values impact"
    ]
    
    all_results = []
    print(f"  🔍 Running {len(queries)} market intelligence searches...")
    
    for i, query in enumerate(queries, 1):
        response = search_client.search(query)
        results = [r["content"] for r in response["results"][:3]]  # 3 results per query for detailed analysis
        all_results.extend(results)
        
        if i % 4 == 0:  # Progress indicator
            print(f"    ✓ Completed {i}/{len(queries)} market analysis searches...")
    
    print(f"  ✅ Collected {len(all_results)} market intelligence data points")
    return "\n".join(all_results)


def get_market_velocity_analysis(address: str) -> str:
    """Get market velocity data - how quickly properties sell in the area"""
    print(f"⚡ Analyzing market velocity for: {address}")
    
    location_parts = address.split(',')
    suburb_city = location_parts[1].strip() if len(location_parts) > 1 else address
    state_region = location_parts[2].strip() if len(location_parts) > 2 else ""
    
    queries = [
        f"{suburb_city} average days on market 2024",
        f"{suburb_city} properties selling quickly fast sales",
        f"{suburb_city} time to sell property statistics",
        f"{suburb_city} market activity property turnover rates",
        f"{suburb_city} {state_region} buyer demand property competition",
        f"{suburb_city} auction clearance rates success rates",
        f"{suburb_city} properties selling above below asking price",
        f"{suburb_city} hot property market fast selling homes"
    ]
    
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    
    print(f"  ✅ Collected market velocity data")
    return "\n".join(all_results)


def get_market_competition_analysis(address: str) -> str:
    """Analyze current market competition and supply/demand dynamics"""
    print(f"🎯 Analyzing market competition for: {address}")
    
    location_parts = address.split(',')
    suburb_city = location_parts[1].strip() if len(location_parts) > 1 else address
    state_region = location_parts[2].strip() if len(location_parts) > 2 else ""
    
    queries = [
        f"{suburb_city} properties for sale current listings",
        f"{suburb_city} property supply demand analysis",
        f"{suburb_city} how many homes for sale market inventory",
        f"{suburb_city} buyer competition multiple offers",
        f"{suburb_city} property stock levels housing supply",
        f"{suburb_city} {state_region} seller market buyer market conditions",
        f"{suburb_city} property listing price vs sale price analysis",
        f"{suburb_city} market conditions tight supply high demand"
    ]
    
    all_results = []
    for query in queries:
        response = search_client.search(query)
        all_results.extend([r["content"] for r in response["results"][:2]])
    
    print(f"  ✅ Collected market competition data")
    return "\n".join(all_results)