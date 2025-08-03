"""
Link Aggregation Policy implementation.

This module implements the LinkAggregationPolicy class for handling Cisco Intersight
Link Aggregation Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class LinkAggregationPolicy(BasePolicy):
    """
    Implementation for Intersight Link Aggregation Policy objects.
    
    The Link Aggregation policy enables you to configure link aggregation 
    for the fabric interconnect ports.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "fabric.LinkAggregationPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Link Aggregation Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/link_aggregation"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Link Aggregation Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'LacpRate': FieldDefinition(
                name='LacpRate',
                field_type=FieldType.STRING,
                required=False,
                description='Flag used to indicate whether LACP PDUs are to be sent fast, i.e., every 1 second',
                enum_values=['normal', 'fast'],
                default_value='normal'
            ),
            'SuspendIndividual': FieldDefinition(
                name='SuspendIndividual',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Flag tells the switch whether to suspend the port if it does not receive LACP PDU',
                default_value=True
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'LacpRate': 'normal',
            'SuspendIndividual': True
        }