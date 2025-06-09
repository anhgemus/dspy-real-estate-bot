#!/usr/bin/env python3
"""
Test script for caching functionality.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cache_manager import PropertyCache
from src.message_parser import PropertyQuery

def test_cache_basic():
    """Test basic cache functionality"""
    print("🧪 Testing Basic Cache Functionality...")
    
    # Create temporary cache directory
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = PropertyCache(
            max_memory_items=5,
            memory_ttl_hours=1,
            disk_cache_dir=temp_dir,
            disk_ttl_days=1,
            enable_disk_cache=True
        )
        
        # Test data
        query_data = {
            'addresses': ['123 Main St, City, STATE 12345'],
            'query_type': 'single'
        }
        
        fake_result = {
            'estimate': '$500,000',
            'confidence': 0.85,
            'analysis': 'Test property analysis'
        }
        
        # Test cache miss
        result = cache.get(query_data)
        assert result is None, "Should be cache miss initially"
        print("✅ Cache miss test passed")
        
        # Test cache set and hit
        cache.set(query_data, fake_result)
        result = cache.get(query_data)
        assert result == fake_result, "Should return cached result"
        print("✅ Cache hit test passed")
        
        # Test address normalization
        query_data_normalized = {
            'addresses': ['123 main street, city, state 12345'],  # Different case
            'query_type': 'single'
        }
        result = cache.get(query_data_normalized)
        assert result == fake_result, "Should normalize addresses for cache hits"
        print("✅ Address normalization test passed")
        
        # Test statistics
        stats = cache.get_cache_info()
        assert stats['statistics']['hits'] >= 1, "Should track cache hits"
        assert stats['statistics']['misses'] >= 1, "Should track cache misses"
        print("✅ Statistics tracking test passed")

def test_cache_advanced():
    """Test advanced cache features"""
    print("\n🔧 Testing Advanced Cache Features...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = PropertyCache(
            max_memory_items=2,  # Small limit to test eviction
            memory_ttl_hours=24,
            disk_cache_dir=temp_dir,
            enable_disk_cache=True
        )
        
        # Test multiple properties
        for i in range(5):
            query_data = {
                'addresses': [f'{100 + i} Test St, City, STATE 12345'],
                'query_type': 'single'
            }
            fake_result = {'estimate': f'${(i+1)*100000}', 'confidence': 0.8}
            cache.set(query_data, fake_result)
        
        # Memory cache should have evicted some entries
        cache_info = cache.get_cache_info()
        assert cache_info['memory_cache']['size'] <= 2, "Should respect memory limit"
        print("✅ Memory eviction test passed")
        
        # Test disk cache persistence
        assert cache_info['disk_cache']['size'] > 0, "Should have disk cache entries"
        print("✅ Disk cache persistence test passed")
        
        # Test cache clearing
        memory_count, disk_count = cache.clear_all()
        assert memory_count >= 0, "Should report cleared memory entries"
        assert disk_count >= 0, "Should report cleared disk entries"
        
        cache_info_after = cache.get_cache_info()
        assert cache_info_after['memory_cache']['size'] == 0, "Memory cache should be empty"
        assert cache_info_after['disk_cache']['size'] == 0, "Disk cache should be empty"
        print("✅ Cache clearing test passed")

def test_cache_integration():
    """Test cache with message parser integration"""
    print("\n🔗 Testing Cache Integration...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = PropertyCache(disk_cache_dir=temp_dir)
        
        # Create sample queries
        queries = [
            "What's 123 Main Street, New York, NY 10001 worth?",
            "Estimate 456 Oak Avenue, Los Angeles, CA 90210",
            "Value of 789 Pine St and 791 Pine St together"
        ]
        
        from src.message_parser import MessageParser
        parser = MessageParser()
        
        for query_text in queries:
            query = parser.parse_message(query_text)
            
            # Create cache data from query
            cache_data = {
                'addresses': query.addresses,
                'query_type': query.query_type
            }
            
            # Test caching with parsed data
            fake_result = {
                'query': query_text[:30],
                'estimate': '$750,000',
                'confidence': 0.9
            }
            
            # Cache miss first
            result = cache.get(cache_data)
            assert result is None, f"Should be cache miss for: {query_text[:30]}"
            
            # Cache and hit
            cache.set(cache_data, fake_result)
            result = cache.get(cache_data)
            assert result == fake_result, f"Should cache hit for: {query_text[:30]}"
        
        print("✅ Parser integration test passed")

def main():
    """Run all cache tests"""
    print("🚀 Testing Cache System\n")
    
    try:
        test_cache_basic()
        test_cache_advanced()
        test_cache_integration()
        
        print("\n✅ All cache tests passed!")
        print("\n💡 Cache Features Verified:")
        print("• In-memory caching with LRU eviction")
        print("• Persistent disk caching")
        print("• Address normalization")
        print("• Statistics tracking")
        print("• Cache invalidation")
        print("• Integration with message parser")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Cache test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())