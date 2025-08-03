"""
Syslog Policy object implementation.

This module implements the SyslogPolicy class for handling Cisco Intersight
syslog policy in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class SyslogPolicy(BasePolicy):
    """
    Implementation for Intersight Syslog Policy objects.
    
    Syslog Policy defines settings and configurations for the syslog policy.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "syslog.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Syslog Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing Syslog Policy YAML files."""
        return "policies/syslog"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Syslog Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add syslog policy-specific fields
        fields.update({
            'LocalClients': FieldDefinition(
                name='LocalClients',
                field_type=FieldType.ARRAY,
                required=False,
                description='Array of local syslog clients'
            ),
            'RemoteClients': FieldDefinition(
                name='RemoteClients',
                field_type=FieldType.ARRAY,
                required=False,
                description='Array of remote syslog clients'
            ),
        })
        
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this policy type.
        
        Returns:
            Dictionary of example field values
        """
        return {
            # Example values will be populated based on OpenAPI schema
            # This is used for documentation generation
        }
