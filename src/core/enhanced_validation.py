"""
Enhanced validation rules for specific Intersight object types.

This module provides specialized validation rules that extend the base validation
framework with object-type specific logic and business rules.
"""

import logging
from typing import Dict, Any, List, Optional, Set
from abc import ABC, abstractmethod

from .validation import CrossFieldValidationRule, ObjectValidator
from ..utils.validation_utils import (
    validate_ip_address, validate_mac_address, validate_vlan_id,
    validate_port_number, validate_wwn, validate_iqn, validate_uuid,
    validate_hostname, validate_cidr_notation, validate_range_string,
    validate_name_field
)

logger = logging.getLogger(__name__)


class IntersightSpecificValidationRule(CrossFieldValidationRule):
    """
    Base class for Intersight-specific validation rules.
    """
    
    @abstractmethod
    def get_supported_object_types(self) -> Set[str]:
        """
        Get the set of object types this rule supports.
        
        Returns:
            Set of object type strings this rule can validate
        """
        pass


class OrganizationFieldValidationRule(IntersightSpecificValidationRule):
    """
    Validates that organization fields are properly formatted for managed objects.
    """
    
    def get_supported_object_types(self) -> Set[str]:
        """Policy and profile objects require organization fields."""
        return {
            'bios.Policy', 'boot.Policy', 'memory.Policy', 'vmedia.Policy',
            'syslog.Policy', 'ssh.Policy', 'sol.Policy', 'snmp.Policy',
            'smtp.Policy', 'sdcard.Policy', 'power.Policy', 'ntp.Policy',
            'kvm.Policy', 'ipmi.Policy', 'firmware.Policy', 'certificate.Policy',
            'access.Policy', 'server.Profile', 'chassis.Profile'
        }
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate organization field format."""
        errors = []
        
        if 'Organization' in obj:
            org = obj['Organization']
            
            if not isinstance(org, dict):
                errors.append("Organization field must be an object with 'Name' and 'ObjectType' fields")
            else:
                if 'Name' not in org:
                    errors.append("Organization object must have a 'Name' field")
                elif not isinstance(org['Name'], str) or not org['Name'].strip():
                    errors.append("Organization Name must be a non-empty string")
                
                if 'ObjectType' not in org:
                    errors.append("Organization object must have an 'ObjectType' field")
                elif org['ObjectType'] != 'organization.Organization':
                    errors.append("Organization ObjectType must be 'organization.Organization'")
        
        return errors


class PolicyReferenceValidationRule(IntersightSpecificValidationRule):
    """
    Validates policy references in profiles to ensure they follow name-based reference format.
    """
    
    def get_supported_object_types(self) -> Set[str]:
        """Profile objects that can reference policies."""
        return {'server.Profile', 'chassis.Profile'}
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate policy references use name-based format."""
        errors = []
        
        # Check PolicyBucket for policy references
        if 'PolicyBucket' in obj and isinstance(obj['PolicyBucket'], list):
            for i, policy_ref in enumerate(obj['PolicyBucket']):
                if isinstance(policy_ref, dict):
                    self._validate_policy_reference(policy_ref, f"PolicyBucket[{i}]", errors)
        
        # Check direct policy references (varies by profile type)
        policy_fields = [
            'BiosPolicy', 'BootPolicy', 'KvmPolicy', 'IpmiPolicy', 
            'SolPolicy', 'VmediaPolicy', 'LocalUserPolicy'
        ]
        
        for field in policy_fields:
            if field in obj and obj[field] is not None:
                self._validate_policy_reference(obj[field], field, errors)
        
        return errors
    
    def _validate_policy_reference(self, policy_ref: Dict[str, Any], field_path: str, errors: List[str]):
        """Validate a single policy reference."""
        if not isinstance(policy_ref, dict):
            errors.append(f"Policy reference at '{field_path}' must be an object")
            return
        
        # Check for name-based reference format
        if 'Name' in policy_ref:
            if not isinstance(policy_ref['Name'], str) or not policy_ref['Name'].strip():
                errors.append(f"Policy reference '{field_path}' Name must be a non-empty string")
        else:
            # Check if it's using MOID reference (should be converted to name)
            if 'Moid' in policy_ref:
                errors.append(
                    f"Policy reference '{field_path}' uses MOID reference. "
                    "Use name-based references for GitOps compatibility"
                )
            else:
                errors.append(f"Policy reference '{field_path}' must have a 'Name' field")
        
        # Validate ObjectType
        if 'ObjectType' not in policy_ref:
            errors.append(f"Policy reference '{field_path}' must have an 'ObjectType' field")
        elif not isinstance(policy_ref['ObjectType'], str):
            errors.append(f"Policy reference '{field_path}' ObjectType must be a string")


