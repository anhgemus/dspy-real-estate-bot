#!/usr/bin/env python3
"""
Test script for address parsing improvements.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.message_parser import MessageParser
from src.config import setup_dspy

# Setup DSPy for LLM-based parsing
setup_dspy()

def test_address_parsing():
    """Test address parsing with various examples"""
    parser = MessageParser()
    
    test_cases = [
        # Single address cases that should NOT be treated as multiple
        {
            'message': '289A gaffney street, pascoe vale vic 3044',
            'expected_type': 'single',
            'expected_count': 1,
            'description': 'Australian address with "and" in street name'
        },
        {
            'message': 'What is 289A gaffney street, pascoe vale vic 3044 worth?',
            'expected_type': 'single', 
            'expected_count': 1,
            'description': 'Question about single Australian address'
        },
        {
            'message': '123 Woodland Avenue, Portland, OR 97210',
            'expected_type': 'single',
            'expected_count': 1,
            'description': 'US address with "and" in street name'
        },
        
        # Multiple address cases that SHOULD be treated as multiple
        {
            'message': '123 Main St and 456 Oak Ave',
            'expected_type': 'multiple',
            'expected_count': 2,
            'description': 'Two addresses separated by "and"'
        },
        {
            'message': 'Compare 123 Main Street, City, ST 12345 and 456 Oak Avenue, Town, ST 12346',
            'expected_type': 'compare',
            'expected_count': 2,
            'description': 'Comparison of two addresses'
        },
        {
            'message': 'What are both properties worth: 123 Main St and 456 Oak Ave',
            'expected_type': 'multiple',
            'expected_count': 2,
            'description': 'Multiple properties with explicit language'
        },
        
        # Edge cases
        {
            'message': 'Estimate the combined value of two houses',
            'expected_type': 'multiple',
            'expected_count': 0,
            'description': 'Multiple property language but no addresses'
        }
    ]
    
    print("🧪 Testing Address Parsing Improvements\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Input: '{test_case['message']}'")
        
        query = parser.parse_message(test_case['message'])
        
        print(f"Found {len(query.addresses)} address(es):")
        for addr in query.addresses:
            print(f"  - {addr}")
        print(f"Query type: {query.query_type}")
        
        # Check results
        success = True
        if query.query_type != test_case['expected_type']:
            print(f"❌ FAIL: Expected type '{test_case['expected_type']}', got '{query.query_type}'")
            success = False
        
        if len(query.addresses) != test_case['expected_count']:
            print(f"❌ FAIL: Expected {test_case['expected_count']} addresses, got {len(query.addresses)}")
            success = False
        
        if success:
            print("✅ PASS")
        
        print("-" * 60)
    
    print("\n🎯 Key Test: Australian address with 'and' in street name")
    test_query = parser.parse_message("289A gaffney street, pascoe vale vic 3044")
    print(f"Addresses found: {test_query.addresses}")
    print(f"Query type: {test_query.query_type}")
    
    if test_query.query_type == 'single' and len(test_query.addresses) == 1:
        print("✅ SUCCESS: Address parsed correctly as single property")
        return True
    else:
        print("❌ FAILURE: Address not parsed correctly")
        return False

if __name__ == "__main__":
    success = test_address_parsing()
    sys.exit(0 if success else 1)