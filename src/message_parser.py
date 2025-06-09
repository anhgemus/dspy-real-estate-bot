"""
Message parsing utilities for Telegram bot.
Extracts addresses and property queries from user messages.
"""

import re
from typing import List, Optional, Tuple
from pydantic import BaseModel


class PropertyQuery(BaseModel):
    """Structured property query from user message"""
    addresses: List[str]
    query_type: str  # 'single', 'multiple', 'compare'
    raw_message: str


class MessageParser:
    """Parser for extracting property information from user messages"""
    
    # Address pattern for various international formats
    ADDRESS_PATTERNS = [
        # Australian format: "123 Street Name, Suburb, STATE 1234"
        r'(\d+[A-Z]?\s+[^,]+,\s*[^,]+,\s*[A-Z]{2,3}\s*\d{4}(?:\s*[A-Za-z]+)?)',
        # US format: "123 Street Name, City, ST 12345"
        r'(\d+[A-Z]?\s+[^,]+,\s*[^,]+,\s*[A-Z]{2}\s*\d{5})',
        # UK format: "123 Street Name, City, Postcode"
        r'(\d+[A-Z]?\s+[^,]+,\s*[^,]+,\s*[A-Z]{1,2}\d{1,2}[A-Z]?\s*\d[A-Z]{2})',
        # Simple format: "123 Street Name"
        r'(\d+[A-Z]?\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Court|Ct|Place|Pl))',
    ]
    
    # Query type indicators
    COMPARISON_KEYWORDS = ['compare', 'vs', 'versus', 'difference', 'both', 'together']
    MULTIPLE_KEYWORDS = ['and', '&', 'plus', 'combined', 'together']
    
    def parse_message(self, message: str) -> PropertyQuery:
        """Parse user message and extract property query information"""
        addresses = self._extract_addresses(message)
        query_type = self._determine_query_type(message, addresses)
        
        return PropertyQuery(
            addresses=addresses,
            query_type=query_type,
            raw_message=message
        )
    
    def _extract_addresses(self, message: str) -> List[str]:
        """Extract addresses from message using regex patterns"""
        addresses = []
        
        for pattern in self.ADDRESS_PATTERNS:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                # Clean up the address
                cleaned_address = match.strip()
                if cleaned_address not in addresses:
                    addresses.append(cleaned_address)
        
        return addresses
    
    def _determine_query_type(self, message: str, addresses: List[str]) -> str:
        """Determine the type of query based on message content and addresses"""
        message_lower = message.lower()
        
        # Check for comparison keywords
        if any(keyword in message_lower for keyword in self.COMPARISON_KEYWORDS):
            return 'compare'
        
        # Check for multiple property keywords
        if (len(addresses) > 1 or 
            any(keyword in message_lower for keyword in self.MULTIPLE_KEYWORDS)):
            return 'multiple'
        
        return 'single'
    
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
        # Must have at least a number and street name
        if not re.search(r'\d+', address):
            return False
        
        # Must be reasonable length
        if len(address.strip()) < 5:
            return False
        
        return True
    
    def format_query_summary(self, query: PropertyQuery) -> str:
        """Create a summary of the parsed query for user confirmation"""
        if not query.addresses:
            return "❌ No valid addresses found in your message."
        
        summary = f"📍 Found {len(query.addresses)} address(es):\n"
        for i, addr in enumerate(query.addresses, 1):
            summary += f"{i}. {addr}\n"
        
        summary += f"\n🔍 Query type: {query.query_type.title()}"
        
        return summary