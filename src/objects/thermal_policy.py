"""
Thermal Policy object implementation.

This module implements the ThermalPolicy class for handling Cisco Intersight
thermal policy in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class ThermalPolicy(BasePolicy):
    """
    Implementation for Intersight Thermal Policy objects.
    
    Thermal Policy defines settings and configurations for the thermal policy.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "thermal.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Thermal Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing Thermal Policy YAML files."""
        return "policies/thermal"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Thermal Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add thermal policy-specific fields based on OpenAPI schema  
        fields.update({
            "fan_control_mode": FieldDefinition(
                name="fan_control_mode",
                field_type=FieldType.STRING,
                description="Sets the Fan Control Mode. High Power, Maximum Power and Acoustic modes are supported only on the Cisco UCS C-Series servers and on the X-Series Chassis.",
                enum_values=["Balanced", "LowPower", "HighPower", "MaximumPower", "Acoustic"],
                default_value="Balanced"
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
            "fan_control_mode": "Balanced"
        }
