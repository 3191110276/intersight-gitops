"""
SAN Connectivity Policy implementation.

This module implements the SanConnectivityPolicy class for handling Cisco Intersight
SAN Connectivity Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class SanConnectivityPolicy(BasePolicy):
    """
    Implementation for Intersight SAN Connectivity Policy objects.
    
    The SAN Connectivity policy defines the storage connectivity requirements 
    for servers. This policy allows you to configure vHBAs for the server.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.SanConnectivityPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "SAN Connectivity Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/san_connectivity"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to SAN Connectivity Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'PlacementMode': FieldDefinition(
                name='PlacementMode',
                field_type=FieldType.STRING,
                required=False,
                description='The mode used for placement of vHBAs on network adapters',
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
            ),
            'WwnnAddressType': FieldDefinition(
                name='WwnnAddressType',
                field_type=FieldType.STRING,
                required=False,
                description='Type of allocation selected to assign a WWNN address for the server associated with the SAN Connectivity Policy',
                enum_values=['POOL', 'STATIC'],
                default_value='POOL'
            ),
            'WwnnPool': FieldDefinition(
                name='WwnnPool',
                field_type=FieldType.REFERENCE,
                required=False,
                description='WWNN pool to be associated with SAN Connectivity Policy',
                reference_type='fcpool.Pool',
                reference_field='Name'
            ),
            'WwnnStatic': FieldDefinition(
                name='WwnnStatic',
                field_type=FieldType.STRING,
                required=False,
                description='The WWNN address for the server node must be in hexadecimal format xx:xx:xx:xx:xx:xx:xx:xx'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'PlacementMode': 'custom',
            'TargetPlatform': 'FIAttached',
            'WwnnAddressType': 'POOL'
        }