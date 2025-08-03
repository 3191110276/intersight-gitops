"""
Switch Control Policy implementation.

This module implements the SwitchControlPolicy class for handling Cisco Intersight
Switch Control Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class SwitchControlPolicy(BasePolicy):
    """
    Implementation for Intersight Switch Control Policy objects.
    
    The Switch Control policy allows you to configure the switching 
    mode and MAC address table aging timeout for the fabric interconnects.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.SwitchControlPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Switch Control Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/switch_control"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define all fields for Switch Control Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'EthernetSwitchingMode': FieldDefinition(
                name='EthernetSwitchingMode',
                field_type=FieldType.STRING,
                required=False,
                description='Enable or Disable Ethernet End Host Switching Mode',
                enum_values=['end-host', 'switch'],
                default_value='end-host'
            ),
            'FcSwitchingMode': FieldDefinition(
                name='FcSwitchingMode',
                field_type=FieldType.STRING,
                required=False,
                description='Enable or Disable FC End Host Switching Mode',
                enum_values=['end-host', 'switch'],
                default_value='end-host'
            ),
            'MacAgingSettings': FieldDefinition(
                name='MacAgingSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='MAC address aging timeout settings'
            ),
            'ReservedVlanStartId': FieldDefinition(
                name='ReservedVlanStartId',
                field_type=FieldType.INTEGER,
                required=False,
                description='Starting VLAN ID for reserved VLAN range',
                default_value=3915,
                minimum=1,
                maximum=4093
            ),
            'VlanPortOptimizationEnabled': FieldDefinition(
                name='VlanPortOptimizationEnabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='To enable or disable the VLAN port optimization',
                default_value=False
            )
        })
        return fields
    
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'EthernetSwitchingMode': 'end-host',
            'FcSwitchingMode': 'end-host',
            'ReservedVlanStartId': 3915,
            'VlanPortOptimizationEnabled': False,
            'MacAgingSettings': {
                'MacAgingOption': 'Default',
                'MacAgingTime': 14500
            }
        }