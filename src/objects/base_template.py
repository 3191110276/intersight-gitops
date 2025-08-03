"""
Base Template class for all Intersight template objects.

This module provides the base Template class that all specific template 
implementations inherit from. It handles common template attributes and
provides a foundation for template-specific implementations.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Set
from abc import abstractmethod

from src.core.object_type import ObjectType, FieldDefinition, FieldType, DependencyDefinition, ValidationLevel

logger = logging.getLogger(__name__)


class BaseTemplate(ObjectType):
    """
    Base class for all Intersight template objects.
    
    This class provides common functionality for all template types including:
    - Organization field handling
    - Common template attributes (Name, Description, Tags)
    - Template-specific validation and transformation
    """
    
    def __init__(self, api_client=None, openapi_schema=None, validation_level=ValidationLevel.STRICT):
        """Initialize the base template object."""
        super().__init__(api_client, openapi_schema, validation_level)
    
    @property
    def folder_path(self) -> str:
        """Return the base folder path for templates."""
        return "templates"
    
    def _get_common_template_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get common fields that all templates share.
        
        Returns:
            Dictionary of common template field definitions
        """
        return {
            'Name': FieldDefinition(
                name='Name',
                field_type=FieldType.STRING,
                required=True,
                description='Name of the template',
                min_length=1,
                max_length=64,
                pattern=r'^[a-zA-Z0-9_.:-]{1,64}$'
            ),
            'Description': FieldDefinition(
                name='Description',
                field_type=FieldType.STRING,
                required=False,
                description='Description of the template'
            ),
            'Organization': FieldDefinition(
                name='Organization',
                field_type=FieldType.REFERENCE,
                required=True,
                description='A reference to a organizationOrganization resource',
                reference_type='organization.Organization',
                reference_field='Name'
            ),
            'ObjectType': FieldDefinition(
                name='ObjectType',
                field_type=FieldType.STRING,
                required=True,
                description='The concrete type of this complex type'
            ),
            'Tags': FieldDefinition(
                name='Tags',
                field_type=FieldType.ARRAY,
                required=False,
                description='An array of tags, which allow to add key, value meta-data to managed objects'
            )
        }
    
    def _define_dependencies(self) -> Set[DependencyDefinition]:
        """Define common dependencies for templates."""
        base_deps = {
            DependencyDefinition(
                target_type='organization.Organization',
                dependency_type='references',
                required=True,
                description='Templates must belong to an organization'
            )
        }
        # Add template-specific dependencies
        base_deps.update(self._define_template_specific_dependencies())
        return base_deps
    
    def get_organization_name(self, obj: Dict[str, Any]) -> Optional[str]:
        """
        Extract organization name from a template object.
        Organization can be either a string or an object.
        
        Args:
            obj: Template object dictionary
            
        Returns:
            Organization name or None if not found
        """
        org_ref = obj.get('Organization')
        
        # Handle organization as simple string (new format)
        if isinstance(org_ref, str):
            return org_ref
        
        # Handle organization as object (legacy format)
        if isinstance(org_ref, dict):
            return org_ref.get('Name') or org_ref.get('Moid')
        
        return None
    
    def generate_filename(self, obj: Dict[str, Any], organization_name: str = None) -> str:
        """
        Generate a filename for a template object.
        
        Templates are named with organization prefix: {org_name}_{template_name}.yaml
        
        Args:
            obj: The template object dictionary
            organization_name: Organization name (extracted if not provided)
            
        Returns:
            Generated filename string
        """
        name = obj.get('Name', 'unnamed')
        # Sanitize filename
        name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        name = name.replace(' ', '_')
        
        # Get or extract organization name
        if not organization_name:
            organization_name = self.get_organization_name(obj) or 'default'
        
        # Sanitize organization name
        org_name = "".join(c for c in organization_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        org_name = org_name.replace(' ', '_')
        
        return f"{org_name}_{name}.yaml"
    
    @abstractmethod
    def _define_template_specific_dependencies(self) -> Set[DependencyDefinition]:
        """
        Define dependencies specific to this template type.
        
        Returns:
            Set of template-specific dependency definitions
        """
        pass
    
    @abstractmethod
    def _get_example_template_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this template type.
        
        Returns:
            Dictionary of example field values
        """
        pass