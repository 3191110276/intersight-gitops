"""
Ethernet Adapter Policy implementation.

This module implements the EthernetAdapterPolicy class for handling Cisco Intersight
Ethernet Adapter Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class EthernetAdapterPolicy(BasePolicy):
    """
    Implementation for Intersight Ethernet Adapter Policy objects.
    
    An Ethernet adapter policy governs the host-side behavior of the adapter, 
    including how the adapter handles traffic. For each VIC Virtual Ethernet 
    Interface various features like VXLAN, NVGRE, ARFS, Interrupt settings, 
    and TCP Offload settings can be configured.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.EthAdapterPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Ethernet Adapter Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/ethernet_adapter"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields for Ethernet Adapter Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'AdvancedFilter': FieldDefinition(
                name='AdvancedFilter',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables advanced filtering on the interface',
                default_value=False
            ),
            'ArfsSettings': FieldDefinition(
                name='ArfsSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Settings for Accelerated Receive Flow Steering to reduce the network latency and increase CPU cache efficiency'
            ),
            'CompletionQueueSettings': FieldDefinition(
                name='CompletionQueueSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Completion Queue resource settings'
            ),
            'EtherChannelPinningEnabled': FieldDefinition(
                name='EtherChannelPinningEnabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables EtherChannel Pinning to combine multiple physical links between two network switches into a single logical link',
                default_value=False
            ),
            'GeneveEnabled': FieldDefinition(
                name='GeneveEnabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='GENEVE offload protocol allows you to create logical networks that span physical network boundaries',
                default_value=False
            ),
            'InterruptScaling': FieldDefinition(
                name='InterruptScaling',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables Interrupt Scaling on the interface',
                default_value=False
            ),
            'InterruptSettings': FieldDefinition(
                name='InterruptSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Interrupt Settings for the virtual ethernet interface'
            ),
            'RssSettings': FieldDefinition(
                name='RssSettings',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Receive Side Scaling allows the incoming traffic to be spread across multiple CPU cores',
                default_value=True
            ),
            'RxQueueSettings': FieldDefinition(
                name='RxQueueSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Receive Queue resource settings'
            ),
            'TcpOffloadSettings': FieldDefinition(
                name='TcpOffloadSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='The TCP offload settings decide whether to offload the TCP related network functions from the CPU to the network hardware or not'
            ),
            'TxQueueSettings': FieldDefinition(
                name='TxQueueSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Transmit Queue resource settings'
            ),
            'UplinkFailbackTimeout': FieldDefinition(
                name='UplinkFailbackTimeout',
                field_type=FieldType.INTEGER,
                required=False,
                description='Uplink Failback Timeout in seconds when uplink failover is enabled for a vNIC',
                default_value=5,
                minimum=0,
                maximum=600
            ),
            'VxlanSettings': FieldDefinition(
                name='VxlanSettings',
                field_type=FieldType.OBJECT,
                required=False,
                description='Virtual Extensible LAN Protocol Settings'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'AdvancedFilter': False,
            'EtherChannelPinningEnabled': False,
            'GeneveEnabled': False,
            'InterruptScaling': False,
            'RssSettings': True,
            'UplinkFailbackTimeout': 5,
            'InterruptSettings': {
                'CoalescingTime': 125,
                'CoalescingType': 'MIN',
                'Count': 32,
                'Mode': 'MSIx'
            },
            'RxQueueSettings': {
                'Count': 4,
                'RingSize': 512
            },
            'TxQueueSettings': {
                'Count': 4,
                'RingSize': 256
            }
        }