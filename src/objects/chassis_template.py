"""
Chassis Template implementation.

This module implements the ChassisTemplate class for handling Cisco Intersight
Chassis Template objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_template import BaseTemplate
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class ChassisTemplate(BaseTemplate):
    """
    Implementation for Intersight Chassis Template objects.
    
    Chassis Templates provide a template definition for chassis profiles 
    that can be used to standardize chassis configurations.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "chassis.ProfileTemplate"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Chassis Template"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing template YAML files."""
        return "templates/chassis"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Chassis Template objects."""
        # Get common template fields
        fields = self._get_common_template_fields()
        
        # Add chassis template-specific fields
        fields.update({
            'TargetPlatform': FieldDefinition(
                name='TargetPlatform',
                field_type=FieldType.STRING,
                required=False,
                description='The platform for which the chassis profile template is applicable',
                enum_values=['FIAttached'],
                default_value='FIAttached'
            )
        })
        
        return fields
    
    def _define_template_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to Chassis Template."""
        return set()
    
    def _get_example_template_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this template type."""
        return {
            'TargetPlatform': 'FIAttached'
        }