"""
Device Connector Policy object implementation.

This module implements the DeviceConnectorPolicy class for handling Cisco Intersight
device connector policy in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class DeviceConnectorPolicy(BasePolicy):
    """
    Implementation for Intersight Device Connector Policy objects.
    
    Device Connector Policy defines settings and configurations for the device connector policy.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "deviceconnector.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Device Connector Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing Device Connector Policy YAML files."""
        return "policies/device_connector"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Device Connector Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add Device Connector Policy specific fields based on OpenAPI schema
        fields.update({
            "lockout_enabled": FieldDefinition(
                field_type=FieldType.BOOLEAN,
                description="Enables configuration lockout on the endpoint",
                required=False,
                default=True,
                api_field_name="LockoutEnabled"
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
            "lockout_enabled": True,
        }
