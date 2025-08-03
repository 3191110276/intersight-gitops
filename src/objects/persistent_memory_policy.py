"""
Persistent Memory Policy implementation.

This module implements the PersistentMemoryPolicy class for handling Cisco Intersight
Persistent Memory Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class PersistentMemoryPolicy(BasePolicy):
    """
    Implementation for Intersight Persistent Memory Policy objects.
    
    The Persistent Memory policy allows you to configure persistent memory 
    modules (also known as storage class memory or NVDIMM) settings for servers.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "memory.PersistentMemoryPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Persistent Memory Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/persistent_memory"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Persistent Memory Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'Goals': FieldDefinition(
                name='Goals',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of persistent memory configuration goals'
            ),
            'LocalSecurity': FieldDefinition(
                name='LocalSecurity',
                field_type=FieldType.OBJECT,
                required=False,
                description='Local security settings for persistent memory'
            ),
            'LogicalNamespaces': FieldDefinition(
                name='LogicalNamespaces',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of logical namespaces for persistent memory'
            ),
            'ManagementMode': FieldDefinition(
                name='ManagementMode',
                field_type=FieldType.STRING,
                required=False,
                description='Management mode for the persistent memory policy',
                enum_values=['configured-from-intersight', 'configured-from-operating-system'],
                default_value='configured-from-intersight'
            ),
            'RetainNamespaces': FieldDefinition(
                name='RetainNamespaces',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Persistent Memory Namespaces to be retained or not',
                default_value=True
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'ManagementMode': 'configured-from-intersight',
            'RetainNamespaces': True,
            'Goals': [
                {
                    'MemoryModePercentage': 0,
                    'PersistentMemoryType': 'app-direct',
                    'SocketId': 'All Sockets'
                }
            ],
            'LocalSecurity': {
                'Enabled': False,
                'SecurePassphrase': ''
            }
        }