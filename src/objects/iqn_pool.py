"""
IQN Pool object implementation.

This module implements the IqnPool class for handling Cisco Intersight
iqn pool in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set, List

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_pool import BasePool

logger = logging.getLogger(__name__)


class IqnPool(BasePool):
    """
    Implementation for Intersight IQN Pool objects.
    
    IQN Pool manages allocation and assignment of iqn resources.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "iqnpool.Pool"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "IQN Pool"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing IQN Pool YAML files."""
        return "pools/iqn"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for IQN Pool objects."""
        # Start with common pool fields
        fields = self._get_common_pool_fields()
        
        # Add IQN Pool specific fields
        fields.update({
            'IqnSuffixBlocks': FieldDefinition(
                name='IqnSuffixBlocks',
                field_type=FieldType.ARRAY,
                required=False,
                description='Collection of IQN suffix blocks that define the IQN ranges'
            ),
            'Prefix': FieldDefinition(
                name='Prefix',
                field_type=FieldType.STRING,
                required=True,
                description='The prefix for any IQN blocks created for this pool. IQN Prefix must have the format "iqn.yyyy-mm.naming-authority"'
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
            'Prefix': 'iqn.2023-01.com.example',
            'IqnSuffixBlocks': [
                {
                    'ObjectType': 'iqnpool.IqnSuffixBlock',
                    'From': 1,
                    'Size': 100,
                    'Suffix': 'test.pool'
                }
            ]
        }
    
    def validate_object(self, obj: Dict[str, Any]) -> List[str]:
        """
        Validate IQN Pool object with additional IQN-specific validation.
        
        Args:
            obj: IQN Pool object to validate
            
        Returns:
            List of validation error messages
        """
        
        errors = super().validate_object(obj)
        
        # Validate IqnSuffixBlocks if present
        if 'IqnSuffixBlocks' in obj and obj['IqnSuffixBlocks']:
            iqn_blocks = obj['IqnSuffixBlocks']
            if not isinstance(iqn_blocks, list):
                errors.append("IqnSuffixBlocks must be an array")
            else:
                for i, block in enumerate(iqn_blocks):
                    block_errors = self._validate_iqn_block(block, i)
                    errors.extend(block_errors)
        
        return errors
    
    def _validate_iqn_block(self, block: Dict[str, Any], index: int) -> List[str]:
        """
        Validate a single IQN suffix block.
        
        Args:
            block: IQN block dictionary
            index: Index of the block in the array
            
        Returns:
            List of validation error messages
        """
        
        errors = []
        block_prefix = f"IqnSuffixBlocks[{index}]"
        
        # Check required fields
        if not isinstance(block, dict):
            errors.append(f"{block_prefix}: Must be an object")
            return errors
        
        # Validate ObjectType
        if 'ObjectType' not in block:
            errors.append(f"{block_prefix}: Missing required field 'ObjectType'")
        elif block['ObjectType'] != 'iqnpool.IqnSuffixBlock':
            errors.append(f"{block_prefix}: ObjectType must be 'iqnpool.IqnSuffixBlock'")
        
        # Validate From (start number)
        if 'From' not in block:
            errors.append(f"{block_prefix}: Missing required field 'From'")
        elif not isinstance(block['From'], int) or block['From'] < 1:
            errors.append(f"{block_prefix}: 'From' must be a positive integer")
        
        # Validate Size
        if 'Size' not in block:
            errors.append(f"{block_prefix}: Missing required field 'Size'")
        elif not isinstance(block['Size'], int) or block['Size'] < 1:
            errors.append(f"{block_prefix}: 'Size' must be a positive integer")
        
        # Validate Suffix (optional but should be valid if present)
        if 'Suffix' in block and block['Suffix'] is not None:
            if not isinstance(block['Suffix'], str):
                errors.append(f"{block_prefix}: 'Suffix' must be a string")
            elif not block['Suffix'].strip():
                errors.append(f"{block_prefix}: 'Suffix' cannot be empty")
        
        return errors
