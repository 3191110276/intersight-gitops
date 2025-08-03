"""
Power Policy object implementation.

This module implements the PowerPolicy class for handling Cisco Intersight
power policy in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class PowerPolicy(BasePolicy):
    """
    Implementation for Intersight Power Policy objects.
    
    Power Policy defines settings and configurations for the power policy.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "power.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Power Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing Power Policy YAML files."""
        return "policies/power"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Power Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add power policy-specific fields
        fields.update({
            'AllocatedBudget': FieldDefinition(
                name='AllocatedBudget',
                field_type=FieldType.INTEGER,
                required=False,
                description='Allocated power budget (0-65535 watts)',
                minimum=0,
                maximum=65535
            ),
            'DynamicRebalancing': FieldDefinition(
                name='DynamicRebalancing',
                field_type=FieldType.STRING,
                required=False,
                description='Dynamic power rebalancing',
                enum_values=['Enabled', 'Disabled']
            ),
            'ExtendedPowerCapacity': FieldDefinition(
                name='ExtendedPowerCapacity',
                field_type=FieldType.STRING,
                required=False,
                description='Extended power capacity',
                enum_values=['Enabled', 'Disabled']
            ),
            'PowerPriority': FieldDefinition(
                name='PowerPriority',
                field_type=FieldType.STRING,
                required=False,
                description='Power priority level',
                enum_values=['Low', 'Medium', 'High']
            ),
            'PowerProfiling': FieldDefinition(
                name='PowerProfiling',
                field_type=FieldType.STRING,
                required=False,
                description='Power profiling',
                enum_values=['Enabled', 'Disabled']
            ),
            'PowerRestoreState': FieldDefinition(
                name='PowerRestoreState',
                field_type=FieldType.STRING,
                required=False,
                description='Power restore state',
                enum_values=['AlwaysOff', 'AlwaysOn', 'LastState']
            ),
            'PowerSaveMode': FieldDefinition(
                name='PowerSaveMode',
                field_type=FieldType.STRING,
                required=False,
                description='Power save mode',
                enum_values=['Enabled', 'Disabled']
            ),
            'ProcessorPackagePowerLimit': FieldDefinition(
                name='ProcessorPackagePowerLimit',
                field_type=FieldType.STRING,
                required=False,
                description='Processor package power limit',
                enum_values=['Default', 'Maximum', 'Minimum']
            ),
            'RedundancyMode': FieldDefinition(
                name='RedundancyMode',
                field_type=FieldType.STRING,
                required=False,
                description='Redundancy mode',
                enum_values=['Grid', 'NotRedundant', 'N+1', 'N+2']
            )
        })
        
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this policy type.
        
        Returns:
            Dictionary of example field values
        """
        return {
            'AllocatedBudget': 800,
            'DynamicRebalancing': 'Enabled',
            'ExtendedPowerCapacity': 'Enabled',
            'PowerPriority': 'Medium',
            'PowerProfiling': 'Enabled',
            'PowerRestoreState': 'LastState',
            'PowerSaveMode': 'Enabled',
            'ProcessorPackagePowerLimit': 'Default',
            'RedundancyMode': 'N+1'
        }
