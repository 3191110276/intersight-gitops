"""
FC Zone Policy implementation.

This module implements the FcZonePolicy class for handling Cisco Intersight
FC Zone Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class FcZonePolicy(BasePolicy):
    """
    Implementation for Intersight FC Zone Policy objects.
    
    The FC Zone policy allows you to configure Fibre Channel zones for 
    the vHBAs of the servers that are associated with a server profile.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.FcZonePolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "FC Zone Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/fc_zone"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to FC Zone Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'FcTargetZoningType': FieldDefinition(
                name='FcTargetZoningType',
                field_type=FieldType.STRING,
                required=False,
                description='Type of FC zoning (SIST, SIMT, or None)'
            ),
            'FcTargetMembers': FieldDefinition(
                name='FcTargetMembers',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of FC target members for the zone policy'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'FcTargetMembers': [
                {
                    'Name': 'target-1',
                    'Wwpn': '20:00:00:25:B5:00:01:00'
                }
            ]
        }