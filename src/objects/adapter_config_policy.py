"""
Adapter Configuration Policy implementation.

This module implements the AdapterConfigPolicy class for handling Cisco Intersight
Adapter Configuration Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class AdapterConfigPolicy(BasePolicy):
    """
    Implementation for Intersight Adapter Configuration Policy objects.
    
    An Adapter Configuration Policy configures the Ethernet and Fibre-Channel
    settings for the VIC adapter.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "adapter.ConfigPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Adapter Configuration Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/adapter_config"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Adapter Configuration Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add adapter configuration-specific fields
        fields.update({
            'Settings': FieldDefinition(
                name='Settings',
                field_type=FieldType.ARRAY,
                required=False,
                description='Configuration for all the adapters available in the server'
            )
        })
        
        return fields
    
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'Settings': [
                {
                    'SlotId': 'MLOM',
                    'EthSettings': {
                        'LldpEnabled': True
                    },
                    'FcSettings': {
                        'FipEnabled': False
                    }
                }
            ]
        }