"""
Message parsing utilities for Telegram bot.
Extracts addresses and property queries from user messages using LLM.
"""

import re
import json
import dspy
from typing import List, Optional, Tuple
from pydantic import BaseModel


class PropertyQuery(BaseModel):
    """Structured property query from user message"""
    addresses: List[str]
    query_type: str  # 'single', 'multiple', 'compare'
    raw_message: str


class AddressParsingSignature(dspy.Signature):
    """Parse user message to extract property addresses and determine query type."""
    
    user_message = dspy.InputField(desc="User's message about property valuation")
    addresses = dspy.OutputField(desc="List of complete property addresses found in the message, as JSON array of strings. Include full address with street, suburb/city, state/region, and postcode/zipcode when available.")
    query_type = dspy.OutputField(desc="Type of query: 'single' for one property, 'multiple' for multiple properties being combined/sold together, 'compare' for comparing different properties")
    confidence = dspy.OutputField(desc="Confidence score (0.0-1.0) in the parsing accuracy")


class MessageParser:
    """LLM-powered parser for extracting property information from user messages"""
    
    def __init__(self):
        self.address_parser = dspy.Predict(AddressParsingSignature)
    
    def parse_message(self, message: str) -> PropertyQuery:
        """Parse user message and extract property query information using LLM"""
        try:
            # Use LLM to parse the message
            result = self.address_parser(user_message=message)
            
            # Parse the addresses JSON
            try:
                addresses = json.loads(result.addresses)
                if not isinstance(addresses, list):
                    addresses = [str(addresses)] if addresses else []
            except (json.JSONDecodeError, TypeError):
                # Fallback: treat as single address if JSON parsing fails
                addresses = [result.addresses.strip()] if result.addresses.strip() else []
            
            # Validate and clean addresses
            addresses = [addr.strip() for addr in addresses if addr and addr.strip()]
            
            # Ensure query type is valid
            query_type = result.query_type.lower()
            if query_type not in ['single', 'multiple', 'compare']:
                query_type = 'single' if len(addresses) <= 1 else 'multiple'
            
            return PropertyQuery(
                addresses=addresses,
                query_type=query_type,
                raw_message=message
            )
            
        except Exception as e:
            # Fallback to simple regex-based parsing if LLM fails
            return self._fallback_parse(message)
    
    def _fallback_parse(self, message: str) -> PropertyQuery:
        """Fallback parsing using simple heuristics when LLM fails"""
        # Simple regex patterns for fallback
        basic_patterns = [
            r'(\d+[A-Z]?\s+[^,\n]+(?:,\s*[^,\n]+)*)',  # Basic address pattern
        ]
        
        addresses = []
        for pattern in basic_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                addr = match.strip()
                if addr and len(addr) > 5 and addr not in addresses:
                    addresses.append(addr)
        
        # Simple query type determination
        message_lower = message.lower()
        if any(word in message_lower for word in ['compare', 'vs', 'versus']):
            query_type = 'compare'
        elif len(addresses) > 1 or any(word in message_lower for word in ['both', 'multiple', 'together']):
            query_type = 'multiple'
        else:
            query_type = 'single'
        
        return PropertyQuery(
            addresses=addresses,
            query_type=query_type,
            raw_message=message
        )
    
    
    def validate_addresses(self, addresses: List[str]) -> Tuple[List[str], List[str]]:
        """Validate addresses and return valid/invalid lists"""
        valid_addresses = []
        invalid_addresses = []
        
        for address in addresses:
            if self._is_valid_address(address):
                valid_addresses.append(address)
            else:
                invalid_addresses.append(address)
        
        return valid_addresses, invalid_addresses
    
    def _is_valid_address(self, address: str) -> bool:
        """Basic address validation"""
        # Must have at least a number and reasonable content
        if not re.search(r'\d+', address):
            return False
        
        # Must be reasonable length
        if len(address.strip()) < 5:
            return False
        
        # Should contain typical address components
        address_lower = address.lower()
        has_street_indicator = any(indicator in address_lower for indicator in 
                                 ['street', 'st', 'avenue', 'ave', 'road', 'rd', 'drive', 'dr', 
                                  'lane', 'ln', 'court', 'ct', 'place', 'pl', 'crescent', 'cres'])
        
        # Either has street indicator or has geographic pattern (number + name + location)
        has_geographic_pattern = len(address.split(',')) >= 2 or len(address.split()) >= 3
        
        return has_street_indicator or has_geographic_pattern
    
    def format_query_summary(self, query: PropertyQuery) -> str:
        """Create a summary of the parsed query for user confirmation"""
        if not query.addresses:
            return "❌ No valid addresses found in your message."
        
        summary = f"📍 Found {len(query.addresses)} address(es):\n"
        for i, addr in enumerate(query.addresses, 1):
            summary += f"{i}. {addr}\n"
        
        summary += f"\n🔍 Query type: {query.query_type.title()}"
        
        return summary