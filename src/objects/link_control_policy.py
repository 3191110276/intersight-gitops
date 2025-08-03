"""
Link Control Policy implementation.

This module implements the LinkControlPolicy class for handling Cisco Intersight
Link Control Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class LinkControlPolicy(BasePolicy):
    """
    Implementation for Intersight Link Control Policy objects.
    
    The Link Control policy enables you to control the link behavior 
    for the fabric interconnect ports.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.LinkControlPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Link Control Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/link_control"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Link Control Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'UdldSettings': FieldDefinition(
                name='UdldSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Unidirectional Link Detection (UDLD) Settings'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'UdldSettings': {
                'AdminState': 'Enabled',
                'Mode': 'normal'
            }
        }