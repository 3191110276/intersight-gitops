"""
iSCSI Static Target Policy implementation.

This module implements the IscsiStaticTargetPolicy class for handling Cisco Intersight
iSCSI Static Target Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class IscsiStaticTargetPolicy(BasePolicy):
    """
    Implementation for Intersight iSCSI Static Target Policy objects.
    
    The iSCSI Static Target policy allows configuration of static iSCSI targets 
    that can be used by iSCSI boot policies.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.IscsiStaticTargetPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "iSCSI Static Target Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/iscsi_static_target"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to iSCSI Static Target Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'IpAddress': FieldDefinition(
                name='IpAddress',
                field_type=FieldType.STRING,
                required=False,
                description='The IPv4 address assigned to the iSCSI target'
            ),
            'Lun': FieldDefinition(
                name='Lun',
                field_type=FieldType.OBJECT,
                required=False,
                description='LUN information for the iSCSI target'
            ),
            'Port': FieldDefinition(
                name='Port',
                field_type=FieldType.INTEGER,
                required=False,
                description='The port associated with the iSCSI target',
                default_value=3260,
                minimum=1,
                maximum=65535
            ),
            'TargetName': FieldDefinition(
                name='TargetName',
                field_type=FieldType.STRING,
                required=False,
                description='Qualified Name (IQN) or Extended Unique Identifier (EUI) name of the iSCSI target'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'IpAddress': '192.168.1.10',
            'Port': 3260,
            'TargetName': 'iqn.2010-11.com.example:storage.target01',
            'Lun': {
                'Bootable': True,
                'LunId': 0
            }
        }