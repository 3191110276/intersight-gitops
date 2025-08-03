"""
LAN Connectivity Policy implementation.

This module implements the LanConnectivityPolicy class for handling Cisco Intersight
LAN Connectivity Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class LanConnectivityPolicy(BasePolicy):
    """
    Implementation for Intersight LAN Connectivity Policy objects.
    
    The LAN Connectivity policy defines the network connectivity requirements 
    for servers. This policy allows you to configure vNICs, iscsi vNICs and 
    fcoe vNICs for the server.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.LanConnectivityPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "LAN Connectivity Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/lan_connectivity"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to LAN Connectivity Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'AzureQosEnabled': FieldDefinition(
                name='AzureQosEnabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables Azure Stack Host QOS on an adapter',
                default_value=False
            ),
            'IqnAllocationType': FieldDefinition(
                name='IqnAllocationType',
                field_type=FieldType.STRING,
                required=False,
                description='Allocation Type of iSCSI Qualified Name',
                enum_values=['None', 'Sequential', 'Pool'],
                default_value='None'
            ),
            'IqnPool': FieldDefinition(
                name='IqnPool',
                field_type=FieldType.REFERENCE,
                required=False,
                description='IQN pool to be associated with LAN Connectivity Policy',
                reference_type='iqnpool.Pool',
                reference_field='Name'
            ),
            'IqnStaticIdentifier': FieldDefinition(
                name='IqnStaticIdentifier',
                field_type=FieldType.STRING,
                required=False,
                description='User provided static iSCSI Qualified Name (IQN) for use as initiator identifiers by iSCSI vNICs'
            ),
            'PlacementMode': FieldDefinition(
                name='PlacementMode',
                field_type=FieldType.STRING,
                required=False,
                description='The mode used for placement of vNICs on network adapters',
                enum_values=['custom', 'auto'],
                default_value='custom'
            ),
            'TargetPlatform': FieldDefinition(
                name='TargetPlatform',
                field_type=FieldType.STRING,
                required=False,
                description='The platform for which the server profile is applicable',
                enum_values=['Standalone', 'FIAttached'],
                default_value='FIAttached'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'AzureQosEnabled': False,
            'IqnAllocationType': 'None',
            'PlacementMode': 'custom',
            'TargetPlatform': 'FIAttached'
        }