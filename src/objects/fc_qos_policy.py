"""
Fibre Channel QoS Policy implementation.

This module implements the FcQosPolicy class for handling Cisco Intersight
Fibre Channel QoS Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class FcQosPolicy(BasePolicy):
    """
    Implementation for Intersight Fibre Channel QoS Policy objects.
    
    The Fibre Channel QoS policy assigns system class or custom class to the 
    traffic on a vHBA.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.FcQosPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Fibre Channel QoS Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/fc_qos"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields for Fibre Channel QoS Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'MaxDataFieldSize': FieldDefinition(
                name='MaxDataFieldSize',
                field_type=FieldType.INTEGER,
                required=False,
                description='The maximum size of the Fibre Channel frame payload bytes'
            ),
            'Priority': FieldDefinition(
                name='Priority',
                field_type=FieldType.STRING,
                required=False,
                description='The priority for the traffic on the virtual interface',
                enum_values=['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze']
            ),
            'RateLimit': FieldDefinition(
                name='RateLimit',
                field_type=FieldType.INTEGER,
                required=False,
                description='The value in Mbps to use for limiting the data rate on the virtual interface'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'MaxDataFieldSize': 2112,
            'Priority': 'FC',
            'RateLimit': 0
        }