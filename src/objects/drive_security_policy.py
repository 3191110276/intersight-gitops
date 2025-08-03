"""
Drive Security Policy implementation.

This module implements the DriveSecurityPolicy class for handling Cisco Intersight
Drive Security Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class DriveSecurityPolicy(BasePolicy):
    """
    Implementation for Intersight Drive Security Policy objects.
    
    The drive security policy defines the configuration for a manual key or a 
    KMIP server, which can be applied to multiple servers. You can enable drive 
    security on the servers using either configuration.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "storage.DriveSecurityPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Drive Security Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/drive_security"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Drive Security Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add drive security-specific fields
        fields.update({
            'KeySetting': FieldDefinition(
                name='KeySetting',
                field_type=FieldType.OBJECT,
                required=False,
                description='Key details for supporting drive security'
            )
        })
        
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'KeySetting': {
                'KeyType': 'Manual',
                'ManualKey': {
                    'Passphrase': 'secure-passphrase-123',
                    'IsPassphraseSet': True
                }
            }
        }