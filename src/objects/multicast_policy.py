"""
Multicast Policy implementation.

This module implements the MulticastPolicy class for handling Cisco Intersight
Multicast Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class MulticastPolicy(BasePolicy):
    """
    Implementation for Intersight Multicast Policy objects.
    
    The Multicast policy enables you to configure multicast settings 
    for fabric interconnects.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.MulticastPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Multicast Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/multicast"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Multicast Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'QuerierIpAddress': FieldDefinition(
                name='QuerierIpAddress',
                field_type=FieldType.STRING,
                required=False,
                description='IP address of the IGMP querier used for IGMP snooping'
            ),
            'QuerierState': FieldDefinition(
                name='QuerierState',
                field_type=FieldType.STRING,
                required=False,
                description='Administrative state of the IGMP querier',
                enum_values=['Disabled', 'Enabled'],
                default_value='Disabled'
            ),
            'SnoopingState': FieldDefinition(
                name='SnoopingState',
                field_type=FieldType.STRING,
                required=False,
                description='Administrative state of the IGMP snooping',
                enum_values=['Disabled', 'Enabled'],
                default_value='Enabled'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'QuerierIpAddress': '192.168.1.1',
            'QuerierState': 'Disabled',
            'SnoopingState': 'Enabled'
        }