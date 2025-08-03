"""
iSCSI Adapter Policy implementation.

This module implements the IscsiAdapterPolicy class for handling Cisco Intersight
iSCSI Adapter Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class IscsiAdapterPolicy(BasePolicy):
    """
    Implementation for Intersight iSCSI Adapter Policy objects.
    
    The iSCSI Adapter policy governs the host-side behavior of the adapter, 
    including how the adapter handles traffic on the iSCSI interface.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.IscsiAdapterPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "iSCSI Adapter Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/iscsi_adapter"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to iSCSI Adapter Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'ConnectionTimeOut': FieldDefinition(
                name='ConnectionTimeOut',
                field_type=FieldType.INTEGER,
                required=False,
                description='The number of seconds to wait until Cisco UCS assumes that the initial login has failed and the iSCSI adapter is unavailable',
                default_value=15,
                minimum=0,
                maximum=255
            ),
            'DhcpTimeout': FieldDefinition(
                name='DhcpTimeout',
                field_type=FieldType.INTEGER,
                required=False,
                description='The number of seconds to wait before the initiator assumes that the DHCP server is unavailable',
                default_value=60,
                minimum=60,
                maximum=300
            ),
            'LunBusyRetryCount': FieldDefinition(
                name='LunBusyRetryCount',
                field_type=FieldType.INTEGER,
                required=False,
                description='The number of times to retry the connection in case of a failure during iSCSI LUN discovery',
                default_value=15,
                minimum=0,
                maximum=60
            ),
            'TcpConnectionTimeOut': FieldDefinition(
                name='TcpConnectionTimeOut',
                field_type=FieldType.INTEGER,
                required=False,
                description='The number of seconds to wait before the system decides that the TCP connection is lost',
                default_value=15,
                minimum=1,
                maximum=60
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'ConnectionTimeOut': 15,
            'DhcpTimeout': 60,
            'LunBusyRetryCount': 15,
            'TcpConnectionTimeOut': 15
        }