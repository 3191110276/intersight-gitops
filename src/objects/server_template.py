"""
Server Template implementation.

This module implements the ServerTemplate class for handling Cisco Intersight
Server Template objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_template import BaseTemplate
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class ServerTemplate(BaseTemplate):
    """
    Implementation for Intersight Server Template objects.
    
    Server Templates provide a template definition for server profiles 
    that can be used to standardize server configurations.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "server.ProfileTemplate"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Server Template"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing template YAML files."""
        return "templates/server"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Server Template objects."""
        # Get common template fields
        fields = self._get_common_template_fields()
        
        # Add server template-specific fields
        fields.update({
            'TargetPlatform': FieldDefinition(
                name='TargetPlatform',
                field_type=FieldType.STRING,
                required=False,
                description='The platform for which the server profile template is applicable',
                enum_values=['Standalone', 'FIAttached'],
                default_value='FIAttached'
            ),
            'UuidAddressType': FieldDefinition(
                name='UuidAddressType',
                field_type=FieldType.STRING,
                required=False,
                description='Definition of how UUID address is allocated to the server',
                enum_values=['NONE', 'POOL'],
                default_value='NONE'
            ),
            'UuidPool': FieldDefinition(
                name='UuidPool',
                field_type=FieldType.REFERENCE,
                required=False,
                description='UUID pool associated with this server template',
                reference_type='uuidpool.Pool', 
                reference_field='Name'
            )
        })
        
        return fields
    
    def _define_template_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to Server Template."""
        return {
            DependencyDefinition(
                target_type='uuidpool.Pool',
                dependency_type='references',
                required=False,
                description='Server Template can reference UUID Pool'
            )
        }
    
    def _get_example_template_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this template type."""
        return {
            'TargetPlatform': 'FIAttached',
            'UuidAddressType': 'NONE'
        }