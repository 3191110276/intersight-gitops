"""
Port Policy implementation.

This module implements the PortPolicy class for handling Cisco Intersight
Port Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class PortPolicy(BasePolicy):
    """
    Implementation for Intersight Port Policy objects.
    
    The Port policy enables you to configure the physical ports on the 
    fabric interconnects including port roles, port types, and breakout settings.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.PortPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Port Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/port"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Port Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'DeviceModel': FieldDefinition(
                name='DeviceModel',
                field_type=FieldType.STRING,
                required=False,
                description='Model of the switch/fabric-interconnect for which the port policy is defined'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'DeviceModel': 'UCS-FI-6454'
        }