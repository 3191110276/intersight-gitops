"""
Ethernet Network Group Policy implementation.

This module implements the EthernetNetworkGroupPolicy class for handling Cisco Intersight
Ethernet Network Group Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class EthernetNetworkGroupPolicy(BasePolicy):
    """
    Implementation for Intersight Ethernet Network Group Policy objects.
    
    The Ethernet Network Group policy specifies which VLANs will be allowed 
    on the server uplink ports.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.EthNetworkGroupPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Ethernet Network Group Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/ethernet_network_group"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Ethernet Network Group Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'VlanSettings': FieldDefinition(
                name='VlanSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='VLAN settings for the Ethernet Network Group Policy'
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