"""
Memory Policy object implementation.

This module implements the MemoryPolicy class for handling Cisco Intersight
memory policies in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class MemoryPolicy(BasePolicy):
    """
    Implementation for Intersight Memory Policy objects.
    
    Memory policies define memory configuration settings for servers,
    including DIMM blocklisting and other memory-related configurations.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "memory.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Memory Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing memory policy YAML files."""
        return "policies/memory"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Memory Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add memory policy-specific fields
        memory_fields = {
            'EnableDimmBlocklisting': FieldDefinition(
                name='EnableDimmBlocklisting',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enable DIMM Blocklisting on the server. This feature allows faulty DIMMs to be blocklisted and removed from system inventory'
            )
        }
        
        # Merge common and memory-specific fields
        fields.update(memory_fields)
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to memory policy."""
        return {
            'EnableDimmBlocklisting': True
        }