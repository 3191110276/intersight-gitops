"""
Fibre Channel Adapter Policy implementation.

This module implements the FibreChannelAdapterPolicy class for handling Cisco Intersight
Fibre Channel Adapter Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class FibreChannelAdapterPolicy(BasePolicy):
    """
    Implementation for Intersight Fibre Channel Adapter Policy objects.
    
    The Fibre Channel Adapter policy governs the host-side behavior of the 
    adapter, including how the adapter handles traffic on the vHBA.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.FcAdapterPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Fibre Channel Adapter Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/fibre_channel_adapter"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Fibre Channel Adapter Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'ErrorDetectionTimeout': FieldDefinition(
                name='ErrorDetectionTimeout',
                field_type=FieldType.INTEGER,
                required=False,
                description='Error Detection Timeout, in milliseconds',
                default_value=2000,
                minimum=1000,
                maximum=100000
            ),
            'ErrorRecoverySettings': FieldDefinition(
                name='ErrorRecoverySettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Error Recovery Settings for the vHBA'
            ),
            'FlogiSettings': FieldDefinition(
                name='FlogiSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Fibre Channel Fabric Login (FLOGI) Settings'
            ),
            'InterruptSettings': FieldDefinition(
                name='InterruptSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Interrupt Settings for the vHBA'
            ),
            'IoThrottleCount': FieldDefinition(
                name='IoThrottleCount',
                field_type=FieldType.INTEGER,
                required=False,
                description='The maximum number of data or control I/O operations that can be pending for the virtual interface at one time',
                default_value=512,
                minimum=1,
                maximum=1024
            ),
            'LunCount': FieldDefinition(
                name='LunCount',
                field_type=FieldType.INTEGER,
                required=False,
                description='The maximum number of LUNs that the HBA can support',
                default_value=1024,
                minimum=1,
                maximum=4096
            ),
            'LunQueueDepth': FieldDefinition(
                name='LunQueueDepth',
                field_type=FieldType.INTEGER,
                required=False,
                description='The number of commands that the HBA can send and receive in a single transmission per LUN',
                default_value=20,
                minimum=1,
                maximum=254
            ),
            'PlogiSettings': FieldDefinition(
                name='PlogiSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Fibre Channel Port Login (PLOGI) Settings'
            ),
            'ResourceAllocationTimeout': FieldDefinition(
                name='ResourceAllocationTimeout',
                field_type=FieldType.INTEGER,
                required=False,
                description='Resource Allocation Timeout, in seconds',
                default_value=10000,
                minimum=5000,
                maximum=100000
            ),
            'RxQueueSettings': FieldDefinition(
                name='RxQueueSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Receive Queue Settings for the vHBA'
            ),
            'ScsiQueueSettings': FieldDefinition(
                name='ScsiQueueSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='SCSI Queue Settings for the vHBA'
            ),
            'TxQueueSettings': FieldDefinition(
                name='TxQueueSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Transmit Queue Settings for the vHBA'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'ErrorDetectionTimeout': 2000,
            'IoThrottleCount': 512,
            'LunCount': 1024,
            'LunQueueDepth': 20,
            'ResourceAllocationTimeout': 10000,
            'ErrorRecoverySettings': {
                'Enabled': False,
                'IoRetryCount': 8,
                'IoRetryTimeout': 5,
                'LinkDownTimeout': 30000,
                'PortDownTimeout': 10000
            },
            'FlogiSettings': {
                'Retries': 8,
                'Timeout': 4000
            },
            'PlogiSettings': {
                'Retries': 8,
                'Timeout': 20000
            }
        }