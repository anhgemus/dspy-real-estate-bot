"""
Main entry point for DSPy real estate property valuation agent.
"""

from config import setup_dspy
from agent import create_real_estate_agent, display_results


def main():
    """Main function to run the real estate valuation agent"""
    # Setup DSPy configuration
    setup_dspy()
    
    # Create the agent
    agent = create_real_estate_agent()
    
    # Example queries (uncomment to test different scenarios)
    # prediction = agent(question="What is the estimated price of 340 Barneson Avenue San Mateo CA 94402 today?")
    # prediction = agent(question="What is the estimated price of 289A Gaffney Street, Pascoe Vale, VIC 3044 Australia?")
    prediction = agent(question="If I want to sell two houses 289A Gaffney Street, Pascoe Vale, VIC 3044 Australia and 289 Gaffney Street, Pascoe Vale, VIC 3044 Australia, what is the estimated price of the two houses when selling them together?")
    
    # Display formatted results
    display_results(prediction)


if __name__ == "__main__":
    main()