"""
Domain Profile implementation.

This module implements the DomainProfile class for handling Cisco Intersight
Domain Profile objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_profile import BaseProfile
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class DomainProfile(BaseProfile):
    """
    Implementation for Intersight Domain Profile objects.
    
    A Domain Profile configures multiple Fabric Interconnects to form a 
    single management domain for centralized policy-based configuration 
    of the network, server, and storage resources.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.SwitchProfile"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Domain Profile"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing profile YAML files."""
        return "profiles/domain"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Domain Profile objects."""
        # Get common profile fields
        fields = self._get_common_profile_fields()
        
        # Add domain-specific fields
        fields.update({
            'ConfigChangeContext': FieldDefinition(
                name='ConfigChangeContext',
                field_type=FieldType.OBJECT,
                required=False,
                description='Context information for configuration changes'
            ),
            'ConfigChanges': FieldDefinition(
                name='ConfigChanges',
                field_type=FieldType.OBJECT,
                required=False,
                description='Details of configuration changes'
            ),
            'SwitchClusterProfile': FieldDefinition(
                name='SwitchClusterProfile',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Switch cluster profile associated with this domain profile',
                reference_type='fabric.SwitchClusterProfile',
                reference_field='Name'
            ),
            'Type': FieldDefinition(
                name='Type',
                field_type=FieldType.STRING,
                required=False,
                description='Defines the type of the profile',
                enum_values=['instance', 'template'],
                default_value='instance'
            )
        })
        
        return fields
    
    def _define_profile_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to Domain Profile."""
        return {
            DependencyDefinition(
                target_type='fabric.SwitchClusterProfile',
                dependency_type='references',
                required=False,
                description='Domain Profile can reference Switch Cluster Profile'
            )
        }
    
    def _get_example_profile_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this profile type."""
        return {
            'Type': 'instance'
        }