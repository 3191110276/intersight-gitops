"""
VLAN Policy implementation.

This module implements the VlanPolicy class for handling Cisco Intersight
VLAN Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class VlanPolicy(BasePolicy):
    """
    Implementation for Intersight VLAN Policy objects.
    
    The VLAN policy allows you to configure VLANs and multicast policies 
    for the fabric interconnects.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.EthNetworkPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "VLAN Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/vlan"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields for VLAN Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'VlanSettings': FieldDefinition(
                name='VlanSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='VLAN settings configuration'
            )
        })
        return fields
    
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'VlanSettings': {
                'NativeVlan': 1,
                'AllowedVlans': '100-200,300'
            }
        }