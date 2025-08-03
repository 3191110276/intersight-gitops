"""
Ethernet QoS Policy implementation.

This module implements the EthernetQosPolicy class for handling Cisco Intersight
Ethernet QoS Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class EthernetQosPolicy(BasePolicy):
    """
    Implementation for Intersight Ethernet QoS Policy objects.
    
    The Ethernet QoS policy assigns system class or custom class to the 
    traffic on a vNIC.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.EthQosPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Ethernet QoS Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/ethernet_qos"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Ethernet QoS Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'Burst': FieldDefinition(
                name='Burst',
                field_type=FieldType.INTEGER,
                required=False,
                description='The burst traffic, in bytes, allowed on the vNIC',
                default_value=1024,
                minimum=1024,
                maximum=1000000
            ),
            'Cos': FieldDefinition(
                name='Cos',
                field_type=FieldType.INTEGER,
                required=False,
                description='Class of Service to be associated to the traffic on the virtual interface',
                default_value=0,
                minimum=0,
                maximum=7
            ),
            'Mtu': FieldDefinition(
                name='Mtu',
                field_type=FieldType.INTEGER,
                required=False,
                description='The Maximum Transmission Unit (MTU) or packet size that the virtual interface accepts',
                default_value=1500,
                minimum=1500,
                maximum=9000
            ),
            'Priority': FieldDefinition(
                name='Priority',
                field_type=FieldType.STRING,
                required=False,
                description='The priortiy matching the System QoS specified in the fabric profile',
                enum_values=['Best Effort', 'FC', 'Platinum', 'Gold', 'Silver', 'Bronze'],
                default_value='Best Effort'
            ),
            'RateLimit': FieldDefinition(
                name='RateLimit',
                field_type=FieldType.INTEGER,
                required=False,
                description='The value in Mbps to use for limiting the data rate on the virtual interface',
                default_value=0,
                minimum=0,
                maximum=40000
            ),
            'TrustHostCos': FieldDefinition(
                name='TrustHostCos',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables usage of the Class of Service provided by the operating system',
                default_value=False
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'Burst': 1024,
            'Cos': 0,
            'Mtu': 1500,
            'Priority': 'Best Effort',
            'RateLimit': 0,
            'TrustHostCos': False
        }