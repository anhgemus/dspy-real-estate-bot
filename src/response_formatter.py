"""
Response formatting utilities for Telegram bot.
Formats property valuation results for user-friendly display.
"""

from typing import Any, Dict
from pydantic import BaseModel


class FormattedResponse(BaseModel):
    """Formatted response for Telegram"""
    text: str
    parse_mode: str = "Markdown"


class ResponseFormatter:
    """Formatter for property valuation responses"""
    
    def __init__(self):
        self.max_message_length = 4096  # Telegram limit
    
    def format_property_valuation(self, prediction: Any) -> FormattedResponse:
        """Format a complete property valuation response"""
        try:
            # Extract key information
            confidence_emoji = self._get_confidence_emoji(prediction.confidence)
            
            response = f"""🏠 *Property Valuation Report* {confidence_emoji}

📍 *Property Details*
{self._format_property_details(prediction.property_details)}

💰 *Final Estimate*
{self._format_final_estimate(prediction.final_estimate)}

📊 *Price Range*
{self._format_price_range(prediction.price_range)}

🏘️ *Comparable Sales*
{self._format_comparable_sales(prediction.comparable_sales)}

📈 *Market Analysis*
{self._format_market_analysis(prediction.neighborhood_analysis, prediction.market_adjustments)}

🔍 *Confidence Level*
{self._format_confidence(prediction.confidence)}

⚡ *Analysis Complete*"""

            # Truncate if too long
            if len(response) > self.max_message_length:
                response = self._create_summary_response(prediction)
            
            return FormattedResponse(text=response)
            
        except Exception as e:
            return self._format_error_response(str(e))
    
    def format_multiple_properties(self, prediction: Any) -> FormattedResponse:
        """Format response for multiple adjacent properties"""
        try:
            confidence_emoji = self._get_confidence_emoji(prediction.confidence)
            
            response = f"""🏘️ *Combined Property Valuation* {confidence_emoji}

📍 *Properties Analyzed*
{self._format_property_details(prediction.property_details)}

💰 *Combined Estimate*
{self._format_final_estimate(prediction.final_estimate)}

📊 *Price Range*
{self._format_price_range(prediction.price_range)}

🔗 *Land Assembly Premium*
{self._format_land_assembly_info(prediction.market_adjustments)}

🏘️ *Market Context*
{self._format_market_analysis(prediction.neighborhood_analysis, prediction.market_adjustments)}

🔍 *Confidence Level*
{self._format_confidence(prediction.confidence)}

⚡ *Analysis Complete*"""

            if len(response) > self.max_message_length:
                response = self._create_summary_response(prediction)
                
            return FormattedResponse(text=response)
            
        except Exception as e:
            return self._format_error_response(str(e))
    
    def format_quick_estimate(self, address: str, estimate: str, confidence: float) -> FormattedResponse:
        """Format a quick estimate response"""
        confidence_emoji = self._get_confidence_emoji(confidence)
        
        response = f"""🏠 *Quick Estimate* {confidence_emoji}

📍 *Address*
{address}

💰 *Estimated Value*
{estimate}

🔍 *Confidence*
{int(confidence * 100)}%

💡 Use /detailed for full analysis"""

        return FormattedResponse(text=response)
    
    def format_processing_message(self, addresses: list) -> FormattedResponse:
        """Format a processing message"""
        if len(addresses) == 1:
            text = f"🔍 Analyzing property at:\n📍 {addresses[0]}\n\n⏳ This may take 30-60 seconds..."
        else:
            text = f"🔍 Analyzing {len(addresses)} properties:\n"
            for i, addr in enumerate(addresses, 1):
                text += f"📍 {i}. {addr}\n"
            text += "\n⏳ This may take 60-90 seconds..."
        
        return FormattedResponse(text=text)
    
    def format_help_message(self) -> FormattedResponse:
        """Format help message"""
        response = """🏠 *Real Estate Valuation Bot*

*Available Commands:*
/start - Welcome message
/help - Show this help
/estimate - Get property valuation

*How to Use:*
Just send me an address like:
• "What's 123 Main St, City, State worth?"
• "Estimate 456 Oak Ave"
• "Value of 789 Pine St, Suburb, STATE 1234"

*Multiple Properties:*
• "Value of 123 Main St and 125 Main St together"
• "Compare 456 Oak Ave vs 458 Oak Ave"

*Features:*
✅ Individual property valuations
✅ Adjacent property combinations
✅ Land assembly premiums
✅ Neighborhood analysis
✅ Confidence scoring

💡 *Tip:* Include full addresses with suburb/city and postal code for best results."""

        return FormattedResponse(text=response)
    
    def _format_property_details(self, details: str) -> str:
        """Format property details section"""
        lines = details.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('-'):
                formatted_lines.append(f"• {line}")
            elif line.startswith('-'):
                formatted_lines.append(f"• {line[1:].strip()}")
        
        return '\n'.join(formatted_lines[:5])  # Limit lines
    
    def _format_final_estimate(self, estimate: str) -> str:
        """Format final estimate"""
        lines = estimate.split('\n')
        estimate_line = ""
        
        for line in lines:
            if '$' in line and ('estimate' in line.lower() or 'final' in line.lower()):
                estimate_line = line.strip()
                break
        
        if not estimate_line and lines:
            estimate_line = lines[0].strip()
        
        return f"*{estimate_line}*" if estimate_line else "*Estimate not available*"
    
    def _format_price_range(self, price_range: str) -> str:
        """Format price range"""
        return f"`{price_range.strip()}`"
    
    def _format_comparable_sales(self, comps: str) -> str:
        """Format comparable sales (truncated)"""
        lines = comps.split('\n')
        formatted = []
        
        for line in lines[:3]:  # Limit to 3 comps
            if line.strip() and '$' in line:
                formatted.append(f"• {line.strip()}")
        
        if len(lines) > 3:
            formatted.append("• _(... and more)_")
        
        return '\n'.join(formatted) if formatted else "No recent comparables found"
    
    def _format_market_analysis(self, neighborhood: str, adjustments: str) -> str:
        """Format market analysis section"""
        key_points = []
        
        # Extract key points from neighborhood analysis
        for line in neighborhood.split('\n'):
            if line.strip() and ('school' in line.lower() or 'crime' in line.lower() or 'median' in line.lower()):
                key_points.append(f"• {line.strip()}")
        
        return '\n'.join(key_points[:3])  # Limit points
    
    def _format_land_assembly_info(self, adjustments: str) -> str:
        """Extract and format land assembly information"""
        for line in adjustments.split('\n'):
            if 'assembly' in line.lower() or 'premium' in line.lower():
                return f"• {line.strip()}"
        
        return "• Standard market conditions applied"
    
    def _format_confidence(self, confidence: float) -> str:
        """Format confidence level"""
        percentage = int(confidence * 100)
        if percentage >= 80:
            level = "High"
            emoji = "🟢"
        elif percentage >= 60:
            level = "Medium"
            emoji = "🟡"
        else:
            level = "Low"
            emoji = "🔴"
        
        return f"{emoji} {percentage}% ({level})"
    
    def _get_confidence_emoji(self, confidence: float) -> str:
        """Get emoji based on confidence level"""
        if confidence >= 0.8:
            return "🎯"
        elif confidence >= 0.6:
            return "📊"
        else:
            return "❓"
    
    def _create_summary_response(self, prediction: Any) -> str:
        """Create a shorter summary response"""
        try:
            confidence_emoji = self._get_confidence_emoji(prediction.confidence)
            
            return f"""🏠 *Property Valuation Summary* {confidence_emoji}

💰 *{self._format_final_estimate(prediction.final_estimate)}*

📊 *Range:* {self._format_price_range(prediction.price_range)}

🔍 *Confidence:* {self._format_confidence(prediction.confidence)}

💡 Full report available - contact for details"""
            
        except Exception:
            return "📊 Valuation complete - contact for detailed results"
    
    def _format_error_response(self, error: str) -> FormattedResponse:
        """Format error response"""
        response = f"""❌ *Analysis Error*

Sorry, I encountered an issue processing your request.

*Error:* {error[:100]}...

Please try:
• Checking the address format
• Using a more specific address
• Trying again in a few moments

Type /help for usage examples."""

        return FormattedResponse(text=response)