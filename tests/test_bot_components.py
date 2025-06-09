#!/usr/bin/env python3
"""
Test script for Telegram bot components without requiring API keys.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.message_parser import MessageParser
from src.response_formatter import ResponseFormatter

def test_message_parser():
    """Test message parsing functionality"""
    print("🧪 Testing Message Parser...")
    
    parser = MessageParser()
    
    test_cases = [
        "What's 123 Main Street, New York, NY 10001 worth?",
        "Estimate 456 Oak Avenue, Los Angeles, CA 90210",
        "Value of 789 Pine St and 791 Pine St together",
        "Compare 123 First St vs 125 First St",
        "289 Gaffney Street, Pascoe Vale, VIC 3044 Australia",
    ]
    
    for message in test_cases:
        query = parser.parse_message(message)
        print(f"📝 '{message[:40]}...'")
        print(f"   → Addresses: {query.addresses}")
        print(f"   → Type: {query.query_type}")
        print()

def test_response_formatter():
    """Test response formatting functionality"""
    print("🎨 Testing Response Formatter...")
    
    formatter = ResponseFormatter()
    
    # Test help message
    help_msg = formatter.format_help_message()
    print("📋 Help Message Preview:")
    print(help_msg.text[:200] + "...")
    print()
    
    # Test quick estimate
    quick_est = formatter.format_quick_estimate(
        "123 Main St, City", 
        "$850,000", 
        0.85
    )
    print("⚡ Quick Estimate Preview:")
    print(quick_est.text)
    print()
    
    # Test processing message
    processing = formatter.format_processing_message(["123 Main St", "125 Main St"])
    print("⏳ Processing Message Preview:")
    print(processing.text)

def main():
    """Run all component tests"""
    print("🚀 Testing Telegram Bot Components\n")
    
    try:
        test_message_parser()
        test_response_formatter()
        print("✅ All component tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())