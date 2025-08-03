"""
System QoS Policy implementation.

This module implements the SystemQosPolicy class for handling Cisco Intersight
System QoS Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class SystemQosPolicy(BasePolicy):
    """
    Implementation for Intersight System QoS Policy objects.
    
    The System QoS policy defines the Quality of Service (QoS) system classes 
    for the data traffic on the fabric interconnects.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.SystemQosPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "System QoS Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/system_qos"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define all fields for System QoS Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'Classes': FieldDefinition(
                name='Classes',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of system QoS classes'
            )
        })
        return fields
    
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'Classes': [
                {
                    'AdminState': 'Enabled',
                    'BandwidthPercent': 0,
                    'Cos': 5,
                    'Mtu': 2240,
                    'MulticastOptimize': False,
                    'Name': 'Platinum',
                    'PacketDrop': False,
                    'Weight': 10
                },
                {
                    'AdminState': 'Enabled',
                    'BandwidthPercent': 0,
                    'Cos': 4,
                    'Mtu': 2240,
                    'MulticastOptimize': False,
                    'Name': 'Gold',
                    'PacketDrop': True,
                    'Weight': 9
                },
                {
                    'AdminState': 'Enabled',
                    'BandwidthPercent': 0,
                    'Cos': 2,
                    'Mtu': 2240,
                    'MulticastOptimize': False,
                    'Name': 'Silver',
                    'PacketDrop': True,
                    'Weight': 8
                },
                {
                    'AdminState': 'Enabled',
                    'BandwidthPercent': 0,
                    'Cos': 1,
                    'Mtu': 2240,
                    'MulticastOptimize': False,
                    'Name': 'Bronze',
                    'PacketDrop': True,
                    'Weight': 7
                },
                {
                    'AdminState': 'Enabled',
                    'BandwidthPercent': 0,
                    'Cos': 255,
                    'Mtu': 2240,
                    'MulticastOptimize': False,
                    'Name': 'Best Effort',
                    'PacketDrop': True,
                    'Weight': 5
                },
                {
                    'AdminState': 'Enabled',
                    'BandwidthPercent': 50,
                    'Cos': 3,
                    'Mtu': 2240,
                    'MulticastOptimize': False,
                    'Name': 'FC',
                    'PacketDrop': False,
                    'Weight': 5
                }
            ]
        }