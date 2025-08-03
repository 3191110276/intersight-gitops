"""
Reference resolver for managing name-to-MOID and MOID-to-name conversions.

This module provides comprehensive reference resolution capabilities for
the GitOps workflow, including caching and batch processing.
"""

import logging
from typing import Dict, Any, List, Optional, Set, Tuple
from collections import defaultdict
import time

logger = logging.getLogger(__name__)


class ReferenceResolver:
    """
    Manages reference resolution between names and MOIDs for GitOps operations.
    
    This class provides:
    - Name-to-MOID resolution with caching
    - MOID-to-name conversion for export
    - Batch processing for improved performance
    - Cache management and invalidation
    """
    
    def __init__(self, api_client):
        """
        Initialize the reference resolver.
        
        Args:
            api_client: The Intersight API client instance
        """
        self.api_client = api_client
        
        # Cache for name-to-MOID mappings
        self._name_to_moid_cache: Dict[str, Dict[str, str]] = defaultdict(dict)
        
        # Cache for MOID-to-name mappings
        self._moid_to_name_cache: Dict[str, Dict[str, str]] = defaultdict(dict)
        
        # Cache timestamps for invalidation
        self._cache_timestamps: Dict[str, float] = {}
        
        # Cache TTL in seconds (5 minutes default)
        self.cache_ttl = 300
        
        # Track which object types have been fully cached
        self._fully_cached_types: Set[str] = set()
    
    def resolve_name_to_moid(self, object_type: str, name: str, organization_name: str = None) -> Optional[str]:
        """
        Resolve an object name to its MOID.
        
        Args:
            object_type: The Intersight object type
            name: The object name to resolve
            organization_name: Organization name for scoped objects
            
        Returns:
            MOID string or None if not found
        """
        try:
            # Check cache first
            cache_key = self._get_cache_key(object_type, organization_name)
            
            if self._is_cache_valid(cache_key) and name in self._name_to_moid_cache[cache_key]:
                logger.debug(f"Cache hit for {object_type} name '{name}'")
                return self._name_to_moid_cache[cache_key][name]
            
            # If not in cache, try to populate cache for this object type
            if cache_key not in self._fully_cached_types:
                self._populate_cache(object_type, organization_name)
            
            # Check cache again after population
            if name in self._name_to_moid_cache[cache_key]:
                return self._name_to_moid_cache[cache_key][name]
            
            # If still not found, do a direct query
            logger.debug(f"Direct query for {object_type} name '{name}'")
            return self._direct_name_lookup(object_type, name, organization_name)
            
        except Exception as e:
            logger.error(f"Failed to resolve name '{name}' for {object_type}: {e}")
            return None
    
    def resolve_moid_to_name(self, object_type: str, moid: str) -> Optional[str]:
        """
        Resolve a MOID to its object name.
        
        Args:
            object_type: The Intersight object type
            moid: The MOID to resolve
            
        Returns:
            Object name or None if not found
        """
        try:
            # Check cache first
            cache_key = self._get_cache_key(object_type)
            
            if self._is_cache_valid(cache_key) and moid in self._moid_to_name_cache[cache_key]:
                logger.debug(f"Cache hit for {object_type} MOID '{moid}'")
                return self._moid_to_name_cache[cache_key][moid]
            
            # If not in cache, try to populate cache for this object type
            if cache_key not in self._fully_cached_types:
                self._populate_cache(object_type)
            
            # Check cache again after population
            if moid in self._moid_to_name_cache[cache_key]:
                return self._moid_to_name_cache[cache_key][moid]
            
            # If still not found, do a direct query
            logger.debug(f"Direct query for {object_type} MOID '{moid}'")
            return self._direct_moid_lookup(object_type, moid)
            
        except Exception as e:
            logger.error(f"Failed to resolve MOID '{moid}' for {object_type}: {e}")
            return None
    
    def convert_moid_reference_to_name(self, reference: Dict[str, Any], fallback_name: str = None) -> str:
        """
        Convert a MOID reference dictionary to a name string for GitOps export.
        
        This method handles the common pattern of converting Intersight MOID references
        to name-based references for GitOps compatibility.
        
        Args:
            reference: Dictionary containing MOID reference (e.g., Organization reference)
            fallback_name: Name to use if resolution fails (default: 'default')
            
        Returns:
            Resolved name string or fallback
        """
        if not isinstance(reference, dict):
            # If it's already a string, return as-is
            if isinstance(reference, str):
                return reference
            logger.warning(f"Invalid reference type: {type(reference)}, using fallback")
            return fallback_name or 'default'
        
        # Try to get name directly from reference
        if 'Name' in reference or 'name' in reference:
            name = reference.get('Name') or reference.get('name')
            if name:
                return name
        
        # Try to resolve MOID to name
        moid = reference.get('Moid') or reference.get('moid')
        object_type = reference.get('ObjectType') or reference.get('object_type')
        
        if moid and object_type:
            resolved_name = self.resolve_moid_to_name(object_type, moid)
            if resolved_name:
                logger.debug(f"Successfully resolved {object_type} MOID '{moid}' to name '{resolved_name}'")
                return resolved_name
            else:
                logger.warning(f"Could not resolve {object_type} MOID '{moid}' to name, using fallback '{fallback_name or 'default'}'")
        else:
            logger.warning(f"Reference missing required fields (Moid/ObjectType): {reference}")
        
        return fallback_name or 'default'
    
    def batch_resolve_names_to_moids(self, references: List[Tuple[str, str, str]]) -> Dict[Tuple[str, str, str], Optional[str]]:
        """
        Batch resolve multiple name references to MOIDs.
        
        Args:
            references: List of tuples (object_type, name, organization_name)
            
        Returns:
            Dictionary mapping (object_type, name, organization_name) to MOID
        """
        results = {}
        
        # Group by object type for efficient batch processing
        by_type = defaultdict(list)
        for ref in references:
            by_type[ref[0]].append(ref)
        
        # Process each object type
        for object_type, type_refs in by_type.items():
            # Populate cache for this type if needed
            cache_key = self._get_cache_key(object_type)
            if cache_key not in self._fully_cached_types:
                self._populate_cache(object_type)
            
            # Resolve each reference
            for object_type, name, org_name in type_refs:
                moid = self.resolve_name_to_moid(object_type, name, org_name)
                results[(object_type, name, org_name)] = moid
        
        return results
    
    def batch_resolve_moids_to_names(self, references: List[Tuple[str, str]]) -> Dict[Tuple[str, str], Optional[str]]:
        """
        Batch resolve multiple MOID references to names.
        
        Args:
            references: List of tuples (object_type, moid)
            
        Returns:
            Dictionary mapping (object_type, moid) to name
        """
        results = {}
        
        # Group by object type for efficient batch processing
        by_type = defaultdict(list)
        for ref in references:
            by_type[ref[0]].append(ref)
        
        # Process each object type
        for object_type, type_refs in by_type.items():
            # Populate cache for this type if needed
            cache_key = self._get_cache_key(object_type)
            if cache_key not in self._fully_cached_types:
                self._populate_cache(object_type)
            
            # Resolve each reference
            for object_type, moid in type_refs:
                name = self.resolve_moid_to_name(object_type, moid)
                results[(object_type, moid)] = name
        
        return results
    
    def invalidate_cache(self, object_type: str = None):
        """
        Invalidate cached data.
        
        Args:
            object_type: Specific object type to invalidate, or None for all
        """
        if object_type:
            # Invalidate specific type
            cache_keys_to_remove = [
                key for key in self._cache_timestamps.keys() 
                if key.startswith(f"{object_type}:")
            ]
            for key in cache_keys_to_remove:
                del self._cache_timestamps[key]
                if key in self._name_to_moid_cache:
                    del self._name_to_moid_cache[key]
                if key in self._moid_to_name_cache:
                    del self._moid_to_name_cache[key]
                self._fully_cached_types.discard(key)
            
            logger.info(f"Invalidated cache for {object_type}")
        else:
            # Invalidate all
            self._cache_timestamps.clear()
            self._name_to_moid_cache.clear()
            self._moid_to_name_cache.clear()
            self._fully_cached_types.clear()
            
            logger.info("Invalidated all cached data")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        stats = {
            'cached_types': len(self._cache_timestamps),
            'name_to_moid_entries': sum(len(cache) for cache in self._name_to_moid_cache.values()),
            'moid_to_name_entries': sum(len(cache) for cache in self._moid_to_name_cache.values()),
            'fully_cached_types': len(self._fully_cached_types),
            'cache_ttl_seconds': self.cache_ttl
        }
        
        # Add per-type statistics
        stats['by_type'] = {}
        for cache_key in self._cache_timestamps:
            object_type = cache_key.split(':')[0]
            stats['by_type'][object_type] = {
                'name_to_moid_count': len(self._name_to_moid_cache.get(cache_key, {})),
                'moid_to_name_count': len(self._moid_to_name_cache.get(cache_key, {})),
                'cached_at': self._cache_timestamps[cache_key],
                'is_valid': self._is_cache_valid(cache_key)
            }
        
        return stats
    
    def _get_cache_key(self, object_type: str, organization_name: str = None) -> str:
        """Generate cache key for an object type and optional organization."""
        if organization_name:
            return f"{object_type}:{organization_name}"
        return f"{object_type}:global"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid."""
        if cache_key not in self._cache_timestamps:
            return False
        
        age = time.time() - self._cache_timestamps[cache_key]
        return age < self.cache_ttl
    
    def _populate_cache(self, object_type: str, organization_name: str = None):
        """
        Populate cache for an object type by querying all objects.
        
        Args:
            object_type: The object type to cache
            organization_name: Organization name for scoped objects
        """
        try:
            logger.debug(f"Populating cache for {object_type}")
            
            # Query all objects of this type
            query_kwargs = {}
            if organization_name:
                query_kwargs['filter'] = f"Organization/Name eq '{organization_name}'"
            
            objects = self.api_client.query_objects(object_type, **query_kwargs)
            
            cache_key = self._get_cache_key(object_type, organization_name)
            
            # Populate both caches
            name_cache = {}
            moid_cache = {}
            
            for obj in objects:
                name = obj.get('Name')
                moid = obj.get('Moid')
                
                if name and moid:
                    name_cache[name] = moid
                    moid_cache[moid] = name
            
            # Update caches
            self._name_to_moid_cache[cache_key] = name_cache
            self._moid_to_name_cache[cache_key] = moid_cache
            self._cache_timestamps[cache_key] = time.time()
            self._fully_cached_types.add(cache_key)
            
            logger.info(f"Cached {len(name_cache)} {object_type} objects")
            
        except Exception as e:
            logger.error(f"Failed to populate cache for {object_type}: {e}")
    
    def _direct_name_lookup(self, object_type: str, name: str, organization_name: str = None) -> Optional[str]:
        """
        Perform direct API lookup for a name.
        
        Args:
            object_type: The object type
            name: The name to look up
            organization_name: Organization name for scoped objects
            
        Returns:
            MOID or None if not found
        """
        try:
            filter_expr = f"Name eq '{name}'"
            if organization_name:
                filter_expr += f" and Organization/Name eq '{organization_name}'"
            
            objects = self.api_client.query_objects(object_type, filter=filter_expr)
            
            if objects:
                moid = objects[0].get('Moid')
                if moid:
                    # Cache the result
                    cache_key = self._get_cache_key(object_type, organization_name)
                    self._name_to_moid_cache[cache_key][name] = moid
                    self._moid_to_name_cache[cache_key][moid] = name
                    return moid
            
            return None
            
        except Exception as e:
            logger.error(f"Direct name lookup failed for {object_type} '{name}': {e}")
            return None
    
    def _direct_moid_lookup(self, object_type: str, moid: str) -> Optional[str]:
        """
        Perform direct API lookup for a MOID.
        
        Args:
            object_type: The object type
            moid: The MOID to look up
            
        Returns:
            Object name or None if not found
        """
        try:
            obj = self.api_client.get_object_by_moid(object_type, moid)
            
            if obj:
                name = obj.get('Name')
                if name:
                    # Cache the result
                    cache_key = self._get_cache_key(object_type)
                    self._name_to_moid_cache[cache_key][name] = moid
                    self._moid_to_name_cache[cache_key][moid] = name
                    return name
            
            return None
            
        except Exception as e:
            logger.error(f"Direct MOID lookup failed for {object_type} '{moid}': {e}")
            return None