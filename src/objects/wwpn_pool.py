"""
WWPN Pool implementation.

This module implements the WwpnPool class for handling Cisco Intersight
WWPN Pool objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_pool import BasePool
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class WwpnPool(BasePool):
    """
    Implementation for Intersight WWPN Pool objects.
    
    WWPN Pool provides identities to be assigned to Fibre Channel interfaces.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fcpool.Pool"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "WWPN Pool"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing pool YAML files."""
        return "pools/wwpn"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for WWPN Pool objects."""
        # Get common pool fields
        fields = self._get_common_pool_fields()
        
        # Add WWPN-specific fields
        fields.update({
            'IdBlocks': FieldDefinition(
                name='IdBlocks',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of Identities in this pool'
            ),
            'PoolPurpose': FieldDefinition(
                name='PoolPurpose',
                field_type=FieldType.STRING,
                required=False,
                description='Purpose of this pool, whether it is for WWPN or WWNN',
                enum_values=['WWPN', 'WWNN'],
                default_value='WWPN'
            )
        })
        
        return fields
    
    def _define_pool_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to WWPN Pool."""
        return set()
    
    def _get_example_pool_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this pool type."""
        return {
            'PoolPurpose': 'WWPN',
            'IdBlocks': [
                {
                    'From': '20:00:00:25:B5:00:00:00',
                    'To': '20:00:00:25:B5:00:00:FF',
                    'Size': 256
                }
            ]
        }