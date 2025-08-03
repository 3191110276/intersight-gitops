"""
VSAN Policy implementation.

This module implements the VsanPolicy class for handling Cisco Intersight
VSAN Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class VsanPolicy(BasePolicy):
    """
    Implementation for Intersight VSAN Policy objects.
    
    The VSAN policy allows you to configure VSANs (Virtual Storage Area Networks) 
    for the fabric interconnects in Fibre Channel environments.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.FcNetworkPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "VSAN Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/vsan"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields for VSAN Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'EnableTrunking': FieldDefinition(
                name='EnableTrunking',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enable or Disable Trunking on all of configured FC uplink ports'
            )
        })
        return fields
    
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'EnableTrunking': True
        }