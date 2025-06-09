"""
Tool functions for DSPy real estate agent.
Contains all specialized search and data gathering tools.
"""

from datetime import datetime
from .config import get_search_client

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