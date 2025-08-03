"""
Storage Policy implementation.

This module implements the StoragePolicy class for handling Cisco Intersight
Storage Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class StoragePolicy(BasePolicy):
    """
    Implementation for Intersight Storage Policy objects.
    
    The Storage policy allows creation of RAID groups using existing disk group 
    policies and virtual drives on the drive groups. The user has options to 
    move all unused disks to JBOD or Unconfigured good state.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "storage.StoragePolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Storage Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/storage"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define all fields for Storage Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'DefaultDriveMode': FieldDefinition(
                name='DefaultDriveMode',
                field_type=FieldType.STRING,
                required=False,
                description='All the drives that are not used in this policy, will move to the selected state',
                enum_values=['UnconfiguredGood', 'Jbod'],
                default_value='UnconfiguredGood'
            ),
            'DiskGroupPolicies': FieldDefinition(
                name='DiskGroupPolicies',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of disk group policies to be configured'
            ),
            'DriveGroup': FieldDefinition(
                name='DriveGroup',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of drive groups for RAID configuration'
            ),
            'M2VirtualDrive': FieldDefinition(
                name='M2VirtualDrive',
                field_type=FieldType.OBJECT,
                required=False,
                description='Virtual drive configuration for M.2 drives'
            ),
            'RaidController': FieldDefinition(
                name='RaidController',
                field_type=FieldType.OBJECT,
                required=False,
                description='RAID controller configuration'
            ),
            'RetainPolicyVirtualDrives': FieldDefinition(
                name='RetainPolicyVirtualDrives',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Retains the virtual drives defined in policy as it is where it has not been modified by user',
                default_value=True
            ),
            'UnusedDisksState': FieldDefinition(
                name='UnusedDisksState',
                field_type=FieldType.STRING,
                required=False,
                description='State to which drives, not used in this policy, are set',
                enum_values=['UnconfiguredGood', 'Jbod', 'NoChange'],
                default_value='NoChange'
            ),
            'UseJbodForVdCreation': FieldDefinition(
                name='UseJbodForVdCreation',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Disks would be moved to JBOD state first and then Virtual Drives would be created on the drives',
                default_value=False
            ),
            'VirtualDrives': FieldDefinition(
                name='VirtualDrives',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of virtual drives to be configured'
            )
        })
        return fields
    
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'DefaultDriveMode': 'UnconfiguredGood',
            'RetainPolicyVirtualDrives': True,
            'UnusedDisksState': 'UnconfiguredGood',
            'UseJbodForVdCreation': False,
            'VirtualDrives': [
                {
                    'Name': 'VD0',
                    'Size': 100,
                    'ExpandToAvailable': False,
                    'BootDrive': True,
                    'VirtualDrivePolicy': {
                        'AccessPolicy': 'Default',
                        'DriveCache': 'Default',
                        'ReadPolicy': 'Default',
                        'StripSize': 64,
                        'WritePolicy': 'Default'
                    }
                }
            ]
        }