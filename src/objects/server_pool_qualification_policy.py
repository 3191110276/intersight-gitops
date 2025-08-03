"""
Server Pool Qualification Policy implementation.

This module implements the ServerPoolQualificationPolicy class for handling Cisco Intersight
Server Pool Qualification Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class ServerPoolQualificationPolicy(BasePolicy):
    """
    Implementation for Intersight Server Pool Qualification Policy objects.
    
    The Server Pool Qualification policy allows you to specify qualification 
    criteria for servers to be included in server pools based on their attributes.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "resourcepool.QualificationPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Server Pool Qualification Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/server_pool_qualification"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Server Pool Qualification Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'Qualifiers': FieldDefinition(
                name='Qualifiers',
                field_type=FieldType.ARRAY,
                required=False,
                description='Array of resource qualifiers for server qualification'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'Qualifiers': [
                {
                    'ClassId': 'resource.ServerQualifier',
                    'ObjectType': 'resource.ServerQualifier',
                    'Pids': ['UCSC-C220-M5SX', 'UCSC-C240-M5SX']
                },
                {
                    'ClassId': 'resource.ProcessorQualifier',
                    'ObjectType': 'resource.ProcessorQualifier',
                    'CpuCoresRange': {
                        'ClassId': 'resource.CpuCoreRangeFilter',
                        'ObjectType': 'resource.CpuCoreRangeFilter',
                        'MinValue': 8,
                        'MaxValue': 64
                    }
                },
                {
                    'ClassId': 'resource.MemoryQualifier',
                    'ObjectType': 'resource.MemoryQualifier',
                    'MemoryCapacityRange': {
                        'ClassId': 'resource.MemoryCapacityRangeFilter',
                        'ObjectType': 'resource.MemoryCapacityRangeFilter',
                        'MinValue': 32,
                        'MaxValue': 1024
                    }
                }
            ]
        }