class NetworkConfigValidationRule(IntersightSpecificValidationRule):
    """
    Validates network-specific configurations like IP addresses, VLANs, etc.
    """
    
    def get_supported_object_types(self) -> Set[str]:
        """Network-related object types."""
        return {
            'vnic.EthIf', 'vhba.Interface', 'ippool.Pool', 'macpool.Pool',
            'ethernet.NetworkPolicy', 'vlan.Policy', 'lan.ConnectivityPolicy',
            'san.ConnectivityPolicy'
        }
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate network-specific fields."""
        errors = []
        
        # IP address validation
        ip_fields = ['IpAddress', 'Gateway', 'PrimaryDns', 'SecondaryDns']
        for field in ip_fields:
            if field in obj and obj[field]:
                errors.extend(validate_ip_address(obj[field], field))
        
        # VLAN validation
        vlan_fields = ['VlanId', 'NativeVlan']
        for field in vlan_fields:
            if field in obj and obj[field] is not None:
                errors.extend(validate_vlan_id(obj[field], field))
        
        # MAC address validation
        if 'MacAddress' in obj and obj['MacAddress']:
            errors.extend(validate_mac_address(obj['MacAddress'], 'MacAddress'))
        
        # Port number validation
        port_fields = ['Port', 'TargetPort']
        for field in port_fields:
            if field in obj and obj[field] is not None:
                errors.extend(validate_port_number(obj[field], field))
        
        # CIDR validation for pools
        if 'Subnet' in obj and obj['Subnet']:
            errors.extend(validate_cidr_notation(obj['Subnet'], 'Subnet'))
        
        return errors


class PoolConfigValidationRule(IntersightSpecificValidationRule):
    """
    Validates pool configurations including ranges and blocks.
    """
    
    def get_supported_object_types(self) -> Set[str]:
        """Pool object types."""
        return {
            'ippool.Pool', 'macpool.Pool', 'uuidpool.Pool', 
            'iqnpool.Pool', 'fcpool.Pool', 'wwnnpool.Pool', 'wwpnpool.Pool'
        }
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate pool-specific configurations."""
        errors = []
        
        # IP Pool validation
        if 'IpV4Blocks' in obj and isinstance(obj['IpV4Blocks'], list):
            for i, block in enumerate(obj['IpV4Blocks']):
                errors.extend(self._validate_ip_block(block, f"IpV4Blocks[{i}]"))
        
        if 'IpV6Blocks' in obj and isinstance(obj['IpV6Blocks'], list):
            for i, block in enumerate(obj['IpV6Blocks']):
                errors.extend(self._validate_ip_block(block, f"IpV6Blocks[{i}]", ipv6=True))
        
        # MAC Pool validation
        if 'MacBlocks' in obj and isinstance(obj['MacBlocks'], list):
            for i, block in enumerate(obj['MacBlocks']):
                errors.extend(self._validate_mac_block(block, f"MacBlocks[{i}]"))
        
        # UUID Pool validation
        if 'UuidSuffixBlocks' in obj and isinstance(obj['UuidSuffixBlocks'], list):
            for i, block in enumerate(obj['UuidSuffixBlocks']):
                errors.extend(self._validate_uuid_block(block, f"UuidSuffixBlocks[{i}]"))
        
        # IQN Pool validation
        if 'IqnSuffixBlocks' in obj and isinstance(obj['IqnSuffixBlocks'], list):
            for i, block in enumerate(obj['IqnSuffixBlocks']):
                errors.extend(self._validate_iqn_block(block, f"IqnSuffixBlocks[{i}]"))
        
        # WWN Pool validation
        wwn_block_fields = ['WwnBlocks', 'WwnnBlocks', 'WwpnBlocks']
        for field in wwn_block_fields:
            if field in obj and isinstance(obj[field], list):
                for i, block in enumerate(obj[field]):
                    errors.extend(self._validate_wwn_block(block, f"{field}[{i}]"))
        
        return errors
    
    def _validate_ip_block(self, block: Dict[str, Any], field_path: str, ipv6: bool = False) -> List[str]:
        """Validate IP address block."""
        errors = []
        
        if not isinstance(block, dict):
            errors.append(f"IP block '{field_path}' must be an object")
            return errors
        
        # Validate From and To addresses
        for addr_field in ['From', 'To']:
            if addr_field in block and block[addr_field]:
                ip_errors = validate_ip_address(
                    block[addr_field], 
                    f"{field_path}.{addr_field}",
                    allow_ipv4=not ipv6,
                    allow_ipv6=ipv6
                )
                errors.extend(ip_errors)
        
        return errors
    
    def _validate_mac_block(self, block: Dict[str, Any], field_path: str) -> List[str]:
        """Validate MAC address block."""
        errors = []
        
        if not isinstance(block, dict):
            errors.append(f"MAC block '{field_path}' must be an object")
            return errors
        
        # Validate From and To addresses
        for addr_field in ['From', 'To']:
            if addr_field in block and block[addr_field]:
                errors.extend(validate_mac_address(block[addr_field], f"{field_path}.{addr_field}"))
        
        return errors
    
    def _validate_uuid_block(self, block: Dict[str, Any], field_path: str) -> List[str]:
        """Validate UUID block."""
        errors = []
        
        if not isinstance(block, dict):
            errors.append(f"UUID block '{field_path}' must be an object")
            return errors
        
        # Validate From and To suffixes (these are typically numeric ranges)
        for field in ['From', 'To']:
            if field in block and block[field] is not None:
                try:
                    value = int(block[field])
                    if value < 0:
                        errors.append(f"UUID block '{field_path}.{field}' must be non-negative")
                except (ValueError, TypeError):
                    errors.append(f"UUID block '{field_path}.{field}' must be a valid integer")
        
        return errors
    
    def _validate_iqn_block(self, block: Dict[str, Any], field_path: str) -> List[str]:
        """Validate IQN block."""
        errors = []
        
        if not isinstance(block, dict):
            errors.append(f"IQN block '{field_path}' must be an object")
            return errors
        
        # Validate suffix ranges (typically numeric)
        for field in ['From', 'To']:
            if field in block and block[field] is not None:
                try:
                    value = int(block[field])
                    if value < 0:
                        errors.append(f"IQN block '{field_path}.{field}' must be non-negative")
                except (ValueError, TypeError):
                    errors.append(f"IQN block '{field_path}.{field}' must be a valid integer")
        
        return errors
    
    def _validate_wwn_block(self, block: Dict[str, Any], field_path: str) -> List[str]:
        """Validate WWN block."""
        errors = []
        
        if not isinstance(block, dict):
            errors.append(f"WWN block '{field_path}' must be an object")
            return errors
        
        # Validate From and To WWNs
        for addr_field in ['From', 'To']:
            if addr_field in block and block[addr_field]:
                errors.extend(validate_wwn(block[addr_field], f"{field_path}.{addr_field}"))
        
        return errors


