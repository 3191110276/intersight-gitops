"""
MACsec Policy implementation.

This module implements the MacsecPolicy class for handling Cisco Intersight
MACsec Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class MacsecPolicy(BasePolicy):
    """
    Implementation for Intersight MACsec Policy objects.
    
    The MACsec policy enables you to configure MACsec (Media Access Control Security) 
    settings for encryption of Ethernet frames at the data link layer.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.SwitchControlPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "MACsec Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/macsec"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to MACsec Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'MacsecSettings': FieldDefinition(
                name='MacsecSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='MACsec configuration settings'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'MacsecSettings': {
                'Enabled': True,
                'CipherSuite': 'GCM-AES-128'
            }
        }