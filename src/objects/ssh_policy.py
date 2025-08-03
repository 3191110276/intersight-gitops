"""
SSH Policy object implementation.

This module implements the SshPolicy class for handling Cisco Intersight
ssh policy in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class SshPolicy(BasePolicy):
    """
    Implementation for Intersight SSH Policy objects.
    
    SSH Policy defines settings and configurations for the ssh policy.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "ssh.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "SSH Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing SSH Policy YAML files."""
        return "policies/ssh"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for SSH Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add policy-specific fields (will be populated from OpenAPI schema automatically)
        # The OpenAPI integration will extract the actual fields from the schema
        
        fields.update({
            # Common policy fields are already included from base class
            # Additional fields will be loaded from OpenAPI schema
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