class BiosPolicyValidationRule(IntersightSpecificValidationRule):
    """
    Validates BIOS policy specific configurations.
    """
    
    def get_supported_object_types(self) -> Set[str]:
        """BIOS policy object type."""
        return {'bios.Policy'}
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate BIOS policy specific rules."""
        errors = []
        
        # Validate boot mode dependencies
        boot_mode = obj.get('BootMode')
        if boot_mode == 'Uefi':
            # In UEFI mode, certain settings may be required or restricted
            if 'SecureBoot' not in obj:
                errors.append("BIOS Policy: SecureBoot setting should be specified when BootMode is 'Uefi'")
        
        # Validate CPU and memory related settings consistency
        if 'ProcessorC1e' in obj and 'ProcessorC3report' in obj:
            if obj['ProcessorC1e'] == 'enabled' and obj['ProcessorC3report'] == 'disabled':
                errors.append("BIOS Policy: ProcessorC3report should be enabled when ProcessorC1e is enabled")
        
        # Validate memory settings
        memory_fields = ['MemoryMappedIoAbove4gb', 'MemoryInterleave']
        populated_memory_fields = [f for f in memory_fields if f in obj and obj[f] is not None]
        
        if len(populated_memory_fields) == 1:
            errors.append(
                "BIOS Policy: When configuring memory settings, "
                "both MemoryMappedIoAbove4gb and MemoryInterleave should typically be specified"
            )
        
        return errors


def create_enhanced_validator(object_type: str, base_validator: ObjectValidator) -> ObjectValidator:
    """
    Create an enhanced validator with object-type specific rules.
    
    Args:
        object_type: The Intersight object type
        base_validator: Base validator from OpenAPI schema
        
    Returns:
        Enhanced validator with additional rules
    """
    # Available enhanced validation rules
    enhanced_rules = [
        OrganizationFieldValidationRule(),
        PolicyReferenceValidationRule(),
        NetworkConfigValidationRule(),
        PoolConfigValidationRule(),
        BiosPolicyValidationRule(),
    ]
    
    # Add applicable rules to the validator
    for rule in enhanced_rules:
        if object_type in rule.get_supported_object_types():
            base_validator.add_cross_field_rule(rule)
            logger.debug(f"Added {rule.__class__.__name__} to validator for {object_type}")
    
    return base_validator