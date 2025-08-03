"""
Domain Template implementation.

This module implements the DomainTemplate class for handling Cisco Intersight
Domain Template objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_template import BaseTemplate
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class DomainTemplate(BaseTemplate):
    """
    Implementation for Intersight Domain Template objects.
    
    Domain Templates provide a template definition for domain profiles 
    that can be used to standardize fabric interconnect domain configurations.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.SwitchProfileTemplate"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Domain Template"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing template YAML files."""
        return "templates/domain"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Domain Template objects."""
        # Get common template fields
        fields = self._get_common_template_fields()
        
        # Add domain template-specific fields
        fields.update({
            'SwitchType': FieldDefinition(
                name='SwitchType',
                field_type=FieldType.STRING,
                required=False,
                description='The type of switch for the domain template',
                enum_values=['FabricInterconnect'],
                default_value='FabricInterconnect'
            )
        })
        
        return fields
    
    def _define_template_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to Domain Template."""
        return set()
    
    def _get_example_template_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this template type."""
        return {
            'SwitchType': 'FabricInterconnect'
        }