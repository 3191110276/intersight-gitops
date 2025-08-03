"""
Flow Control Policy implementation.

This module implements the FlowControlPolicy class for handling Cisco Intersight
Flow Control Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class FlowControlPolicy(BasePolicy):
    """
    Implementation for Intersight Flow Control Policy objects.
    
    The Flow Control policy enables Priority Flow Control (PFC) on the server 
    interfaces and the corresponding Data Center Ethernet (DCE) interfaces.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.FlowControlPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Flow Control Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/flow_control"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Flow Control Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'PriorityFlowControlMode': FieldDefinition(
                name='PriorityFlowControlMode',
                field_type=FieldType.STRING,
                required=False,
                description='Priority Flow Control Mode for the port',
                enum_values=['on', 'off', 'auto'],
                default_value='auto'
            ),
            'ReceiveDirection': FieldDefinition(
                name='ReceiveDirection',
                field_type=FieldType.STRING,
                required=False,
                description='Link level Flow Control configured in the receive direction',
                enum_values=['Enabled', 'Disabled'],
                default_value='Disabled'
            ),
            'SendDirection': FieldDefinition(
                name='SendDirection',
                field_type=FieldType.STRING,
                required=False,
                description='Link level Flow Control configured in the send direction',
                enum_values=['Enabled', 'Disabled'],
                default_value='Disabled'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'PriorityFlowControlMode': 'auto',
            'ReceiveDirection': 'Disabled',
            'SendDirection': 'Disabled'
        }