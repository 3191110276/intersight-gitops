"""
Scrub Policy implementation.

This module implements the ScrubPolicy class for handling Cisco Intersight
Scrub Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class ScrubPolicy(BasePolicy):
    """
    Implementation for Intersight Scrub Policy objects.
    
    The Scrub policy allows you to securely erase the data on disk drives and 
    on BIOS settings when a server is unassociated from a server profile or 
    when a blade server is removed from a chassis.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "compute.ScrubPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Scrub Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/scrub"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Scrub Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'ScrubTargets': FieldDefinition(
                name='ScrubTargets',
                field_type=FieldType.ARRAY,
                required=False,
                description='Target components to be cleared during scrub. Values: Disk, BIOS',
                default_value=[]
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'ScrubTargets': ['Disk']
        }