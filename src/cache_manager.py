"""
Caching system for DSPy real estate agent.
Provides both in-memory and persistent caching for property valuations.
"""

import hashlib
import json
import time
import pickle
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CacheStats:
    """Statistics for cache performance"""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.saves = 0
        self.evictions = 0
        self.start_time = datetime.now()
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def total_requests(self) -> int:
        """Total cache requests"""
        return self.hits + self.misses
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary"""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "saves": self.saves,
            "evictions": self.evictions,
            "hit_rate": self.hit_rate,
            "total_requests": self.total_requests,
            "uptime": str(datetime.now() - self.start_time).split('.')[0]
        }


class PropertyCache:
    """Intelligent caching system for property valuations"""
    
    def __init__(
        self, 
        max_memory_items: int = 100,
        memory_ttl_hours: int = 24,
        disk_cache_dir: str = "cache",
        disk_ttl_days: int = 7,
        enable_disk_cache: bool = True
    ):
        self.max_memory_items = max_memory_items
        self.memory_ttl = timedelta(hours=memory_ttl_hours)
        self.disk_ttl = timedelta(days=disk_ttl_days)
        self.enable_disk_cache = enable_disk_cache
        
        # In-memory cache: {cache_key: (data, timestamp, access_count)}
        self._memory_cache: Dict[str, Tuple[Any, datetime, int]] = {}
        
        # Disk cache directory
        self.disk_cache_dir = Path(disk_cache_dir)
        if self.enable_disk_cache:
            self.disk_cache_dir.mkdir(exist_ok=True)
        
        # Statistics
        self.stats = CacheStats()
        
        logger.info(f"Cache initialized: memory={max_memory_items}, disk={enable_disk_cache}")
    
    def _generate_cache_key(self, query_data: Dict[str, Any]) -> str:
        """Generate a unique cache key for query data"""
        # Normalize addresses for consistent caching
        normalized_data = self._normalize_query_data(query_data)
        
        # Create hash from normalized data
        data_str = json.dumps(normalized_data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def _normalize_query_data(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize query data for consistent caching"""
        normalized = query_data.copy()
        
        # Normalize addresses
        if 'addresses' in normalized:
            normalized['addresses'] = [
                self._normalize_address(addr) for addr in normalized['addresses']
            ]
            # Sort for consistent ordering
            normalized['addresses'].sort()
        
        # Normalize query type
        if 'query_type' in normalized:
            normalized['query_type'] = normalized['query_type'].lower().strip()
        
        return normalized
    
    def _normalize_address(self, address: str) -> str:
        """Normalize address string for consistent caching"""
        # Convert to lowercase and strip whitespace
        addr = address.lower().strip()
        
        # Remove common variations
        replacements = {
            ' street': ' st',
            ' avenue': ' ave',
            ' road': ' rd',
            ' drive': ' dr',
            ' lane': ' ln',
            ' court': ' ct',
            ' place': ' pl',
            ',  ': ', ',  # Multiple spaces after comma
            '  ': ' '     # Multiple spaces
        }
        
        for old, new in replacements.items():
            addr = addr.replace(old, new)
        
        return addr
    
    def get(self, query_data: Dict[str, Any]) -> Optional[Any]:
        """Get cached result for query"""
        cache_key = self._generate_cache_key(query_data)
        
        # Try memory cache first
        result = self._get_from_memory(cache_key)
        if result is not None:
            self.stats.hits += 1
            logger.debug(f"Cache hit (memory): {cache_key[:8]}...")
            return result
        
        # Try disk cache
        if self.enable_disk_cache:
            result = self._get_from_disk(cache_key)
            if result is not None:
                # Promote to memory cache
                self._save_to_memory(cache_key, result)
                self.stats.hits += 1
                logger.debug(f"Cache hit (disk): {cache_key[:8]}...")
                return result
        
        self.stats.misses += 1
        logger.debug(f"Cache miss: {cache_key[:8]}...")
        return None
    
    def set(self, query_data: Dict[str, Any], result: Any) -> None:
        """Cache result for query"""
        cache_key = self._generate_cache_key(query_data)
        
        # Save to memory cache
        self._save_to_memory(cache_key, result)
        
        # Save to disk cache
        if self.enable_disk_cache:
            self._save_to_disk(cache_key, result, query_data)
        
        self.stats.saves += 1
        logger.debug(f"Cached result: {cache_key[:8]}...")
    
    def _get_from_memory(self, cache_key: str) -> Optional[Any]:
        """Get result from memory cache"""
        if cache_key not in self._memory_cache:
            return None
        
        data, timestamp, access_count = self._memory_cache[cache_key]
        
        # Check if expired
        if datetime.now() - timestamp > self.memory_ttl:
            del self._memory_cache[cache_key]
            return None
        
        # Update access count
        self._memory_cache[cache_key] = (data, timestamp, access_count + 1)
        return data
    
    def _save_to_memory(self, cache_key: str, data: Any) -> None:
        """Save result to memory cache"""
        # Evict if at capacity
        if len(self._memory_cache) >= self.max_memory_items:
            self._evict_memory_cache()
        
        self._memory_cache[cache_key] = (data, datetime.now(), 1)
    
    def _evict_memory_cache(self) -> None:
        """Evict least recently used items from memory cache"""
        if not self._memory_cache:
            return
        
        # Sort by access count (ascending) then by timestamp (ascending)
        sorted_items = sorted(
            self._memory_cache.items(),
            key=lambda x: (x[1][2], x[1][1])  # (access_count, timestamp)
        )
        
        # Remove oldest 25% of items
        items_to_remove = max(1, len(sorted_items) // 4)
        for i in range(items_to_remove):
            key = sorted_items[i][0]
            del self._memory_cache[key]
            self.stats.evictions += 1
        
        logger.debug(f"Evicted {items_to_remove} items from memory cache")
    
    def _get_from_disk(self, cache_key: str) -> Optional[Any]:
        """Get result from disk cache"""
        cache_file = self.disk_cache_dir / f"{cache_key}.pkl"
        
        if not cache_file.exists():
            return None
        
        try:
            # Check file age
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - file_time > self.disk_ttl:
                cache_file.unlink()  # Delete expired file
                return None
            
            # Load cached data
            with open(cache_file, 'rb') as f:
                cached_data = pickle.load(f)
            
            return cached_data['result']
            
        except Exception as e:
            logger.warning(f"Error reading disk cache {cache_key}: {e}")
            # Delete corrupted file
            try:
                cache_file.unlink()
            except:
                pass
            return None
    
    def _save_to_disk(self, cache_key: str, result: Any, query_data: Dict[str, Any]) -> None:
        """Save result to disk cache"""
        cache_file = self.disk_cache_dir / f"{cache_key}.pkl"
        
        try:
            cached_data = {
                'result': result,
                'query_data': query_data,
                'timestamp': datetime.now(),
                'version': '1.0'
            }
            
            with open(cache_file, 'wb') as f:
                pickle.dump(cached_data, f)
                
        except Exception as e:
            logger.warning(f"Error saving to disk cache {cache_key}: {e}")
    
    def invalidate_address(self, address: str) -> int:
        """Invalidate all cache entries containing the given address"""
        normalized_addr = self._normalize_address(address)
        removed_count = 0
        
        # Remove from memory cache
        keys_to_remove = []
        for key in self._memory_cache:
            # We can't easily check the original query data from memory cache
            # So we'll skip this for now - could be enhanced later
            pass
        
        # Remove from disk cache
        if self.enable_disk_cache:
            for cache_file in self.disk_cache_dir.glob("*.pkl"):
                try:
                    with open(cache_file, 'rb') as f:
                        cached_data = pickle.load(f)
                    
                    query_data = cached_data.get('query_data', {})
                    addresses = query_data.get('addresses', [])
                    
                    # Check if any address matches
                    if any(normalized_addr in self._normalize_address(addr) 
                           for addr in addresses):
                        cache_file.unlink()
                        removed_count += 1
                        
                except Exception as e:
                    logger.warning(f"Error checking cache file {cache_file}: {e}")
        
        logger.info(f"Invalidated {removed_count} cache entries for address: {address}")
        return removed_count
    
    def clear_expired(self) -> Tuple[int, int]:
        """Clear expired cache entries"""
        memory_cleared = 0
        disk_cleared = 0
        
        # Clear expired memory cache
        current_time = datetime.now()
        expired_keys = [
            key for key, (_, timestamp, _) in self._memory_cache.items()
            if current_time - timestamp > self.memory_ttl
        ]
        
        for key in expired_keys:
            del self._memory_cache[key]
            memory_cleared += 1
        
        # Clear expired disk cache
        if self.enable_disk_cache:
            for cache_file in self.disk_cache_dir.glob("*.pkl"):
                try:
                    file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
                    if current_time - file_time > self.disk_ttl:
                        cache_file.unlink()
                        disk_cleared += 1
                except Exception as e:
                    logger.warning(f"Error clearing expired file {cache_file}: {e}")
        
        logger.info(f"Cleared {memory_cleared} memory + {disk_cleared} disk expired entries")
        return memory_cleared, disk_cleared
    
    def clear_all(self) -> Tuple[int, int]:
        """Clear all cache entries"""
        memory_count = len(self._memory_cache)
        disk_count = 0
        
        # Clear memory cache
        self._memory_cache.clear()
        
        # Clear disk cache
        if self.enable_disk_cache:
            for cache_file in self.disk_cache_dir.glob("*.pkl"):
                try:
                    cache_file.unlink()
                    disk_count += 1
                except Exception as e:
                    logger.warning(f"Error deleting cache file {cache_file}: {e}")
        
        logger.info(f"Cleared all cache: {memory_count} memory + {disk_count} disk entries")
        return memory_count, disk_count
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get comprehensive cache information"""
        memory_size = len(self._memory_cache)
        disk_size = 0
        disk_size_bytes = 0
        
        if self.enable_disk_cache and self.disk_cache_dir.exists():
            disk_files = list(self.disk_cache_dir.glob("*.pkl"))
            disk_size = len(disk_files)
            disk_size_bytes = sum(f.stat().st_size for f in disk_files)
        
        return {
            "memory_cache": {
                "size": memory_size,
                "max_size": self.max_memory_items,
                "ttl_hours": self.memory_ttl.total_seconds() / 3600
            },
            "disk_cache": {
                "enabled": self.enable_disk_cache,
                "size": disk_size,
                "size_bytes": disk_size_bytes,
                "size_mb": round(disk_size_bytes / (1024 * 1024), 2),
                "ttl_days": self.disk_ttl.days
            },
            "statistics": self.stats.to_dict()
        }