"""
Boot Order Policy object implementation.

This module implements the BootPolicy class for handling Cisco Intersight
boot order policies in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class BootPolicy(BasePolicy):
    """
    Implementation for Intersight Boot Order Policy objects.
    
    Boot policies define the boot order and boot mode settings for servers.
    They specify which devices the server should attempt to boot from and in what order.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "boot.PrecisionPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Boot Order Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing boot policy YAML files."""
        return "policies/boot"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Boot Order Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add boot policy-specific fields
        boot_fields = {
            'ConfiguredBootMode': FieldDefinition(
                name='ConfiguredBootMode',
                field_type=FieldType.STRING,
                required=False,
                description='Sets the BIOS boot mode. UEFI uses the GUID Partition Table (GPT) whereas Legacy mode uses the Master Boot Record (MBR) partitioning scheme',
                enum_values=['Legacy', 'Uefi']
            ),
            'EnforceUefiSecureBoot': FieldDefinition(
                name='EnforceUefiSecureBoot',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='If UEFI secure boot is enabled, the boot mode is set to UEFI by default. Secure boot enforces signature verification of boot software'
            ),
            'BootDevices': FieldDefinition(
                name='BootDevices',
                field_type=FieldType.ARRAY,
                required=False,
                description='An array of boot devices that the system will attempt to boot from in order'
            )
        }
        
        # Merge common and boot-specific fields
        fields.update(boot_fields)
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to boot policy."""
        return {
            'ConfiguredBootMode': 'Uefi',
            'EnforceUefiSecureBoot': True,
            'BootDevices': [
                {
                    'ObjectType': 'boot.LocalDisk',
                    'Name': 'LocalDisk',
                    'Enabled': True,
                    'Bootloader': {
                        'ObjectType': 'boot.Bootloader',
                        'Name': 'BOOTx64.EFI',
                        'Description': 'Default UEFI bootloader',
                        'Path': '\\EFI\\BOOT\\BOOTx64.EFI'
                    }
                },
                {
                    'ObjectType': 'boot.Pxe',
                    'Name': 'PXE',
                    'Enabled': True,
                    'InterfaceName': 'MGMT-A',
                    'IpType': 'IPv4',
                    'Slot': 'MLOM'
                },
                {
                    'ObjectType': 'boot.VirtualMedia',
                    'Name': 'VirtualMedia',
                    'Enabled': True,
                    'Subtype': 'kvm-mapped-dvd'
                }
            ]
        }
    
    def _process_references_for_export(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MOID references to name references for export.
        
        Boot policies may have references to other objects in the BootDevices array.
        
        Args:
            obj: Object dictionary with MOID references
            
        Returns:
            Object dictionary with name references
        """
        # First handle common policy references (Organization)
        processed = super()._process_references_for_export(obj)
        
        # Handle BootDevices references if needed
        # Boot devices typically don't have external references that need name resolution
        # but this is where we would add that logic if needed
        
        return processed
    
    def _process_references_for_import(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert name references to MOID references for import.
        
        Args:
            obj: Object dictionary with name references
            
        Returns:
            Object dictionary with MOID references
        """
        # First handle common policy references (Organization)
        processed = super()._process_references_for_import(obj)
        
        # Handle BootDevices references if needed
        # Boot devices typically don't have external references that need MOID resolution
        # but this is where we would add that logic if needed
        
        return processed