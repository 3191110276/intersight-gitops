"""
Organization Name Resolution System.

This module provides a comprehensive organization name-to-MOID resolution mechanism
that supports multiple strategies for resolving organization names during import operations.
"""

import os
import json
import logging
import yaml
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class OrganizationInfo:
    """Information about an organization."""
    moid: str
    name: str
    object_type: str
    source: str  # 'exported_file', 'api_query', 'cache'
    timestamp: datetime


class OrganizationResolver:
    """
    Comprehensive organization name resolution system.
    
    This class provides multiple strategies for resolving organization names to MOIDs:
    1. Resolution from exported organization YAML files
    2. API lookup as fallback
    3. In-memory caching for performance
    4. Validation and error handling
    """
    
    def __init__(self, api_client=None, cache_ttl_minutes: int = 60):
        """
        Initialize the organization resolver.
        
        Args:
            api_client: Intersight API client instance
            cache_ttl_minutes: Cache time-to-live in minutes
        """
        self.api_client = api_client
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        
        # Organization caches
        self._name_to_moid_cache: Dict[str, OrganizationInfo] = {}
        self._moid_to_name_cache: Dict[str, OrganizationInfo] = {}
        self._exported_orgs: Dict[str, OrganizationInfo] = {}
        
        # Resolution statistics
        self.stats = {
            'cache_hits': 0,
            'exported_file_hits': 0,
            'api_query_hits': 0,
            'resolution_failures': 0
        }
    
    def load_exported_organizations(self, export_dir: str) -> int:
        """
        Load organization information from exported YAML files.
        
        Args:
            export_dir: Directory containing exported organization files
            
        Returns:
            Number of organizations loaded from exported files
        """
        logger.info(f"Loading exported organizations from {export_dir}")
        
        org_dir = os.path.join(export_dir, 'organizations')
        if not os.path.exists(org_dir):
            logger.warning(f"Organizations directory not found: {org_dir}")
            return 0
        
        loaded_count = 0
        
        # Search for organization YAML files
        org_path = Path(org_dir)
        for yaml_file in org_path.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    org_data = yaml.safe_load(f)
                
                if isinstance(org_data, dict) and org_data.get('ObjectType') == 'organization.Organization':
                    name = org_data.get('Name')
                    if name:
                        # Create organization info from exported data
                        # Note: We don't have MOID from exported files, we'll need to resolve via API
                        org_info = OrganizationInfo(
                            moid='',  # Will be resolved when needed
                            name=name,
                            object_type='organization.Organization',
                            source='exported_file',
                            timestamp=datetime.now()
                        )
                        
                        self._exported_orgs[name] = org_info
                        loaded_count += 1
                        logger.debug(f"Loaded exported organization: {name}")
                    else:
                        logger.warning(f"Organization YAML missing Name field: {yaml_file}")
                else:
                    logger.debug(f"Skipping non-organization file: {yaml_file}")
                    
            except Exception as e:
                logger.error(f"Failed to load organization from {yaml_file}: {e}")
        
        # Also check for .yml extension
        for yml_file in org_path.glob("*.yml"):
            try:
                with open(yml_file, 'r') as f:
                    org_data = yaml.safe_load(f)
                
                if isinstance(org_data, dict) and org_data.get('ObjectType') == 'organization.Organization':
                    name = org_data.get('Name')
                    if name and name not in self._exported_orgs:  # Avoid duplicates
                        org_info = OrganizationInfo(
                            moid='',
                            name=name,
                            object_type='organization.Organization',
                            source='exported_file',
                            timestamp=datetime.now()
                        )
                        
                        self._exported_orgs[name] = org_info
                        loaded_count += 1
                        logger.debug(f"Loaded exported organization: {name}")
                        
            except Exception as e:
                logger.error(f"Failed to load organization from {yml_file}: {e}")
        
        logger.info(f"Loaded {loaded_count} organizations from exported files")
        return loaded_count
    
    def resolve_name_to_moid(self, org_name: str) -> Optional[str]:
        """
        Resolve an organization name to its MOID using multiple strategies.
        
        Resolution strategies (in order):
        1. Check in-memory cache
        2. Check exported organization files
        3. Query Intersight API
        
        Args:
            org_name: Organization name to resolve
            
        Returns:
            Organization MOID or None if not found
        """
        if not org_name:
            return None
        
        # Strategy 1: Check in-memory cache
        if org_name in self._name_to_moid_cache:
            cached_org = self._name_to_moid_cache[org_name]
            
            # Check if cache entry is still valid
            if datetime.now() - cached_org.timestamp < self.cache_ttl:
                self.stats['cache_hits'] += 1
                logger.debug(f"Cache hit for organization '{org_name}': {cached_org.moid}")
                return cached_org.moid
            else:
                # Cache expired, remove entry
                del self._name_to_moid_cache[org_name]
                logger.debug(f"Cache entry expired for organization '{org_name}'")
        
        # Strategy 2: Check if organization is in exported files
        if org_name in self._exported_orgs:
            self.stats['exported_file_hits'] += 1
            logger.debug(f"Found organization '{org_name}' in exported files")
            
            # Try to resolve MOID via API for exported organization
            moid = self._query_organization_moid_from_api(org_name)
            if moid:
                # Update exported org info with MOID and cache it
                org_info = OrganizationInfo(
                    moid=moid,
                    name=org_name,
                    object_type='organization.Organization',
                    source='exported_file',
                    timestamp=datetime.now()
                )
                
                self._name_to_moid_cache[org_name] = org_info
                self._moid_to_name_cache[moid] = org_info
                
                return moid
        
        # Strategy 3: Query Intersight API directly
        moid = self._query_organization_moid_from_api(org_name)
        if moid:
            self.stats['api_query_hits'] += 1
            
            # Cache the result
            org_info = OrganizationInfo(
                moid=moid,
                name=org_name,
                object_type='organization.Organization',
                source='api_query',
                timestamp=datetime.now()
            )
            
            self._name_to_moid_cache[org_name] = org_info
            self._moid_to_name_cache[moid] = org_info
            
            logger.debug(f"API query resolved organization '{org_name}' to MOID: {moid}")
            return moid
        
        # All strategies failed
        self.stats['resolution_failures'] += 1
        logger.warning(f"Failed to resolve organization name '{org_name}' to MOID")
        return None
    
    def resolve_moid_to_name(self, org_moid: str) -> Optional[str]:
        """
        Resolve an organization MOID to its name.
        
        Args:
            org_moid: Organization MOID to resolve
            
        Returns:
            Organization name or None if not found
        """
        if not org_moid:
            return None
        
        # Check in-memory cache
        if org_moid in self._moid_to_name_cache:
            cached_org = self._moid_to_name_cache[org_moid]
            
            # Check if cache entry is still valid
            if datetime.now() - cached_org.timestamp < self.cache_ttl:
                self.stats['cache_hits'] += 1
                logger.debug(f"Cache hit for organization MOID '{org_moid}': {cached_org.name}")
                return cached_org.name
            else:
                # Cache expired, remove entry
                del self._moid_to_name_cache[org_moid]
                logger.debug(f"Cache entry expired for organization MOID '{org_moid}'")
        
        # Query API for MOID-to-name resolution
        name = self._query_organization_name_from_api(org_moid)
        if name:
            # Cache the result
            org_info = OrganizationInfo(
                moid=org_moid,
                name=name,
                object_type='organization.Organization',
                source='api_query',
                timestamp=datetime.now()
            )
            
            self._name_to_moid_cache[name] = org_info
            self._moid_to_name_cache[org_moid] = org_info
            
            logger.debug(f"API query resolved organization MOID '{org_moid}' to name: {name}")
            return name
        
        logger.warning(f"Failed to resolve organization MOID '{org_moid}' to name")
        return None
    
    def _query_organization_moid_from_api(self, org_name: str) -> Optional[str]:
        """Query organization MOID from Intersight API by name."""
        if not self.api_client:
            return None
        
        try:
            orgs = self.api_client.query_objects('organization.Organization')
            for org in orgs:
                if org.get('Name') == org_name:
                    return org.get('Moid')
                    
        except Exception as e:
            logger.error(f"Failed to query organization '{org_name}' from API: {e}")
        
        return None
    
    def _query_organization_name_from_api(self, org_moid: str) -> Optional[str]:
        """Query organization name from Intersight API by MOID."""
        if not self.api_client:
            return None
        
        try:
            org = self.api_client.get_object_by_moid('organization.Organization', org_moid)
            if org:
                return org.get('Name')
                
        except Exception as e:
            logger.error(f"Failed to query organization MOID '{org_moid}' from API: {e}")
        
        return None
    
    def validate_organization_reference(self, org_ref: Any) -> bool:
        """
        Validate an organization reference.
        
        Args:
            org_ref: Organization reference (string name or object)
            
        Returns:
            True if the reference is valid and resolvable
        """
        if isinstance(org_ref, str):
            # String reference - check if we can resolve it
            return self.resolve_name_to_moid(org_ref) is not None
        
        elif isinstance(org_ref, dict):
            # Object reference - check if it has valid fields
            if 'Name' in org_ref:
                return self.resolve_name_to_moid(org_ref['Name']) is not None
            elif 'Moid' in org_ref:
                return self.resolve_moid_to_name(org_ref['Moid']) is not None
        
        return False
    
    def get_available_organizations(self) -> List[str]:
        """
        Get list of available organization names.
        
        Returns:
            List of organization names from exported files and cache
        """
        org_names = set()
        
        # Add organizations from exported files
        org_names.update(self._exported_orgs.keys())
        
        # Add organizations from cache
        org_names.update(self._name_to_moid_cache.keys())
        
        return sorted(list(org_names))
    
    def clear_cache(self):
        """Clear all cached organization information."""
        self._name_to_moid_cache.clear()
        self._moid_to_name_cache.clear()
        logger.info("Cleared organization resolution cache")
    
    def get_resolution_stats(self) -> Dict[str, Any]:
        """
        Get resolution statistics.
        
        Returns:
            Dictionary containing resolution statistics
        """
        return {
            'cache_hits': self.stats['cache_hits'],
            'exported_file_hits': self.stats['exported_file_hits'],
            'api_query_hits': self.stats['api_query_hits'],
            'resolution_failures': self.stats['resolution_failures'],
            'cached_organizations': len(self._name_to_moid_cache),
            'exported_organizations': len(self._exported_orgs)
        }
    
    def preload_organizations_from_api(self) -> int:
        """
        Preload all organizations from the API into cache.
        
        Returns:
            Number of organizations loaded
        """
        if not self.api_client:
            logger.warning("Cannot preload organizations: no API client available")
            return 0
        
        try:
            logger.info("Preloading organizations from Intersight API...")
            orgs = self.api_client.query_objects('organization.Organization')
            
            loaded_count = 0
            for org in orgs:
                # Try different possible field names for Name and MOID
                name = org.get('Name') or org.get('name')
                moid = org.get('Moid') or org.get('moid') or org.get('ObjectMoid')
                
                logger.debug(f"Processing org: {org}")
                logger.debug(f"Extracted name: '{name}', moid: '{moid}'")
                
                if moid:  # Only require MOID, handle empty names
                    # Use "default" for organizations with empty/None names (fallback logic from export)
                    effective_name = name if name else "default"
                    logger.info(f"Loading organization: name='{effective_name}', moid='{moid}'")
                    
                    org_info = OrganizationInfo(
                        moid=moid,
                        name=effective_name,
                        object_type='organization.Organization',
                        source='api_query',
                        timestamp=datetime.now()
                    )
                    
                    self._name_to_moid_cache[effective_name] = org_info
                    self._moid_to_name_cache[moid] = org_info
                    loaded_count += 1
                    logger.info(f"Successfully cached organization '{effective_name}' -> '{moid}'")
                else:
                    logger.warning(f"Skipping organization with no MOID: {org}")
            
            logger.info(f"Preloaded {loaded_count} organizations from API")
            return loaded_count
            
        except Exception as e:
            logger.error(f"Failed to preload organizations from API: {e}")
            return 0