"""
iSCSI Boot Policy implementation.

This module implements the IscsiBootPolicy class for handling Cisco Intersight
iSCSI Boot Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class IscsiBootPolicy(BasePolicy):
    """
    Implementation for Intersight iSCSI Boot Policy objects.
    
    The iSCSI Boot policy allows configuration of the boot target details, 
    CHAP authentication, and other iSCSI parameters for the iSCSI vNIC.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.IscsiBootPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "iSCSI Boot Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/iscsi_boot"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to iSCSI Boot Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'AutoTargetvendorName': FieldDefinition(
                name='AutoTargetvendorName',
                field_type=FieldType.STRING,
                required=False,
                description='Auto target interface that is represented via the Initiator name or the DHCP vendor ID'
            ),
            'Chap': FieldDefinition(
                name='Chap',
                field_type=FieldType.OBJECT,
                required=False,
                description='Challenge Handshake Authentication Protocol (CHAP) settings'
            ),
            'InitiatorIpPool': FieldDefinition(
                name='InitiatorIpPool',
                field_type=FieldType.REFERENCE,
                required=False,
                description='IP pool to be associated with the iSCSI vNIC',
                reference_type='ippool.Pool',
                reference_field='Name'
            ),
            'InitiatorIpSource': FieldDefinition(
                name='InitiatorIpSource',
                field_type=FieldType.STRING,
                required=False,
                description='Source Type of Initiator IP Address - DHCP/Static/Pool',
                enum_values=['DHCP', 'Static', 'Pool'],
                default_value='DHCP'
            ),
            'InitiatorStaticIpV4Address': FieldDefinition(
                name='InitiatorStaticIpV4Address',
                field_type=FieldType.STRING,
                required=False,
                description='Static IPv4 address for iSCSI boot interface'
            ),
            'InitiatorStaticIpV4Config': FieldDefinition(
                name='InitiatorStaticIpV4Config',
                field_type=FieldType.OBJECT,
                required=False,
                description='Static IP settings for the iSCSI boot interface'
            ),
            'InitiatorStaticIpV6Address': FieldDefinition(
                name='InitiatorStaticIpV6Address',
                field_type=FieldType.STRING,
                required=False,
                description='Static IPv6 address for iSCSI boot interface'
            ),
            'InitiatorStaticIpV6Config': FieldDefinition(
                name='InitiatorStaticIpV6Config',
                field_type=FieldType.OBJECT,
                required=False,
                description='Static IPv6 settings for the iSCSI boot interface'
            ),
            'IscsiIpType': FieldDefinition(
                name='IscsiIpType',
                field_type=FieldType.STRING,
                required=False,
                description='IP type to be used for iSCSI communication',
                enum_values=['IPv4', 'IPv6'],
                default_value='IPv4'
            ),
            'IscsiAdapterPolicy': FieldDefinition(
                name='IscsiAdapterPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Reference to associated iSCSI Adapter Policy',
                reference_type='vnic.IscsiAdapterPolicy',
                reference_field='Name'
            ),
            'MutualChap': FieldDefinition(
                name='MutualChap',
                field_type=FieldType.OBJECT,
                required=False,
                description='Mutual Challenge Handshake Authentication Protocol (CHAP) settings'
            ),
            'PrimaryTargetPolicy': FieldDefinition(
                name='PrimaryTargetPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='The primary target policy associated with the iSCSI boot policy',
                reference_type='vnic.IscsiStaticTargetPolicy',
                reference_field='Name'
            ),
            'SecondaryTargetPolicy': FieldDefinition(
                name='SecondaryTargetPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='The secondary target policy associated with the iSCSI boot policy',
                reference_type='vnic.IscsiStaticTargetPolicy',
                reference_field='Name'
            ),
            'TargetSourceType': FieldDefinition(
                name='TargetSourceType',
                field_type=FieldType.STRING,
                required=False,
                description='Source Type of Targets that can be assigned to the iSCSI boot policy',
                enum_values=['Static', 'Auto'],
                default_value='Static'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'TargetSourceType': 'Static',
            'InitiatorIpSource': 'Static',
            'IscsiIpType': 'IPv4',
            'AutoTargetvendorName': '',
            'Chap': {
                'ClassId': 'vnic.IscsiAuthProfile',
                'ObjectType': 'vnic.IscsiAuthProfile',
                'IsPasswordSet': False
            },
            'InitiatorStaticIpV4Address': '192.168.1.100',
            'InitiatorStaticIpV4Config': {
                'ClassId': 'ippool.IpV4Config',
                'ObjectType': 'ippool.IpV4Config',
                'Gateway': '192.168.1.1',
                'Netmask': '255.255.255.0',
                'PrimaryDns': '8.8.8.8',
                'SecondaryDns': '8.8.4.4'
            }
        }