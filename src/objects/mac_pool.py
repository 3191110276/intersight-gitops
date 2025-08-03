"""
MAC Pool object implementation.

This module implements the MacPool class for handling Cisco Intersight
mac pool in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set, List

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_pool import BasePool

logger = logging.getLogger(__name__)


class MacPool(BasePool):
    """
    Implementation for Intersight MAC Pool objects.
    
    MAC Pool manages allocation and assignment of mac resources.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "macpool.Pool"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "MAC Pool"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing MAC Pool YAML files."""
        return "pools/mac"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for MAC Pool objects."""
        # Start with common pool fields
        fields = self._get_common_pool_fields()
        
        # Add MAC Pool specific fields
        fields.update({
            'AssignmentOrder': FieldDefinition(
                name='AssignmentOrder',
                field_type=FieldType.STRING,
                required=False,
                description='Assignment order decides the order in which the next identifier is allocated',
                enum_values=['sequential', 'default'],
                default_value='sequential'
            ),
            'MacBlocks': FieldDefinition(
                name='MacBlocks',
                field_type=FieldType.ARRAY,
                required=False,
                description='Collection of MAC blocks that define the MAC address ranges'
            )
        })
        
        return fields
    
    def _get_example_pool_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this pool type.
        
        Returns:
            Dictionary of example field values
        """
        return {
            'AssignmentOrder': 'sequential',
            'MacBlocks': [
                {
                    'ObjectType': 'macpool.Block',
                    'From': '00:25:B5:00:00:01',
                    'To': '00:25:B5:00:00:FF'
                }
            ]
        }
    
    def validate_object(self, obj: Dict[str, Any]) -> List[str]:
        """
        Validate MAC Pool object with additional MAC-specific validation.
        
        Args:
            obj: MAC Pool object to validate
            
        Returns:
            List of validation error messages
        """
        errors = super().validate_object(obj)
        
        # Validate MacBlocks if present
        if 'MacBlocks' in obj and obj['MacBlocks']:
            mac_blocks = obj['MacBlocks']
            if not isinstance(mac_blocks, list):
                errors.append("MacBlocks must be an array")
            else:
                for i, block in enumerate(mac_blocks):
                    block_errors = self._validate_mac_block(block, i)
                    errors.extend(block_errors)
        
        return errors
    
    def _validate_mac_block(self, block: Dict[str, Any], index: int) -> List[str]:
        """
        Validate a single MAC address block.
        
        Args:
            block: MAC block dictionary
            index: Index of the block in the array
            
        Returns:
            List of validation error messages
        """
        errors = []
        block_prefix = f"MacBlocks[{index}]"
        
        # Check required fields
        if not isinstance(block, dict):
            errors.append(f"{block_prefix}: Must be an object")
            return errors
        
        # Validate ObjectType
        if 'ObjectType' not in block:
            errors.append(f"{block_prefix}: Missing required field 'ObjectType'")
        elif block['ObjectType'] != 'macpool.Block':
            errors.append(f"{block_prefix}: ObjectType must be 'macpool.Block'")
        
        # Validate From address
        if 'From' not in block:
            errors.append(f"{block_prefix}: Missing required field 'From'")
        elif not self._is_valid_mac_address(block['From']):
            errors.append(f"{block_prefix}: 'From' must be a valid MAC address in format xx:xx:xx:xx:xx:xx")
        
        # Validate To address
        if 'To' not in block:
            errors.append(f"{block_prefix}: Missing required field 'To'")
        elif not self._is_valid_mac_address(block['To']):
            errors.append(f"{block_prefix}: 'To' must be a valid MAC address in format xx:xx:xx:xx:xx:xx")
        
        # Validate range if both addresses are present and valid
        if ('From' in block and 'To' in block and 
            self._is_valid_mac_address(block['From']) and 
            self._is_valid_mac_address(block['To'])):
            
            if not self._is_valid_mac_range(block['From'], block['To']):
                errors.append(f"{block_prefix}: 'From' address must be less than or equal to 'To' address")
        
        return errors
    
    def _is_valid_mac_address(self, mac_addr: str) -> bool:
        """
        Validate MAC address format.
        
        Args:
            mac_addr: MAC address string
            
        Returns:
            True if valid MAC address format
        """
        if not isinstance(mac_addr, str):
            return False
        
        # MAC address pattern: xx:xx:xx:xx:xx:xx where x is hexadecimal
        import re
        mac_pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        return bool(re.match(mac_pattern, mac_addr))
    
    def _is_valid_mac_range(self, from_mac: str, to_mac: str) -> bool:
        """
        Validate that from_mac <= to_mac.
        
        Args:
            from_mac: Starting MAC address
            to_mac: Ending MAC address
            
        Returns:
            True if valid range
        """
        try:
            # Convert MAC addresses to integers for comparison
            from_int = int(from_mac.replace(':', ''), 16)
            to_int = int(to_mac.replace(':', ''), 16)
            return from_int <= to_int
        except ValueError:
            return False
    
    def _extract_user_defined_values(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract only user-defined values from an Intersight object, with field name correction for MAC pools.
        
        Args:
            obj: The raw object dictionary from Intersight API
            
        Returns:
            Dictionary containing only user-defined values with correct field names
        """
        # Start with base extraction
        extracted = super()._extract_user_defined_values(obj)
        
        # Fix MacBlocks field name issues
        if 'MacBlocks' in extracted and extracted['MacBlocks']:
            corrected_blocks = []
            for block in extracted['MacBlocks']:
                if isinstance(block, dict):
                    corrected_block = {}
                    
                    # Copy ObjectType with case correction
                    if 'ObjectType' in block:
                        corrected_block['ObjectType'] = block['ObjectType']
                    elif 'object_type' in block:
                        corrected_block['ObjectType'] = block['object_type']
                    
                    # Transform _from to From
                    if '_from' in block:
                        corrected_block['From'] = block['_from']
                    elif 'from' in block:
                        corrected_block['From'] = block['from']
                    elif 'From' in block:
                        corrected_block['From'] = block['From']
                    
                    # Transform to/To to To (ensure proper casing)
                    if 'to' in block:
                        corrected_block['To'] = block['to']
                    elif 'To' in block:
                        corrected_block['To'] = block['To']
                    
                    # Skip the 'size' field - it's computed and shouldn't be exported
                    
                    corrected_blocks.append(corrected_block)
                else:
                    corrected_blocks.append(block)
            
            extracted['MacBlocks'] = corrected_blocks
        
        return extracted
