"""
vHBA Template implementation.

This module implements the VhbaTemplate class for handling Cisco Intersight
vHBA Template objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_template import BaseTemplate
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class VhbaTemplate(BaseTemplate):
    """
    Implementation for Intersight vHBA Template objects.
    
    vHBA Templates provide a template definition for vHBAs that can be 
    used in SAN Connectivity Policies to standardize vHBA configurations.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "vnic.FcIf"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "vHBA Template"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing template YAML files."""
        return "templates/vhba"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for vHBA Template objects."""
        # Get common template fields
        fields = self._get_common_template_fields()
        
        # Add vHBA-specific fields
        fields.update({
            'FcAdapterPolicy': FieldDefinition(
                name='FcAdapterPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Fibre Channel Adapter Policy associated with this vHBA',
                reference_type='vnic.FcAdapterPolicy',
                reference_field='Name'
            ),
            'FcNetworkPolicy': FieldDefinition(
                name='FcNetworkPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Fibre Channel Network Policy associated with this vHBA',
                reference_type='vnic.FcNetworkPolicy',
                reference_field='Name'
            ),
            'FcQosPolicy': FieldDefinition(
                name='FcQosPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Fibre Channel QoS Policy associated with this vHBA',
                reference_type='vnic.FcQosPolicy',
                reference_field='Name'
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
            'PersistentBindings': FieldDefinition(
                name='PersistentBindings',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables retention of LUN ID associations in memory until they are manually cleared',
                default_value=False
            ),
            'Placement': FieldDefinition(
                name='Placement',
                field_type=FieldType.OBJECT,
                required=False,
                description='The fabric port to which the vHBAs will be associated'
            ),
            'StaticWwpnAddress': FieldDefinition(
                name='StaticWwpnAddress',
                field_type=FieldType.STRING,
                required=False,
                description='The WWPN address must be in hexadecimal format xx:xx:xx:xx:xx:xx:xx:xx'
            ),
            'TemplateActions': FieldDefinition(
                name='TemplateActions',
                field_type=FieldType.ARRAY,
                required=False,
                description='An array of actions that are supported by this template'
            ),
            'Type': FieldDefinition(
                name='Type',   
                field_type=FieldType.STRING,
                required=False,
                description='VHBA Type configuration for SAN Connectivity Policy',
                enum_values=['fc-initiator', 'fc-nvme-initiator', 'fc-nvme-target', 'fc-target'],
                default_value='fc-initiator'
            ),
            'WwpnAddressType': FieldDefinition(
                name='WwpnAddressType',
                field_type=FieldType.STRING,
                required=False,
                description='Type of allocation selected to assign a WWPN address for the vhba',
                enum_values=['POOL', 'STATIC'],
                default_value='POOL'
            ),
            'WwpnPool': FieldDefinition(
                name='WwpnPool',
                field_type=FieldType.REFERENCE,
                required=False,
                description='WWPN Pool associated with this vHBA',
                reference_type='fcpool.Pool',
                reference_field='Name'
            )
        })
        
        return fields
    
    def _define_template_specific_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies specific to vHBA Template."""
        return {
            DependencyDefinition(
                target_type='vnic.FcAdapterPolicy',
                dependency_type='references',
                required=False,
                description='vHBA Template can reference Fibre Channel Adapter Policy'
            ),
            DependencyDefinition(
                target_type='vnic.FcNetworkPolicy',
                dependency_type='references',
                required=False,
                description='vHBA Template can reference Fibre Channel Network Policy'
            ),
            DependencyDefinition(
                target_type='vnic.FcQosPolicy',
                dependency_type='references',
                required=False,
                description='vHBA Template can reference Fibre Channel QoS Policy'
            ),
            DependencyDefinition(
                target_type='fcpool.Pool',
                dependency_type='references',
                required=False,
                description='vHBA Template can reference WWPN Pool'
            )
        }
    
    def _get_example_template_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this template type."""
        return {
            'Order': 0,
            'PersistentBindings': False,
            'Type': 'fc-initiator',
            'WwpnAddressType': 'POOL',
            'Placement': {
                'Id': 'MLOM',
                'Slot': 'MLOM',
                'SwitchId': 'A'
            }
        }