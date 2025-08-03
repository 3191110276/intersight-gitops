"""
Ethernet Network Control Policy implementation.

This module implements the EthernetNetworkControlPolicy class for handling Cisco Intersight
Ethernet Network Control Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class EthernetNetworkControlPolicy(BasePolicy):
    """
    Implementation for Intersight Ethernet Network Control Policy objects.
    
    The Ethernet Network Control policy governs the Ethernet network control 
    settings for the network adapters.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.EthNetworkControlPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Ethernet Network Control Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/ethernet_network_control"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Ethernet Network Control Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'CdpEnabled': FieldDefinition(
                name='CdpEnabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables the CDP on an interface',
                default_value=False
            ),
            'ForgeMac': FieldDefinition(
                name='ForgeMac',
                field_type=FieldType.STRING,
                required=False,
                description='Determines if the MAC forging is allowed or denied on an interface',
                enum_values=['allow', 'deny'],
                default_value='allow'
            ),
            'LldpSettings': FieldDefinition(
                name='LldpSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='LLDP settings for the Ethernet ports'
            ),
            'MacRegistrationMode': FieldDefinition(
                name='MacRegistrationMode',
                field_type=FieldType.STRING,
                required=False,
                description='Mac registration mode for the Ethernet ports',
                enum_values=['nativeVlanOnly', 'allVlans'],
                default_value='nativeVlanOnly'
            ),
            'UplinkFailAction': FieldDefinition(
                name='UplinkFailAction',
                field_type=FieldType.STRING,
                required=False,
                description='Uplink Fail Action to take when uplink goes down',
                enum_values=['linkDown', 'warning'],
                default_value='linkDown'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'CdpEnabled': False,
            'ForgeMac': 'allow',
            'MacRegistrationMode': 'nativeVlanOnly',
            'UplinkFailAction': 'linkDown',
            'LldpSettings': {
                'ReceiveEnabled': True,
                'TransmitEnabled': True
            }
        }