"""
vNIC Template implementation.

This module implements the VnicTemplate class for handling Cisco Intersight
vNIC Template objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_template import BaseTemplate
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class VnicTemplate(BaseTemplate):
    """
    Implementation for Intersight vNIC Template objects.
    
    vNIC Templates provide a template definition for vNICs that can be 
    used in LAN Connectivity Policies to standardize vNIC configurations.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.EthIf"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "vNIC Template"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing template YAML files."""
        return "templates/vnic"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for vNIC Template objects."""
        # Get common template fields
        fields = self._get_common_template_fields()
        
        # Add vNIC-specific fields
        fields.update({
            'EthAdapterPolicy': FieldDefinition(
                name='EthAdapterPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Ethernet Adapter Policy associated with this vNIC',
                reference_type='vnic.EthAdapterPolicy',
                reference_field='Name'
            ),
            'EthNetworkPolicy': FieldDefinition(
                name='EthNetworkPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Ethernet Network Policy associated with this vNIC',
                reference_type='vnic.EthNetworkPolicy',
                reference_field='Name'
            ),
            'EthQosPolicy': FieldDefinition(
                name='EthQosPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Ethernet QoS Policy associated with this vNIC',
                reference_type='vnic.EthQosPolicy',
                reference_field='Name'
            ),
            'FabricEthNetworkControlPolicy': FieldDefinition(
                name='FabricEthNetworkControlPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Fabric Ethernet Network Control Policy associated with this vNIC',
                reference_type='fabric.EthNetworkControlPolicy',
                reference_field='Name'
            ),
            'FabricEthNetworkGroupPolicy': FieldDefinition(
                name='FabricEthNetworkGroupPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Fabric Ethernet Network Group Policy associated with this vNIC',
                reference_type='fabric.EthNetworkGroupPolicy',
                reference_field='Name'
            ),
            'MacAddressType': FieldDefinition(
                name='MacAddressType',
                field_type=FieldType.STRING,
                required=False,
                description='Type of allocation selected to assign a MAC address for the vnic',
                enum_values=['POOL', 'STATIC'],
                default_value='POOL'
            ),
            'MacPool': FieldDefinition(
                name='MacPool',
                field_type=FieldType.REFERENCE,
                required=False,
                description='MAC address pool associated with this vNIC',
                reference_type='macpool.Pool',
                reference_field='Name'
            ),
            'Mtu': FieldDefinition(
                name='Mtu',
                field_type=FieldType.INTEGER,
                required=False,
                description='The Maximum Transmission Unit (MTU) or packet size that the virtual interface accepts',
                default_value=1500,
                minimum=1500,
                maximum=9000
            ),
            'Order': FieldDefinition(
                name='Order',
                field_type=FieldType.INTEGER,
                required=False,
                description='The order in which the virtual interface is brought up',
                default_value=0,
                minimum=0,
                maximum=256
            ),
            'Placement': FieldDefinition(
                name='Placement',
                field_type=FieldType.OBJECT,
                required=False,
                description='The fabric port to which the vNICs will be associated'
            ),
            'StaticMacAddress': FieldDefinition(
                name='StaticMacAddress',
                field_type=FieldType.STRING,
                required=False,
                description='The MAC address must be in hexadecimal format xx:xx:xx:xx:xx:xx'
            ),
            'TemplateActions': FieldDefinition(
                name='TemplateActions',
                field_type=FieldType.ARRAY,
                required=False,
                description='An array of actions that are supported by this template'
            )
        })
        
        return fields
    
    def _define_template_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to vNIC Template."""
        return {
            DependencyDefinition(
                target_type='vnic.EthAdapterPolicy',
                dependency_type='references',
                required=False,
                description='vNIC Template can reference Ethernet Adapter Policy'
            ),
            DependencyDefinition(
                target_type='vnic.EthNetworkPolicy',
                dependency_type='references',
                required=False,
                description='vNIC Template can reference Ethernet Network Policy'
            ),
            DependencyDefinition(
                target_type='vnic.EthQosPolicy',
                dependency_type='references',
                required=False,
                description='vNIC Template can reference Ethernet QoS Policy'
            ),
            DependencyDefinition(
                target_type='fabric.EthNetworkControlPolicy',
                dependency_type='references',
                required=False,
                description='vNIC Template can reference Fabric Ethernet Network Control Policy'
            ),
            DependencyDefinition(
                target_type='fabric.EthNetworkGroupPolicy',
                dependency_type='references',
                required=False,
                description='vNIC Template can reference Fabric Ethernet Network Group Policy'
            ),
            DependencyDefinition(
                target_type='macpool.Pool',
                dependency_type='references',
                required=False,
                description='vNIC Template can reference MAC Pool'
            )
        }
    
    def _get_example_template_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this template type."""
        return {
            'MacAddressType': 'POOL',
            'Mtu': 1500,
            'Order': 0,
            'Placement': {
                'Id': 'MLOM',
                'Slot': 'MLOM',
                'SwitchId': 'A'
            }
        }