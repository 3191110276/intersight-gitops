"""
Fibre Channel Network Policy implementation.

This module implements the FibreChannelNetworkPolicy class for handling Cisco Intersight
Fibre Channel Network Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class FibreChannelNetworkPolicy(BasePolicy):
    """
    Implementation for Intersight Fibre Channel Network Policy objects.
    
    The Fibre Channel Network policy enables you to create a Fibre Channel 
    network, configure VLANs and VSANs.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.FcNetworkPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Fibre Channel Network Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/fibre_channel_network"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Fibre Channel Network Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'EnableTrunking': FieldDefinition(
                name='EnableTrunking',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enable or disable Trunking on all of configured FC uplink ports',
                default_value=False
            ),
            'VsanSettings': FieldDefinition(
                name='VsanSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='VSAN settings for the Fibre Channel Network Policy'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'EnableTrunking': False,
            'VsanSettings': {
                'DefaultVlan': 4048,
                'Id': 100
            }
        }