"""
Validation utility functions for Intersight GitOps objects.

This module provides utility functions to help with validation tasks
across different object types.
"""

import re
import logging
from typing import Dict, Any, List, Optional, Union, Pattern
from ipaddress import IPv4Address, IPv6Address, AddressValueError

logger = logging.getLogger(__name__)


def validate_ip_address(value: str, field_name: str, allow_ipv4: bool = True, allow_ipv6: bool = True) -> List[str]:
    """
    Validate an IP address.
    
    Args:
        value: IP address string to validate
        field_name: Name of the field being validated
        allow_ipv4: Whether IPv4 addresses are allowed
        allow_ipv6: Whether IPv6 addresses are allowed
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    valid_ipv4 = False
    valid_ipv6 = False
    
    # Try IPv4
    if allow_ipv4:
        try:
            IPv4Address(value)
            valid_ipv4 = True
        except AddressValueError:
            pass
    
    # Try IPv6
    if allow_ipv6 and not valid_ipv4:
        try:
            IPv6Address(value)
            valid_ipv6 = True
        except AddressValueError:
            pass
    
    if not valid_ipv4 and not valid_ipv6:
        if allow_ipv4 and allow_ipv6:
            errors.append(f"Field '{field_name}' must be a valid IPv4 or IPv6 address")
        elif allow_ipv4:
            errors.append(f"Field '{field_name}' must be a valid IPv4 address")
        elif allow_ipv6:
            errors.append(f"Field '{field_name}' must be a valid IPv6 address")
    
    return errors


def validate_mac_address(value: str, field_name: str) -> List[str]:
    """
    Validate a MAC address.
    
    Args:
        value: MAC address string to validate
        field_name: Name of the field being validated
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    # Common MAC address patterns
    mac_patterns = [
        r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',  # XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
        r'^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$',    # XXXX.XXXX.XXXX
        r'^([0-9A-Fa-f]{12})$'                          # XXXXXXXXXXXX
    ]
    
    valid = any(re.match(pattern, value) for pattern in mac_patterns)
    
    if not valid:
        errors.append(f"Field '{field_name}' must be a valid MAC address")
    
    return errors


def validate_vlan_id(value: Union[int, str], field_name: str) -> List[str]:
    """
    Validate a VLAN ID.
    
    Args:
        value: VLAN ID to validate
        field_name: Name of the field being validated
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    try:
        vlan_id = int(value)
        if vlan_id < 1 or vlan_id > 4094:
            errors.append(f"Field '{field_name}' VLAN ID must be between 1 and 4094")
    except (ValueError, TypeError):
        errors.append(f"Field '{field_name}' VLAN ID must be a valid integer")
    
    return errors


def validate_port_number(value: Union[int, str], field_name: str) -> List[str]:
    """
    Validate a network port number.
    
    Args:
        value: Port number to validate
        field_name: Name of the field being validated
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    try:
        port = int(value)
        if port < 1 or port > 65535:
            errors.append(f"Field '{field_name}' port number must be between 1 and 65535")
    except (ValueError, TypeError):
        errors.append(f"Field '{field_name}' port number must be a valid integer")
    
    return errors


def validate_wwn(value: str, field_name: str, wwn_type: str = "WWN") -> List[str]:
    """
    Validate a World Wide Name (WWN).
    
    Args:
        value: WWN string to validate
        field_name: Name of the field being validated
        wwn_type: Type of WWN (WWNN, WWPN, or WWN)
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    # WWN pattern: 8 groups of 2 hex digits separated by colons
    wwn_pattern = r'^([0-9A-Fa-f]{2}:){7}[0-9A-Fa-f]{2}$'
    
    if not re.match(wwn_pattern, value):
        errors.append(f"Field '{field_name}' must be a valid {wwn_type} (format: XX:XX:XX:XX:XX:XX:XX:XX)")
    
    return errors


def validate_iqn(value: str, field_name: str) -> List[str]:
    """
    Validate an iSCSI Qualified Name (IQN).
    
    Args:
        value: IQN string to validate
        field_name: Name of the field being validated
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    # Basic IQN pattern validation
    iqn_pattern = r'^iqn\.\d{4}-\d{2}\.[a-zA-Z0-9\-\.]+:[a-zA-Z0-9\-\.:]+$'
    
    if not re.match(iqn_pattern, value):
        errors.append(f"Field '{field_name}' must be a valid IQN (format: iqn.yyyy-mm.domain:identifier)")
    
    return errors


def validate_uuid(value: str, field_name: str) -> List[str]:
    """
    Validate a UUID.
    
    Args:
        value: UUID string to validate
        field_name: Name of the field being validated
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    # UUID pattern: 8-4-4-4-12 hex digits
    uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    
    if not re.match(uuid_pattern, value):
        errors.append(f"Field '{field_name}' must be a valid UUID")
    
    return errors


def validate_hostname(value: str, field_name: str) -> List[str]:
    """
    Validate a hostname.
    
    Args:
        value: Hostname string to validate
        field_name: Name of the field being validated
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    if len(value) > 253:
        errors.append(f"Field '{field_name}' hostname too long (max 253 characters)")
        return errors
    
    # Hostname pattern: labels separated by dots
    hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    
    if not re.match(hostname_pattern, value):
        errors.append(f"Field '{field_name}' must be a valid hostname")
    
    return errors


def validate_cidr_notation(value: str, field_name: str, allow_ipv4: bool = True, allow_ipv6: bool = True) -> List[str]:
    """
    Validate CIDR notation.
    
    Args:
        value: CIDR string to validate (e.g., "192.168.1.0/24")
        field_name: Name of the field being validated
        allow_ipv4: Whether IPv4 CIDR is allowed
        allow_ipv6: Whether IPv6 CIDR is allowed
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    if '/' not in value:
        errors.append(f"Field '{field_name}' must be in CIDR notation (address/prefix)")
        return errors
    
    try:
        network_part, prefix_part = value.split('/', 1)
        prefix = int(prefix_part)
        
        # Validate IP address part
        ip_errors = validate_ip_address(network_part, field_name, allow_ipv4, allow_ipv6)
        if ip_errors:
            errors.extend(ip_errors)
            return errors
        
        # Validate prefix length
        try:
            IPv4Address(network_part)
            # IPv4 - prefix should be 0-32
            if prefix < 0 or prefix > 32:
                errors.append(f"Field '{field_name}' IPv4 prefix must be between 0 and 32")
        except AddressValueError:
            try:
                IPv6Address(network_part)
                # IPv6 - prefix should be 0-128
                if prefix < 0 or prefix > 128:
                    errors.append(f"Field '{field_name}' IPv6 prefix must be between 0 and 128")
            except AddressValueError:
                errors.append(f"Field '{field_name}' contains invalid IP address")
    
    except ValueError:
        errors.append(f"Field '{field_name}' prefix must be a valid integer")
    except Exception:
        errors.append(f"Field '{field_name}' is not valid CIDR notation")
    
    return errors


def validate_range_string(value: str, field_name: str, min_val: int = None, max_val: int = None) -> List[str]:
    """
    Validate a range string (e.g., "1-10", "5", "1,3,5-7").
    
    Args:
        value: Range string to validate
        field_name: Name of the field being validated
        min_val: Minimum allowed value in range
        max_val: Maximum allowed value in range
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    try:
        # Split by commas for multiple ranges
        ranges = [r.strip() for r in value.split(',')]
        
        for range_part in ranges:
            if '-' in range_part:
                # Range format (e.g., "1-10")
                start_str, end_str = range_part.split('-', 1)
                start = int(start_str.strip())
                end = int(end_str.strip())
                
                if start > end:
                    errors.append(f"Field '{field_name}' range start ({start}) must be <= end ({end})")
                
                if min_val is not None and start < min_val:
                    errors.append(f"Field '{field_name}' range start ({start}) is below minimum ({min_val})")
                
                if max_val is not None and end > max_val:
                    errors.append(f"Field '{field_name}' range end ({end}) is above maximum ({max_val})")
            else:
                # Single value
                val = int(range_part)
                
                if min_val is not None and val < min_val:
                    errors.append(f"Field '{field_name}' value ({val}) is below minimum ({min_val})")
                
                if max_val is not None and val > max_val:
                    errors.append(f"Field '{field_name}' value ({val}) is above maximum ({max_val})")
    
    except ValueError:
        errors.append(f"Field '{field_name}' contains invalid range format")
    
    return errors


def validate_name_field(value: str, field_name: str, max_length: int = 64, 
                       allow_spaces: bool = True, allow_special_chars: bool = False) -> List[str]:
    """
    Validate a name field with common naming restrictions.
    
    Args:
        value: Name string to validate
        field_name: Name of the field being validated
        max_length: Maximum allowed length
        allow_spaces: Whether spaces are allowed
        allow_special_chars: Whether special characters (other than - and _) are allowed
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    if not value.strip():
        errors.append(f"Field '{field_name}' cannot be empty")
        return errors
    
    if len(value) > max_length:
        errors.append(f"Field '{field_name}' exceeds maximum length of {max_length} characters")
    
    # Check for invalid characters
    if not allow_spaces and ' ' in value:
        errors.append(f"Field '{field_name}' cannot contain spaces")
    
    if not allow_special_chars:
        # Allow only alphanumeric, hyphen, underscore, and optionally spaces
        allowed_pattern = r'^[a-zA-Z0-9\-_' + (' ' if allow_spaces else '') + ']+$'
        if not re.match(allowed_pattern, value):
            chars = "letters, numbers, hyphens, and underscores"
            if allow_spaces:
                chars += ", and spaces"
            errors.append(f"Field '{field_name}' can only contain {chars}")
    
    return errors


# Compiled regex patterns for better performance
COMMON_PATTERNS = {
    'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    'fqdn': re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'),
    'ipv4': re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'),
    'ipv6': re.compile(r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$'),
}


def validate_with_pattern(value: str, field_name: str, pattern_name: str) -> List[str]:
    """
    Validate a value against a predefined common pattern.
    
    Args:
        value: String value to validate
        field_name: Name of the field being validated
        pattern_name: Name of the pattern to validate against
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"Field '{field_name}' must be a string")
        return errors
    
    pattern = COMMON_PATTERNS.get(pattern_name)
    if not pattern:
        errors.append(f"Unknown validation pattern: {pattern_name}")
        return errors
    
    if not pattern.match(value):
        errors.append(f"Field '{field_name}' does not match expected {pattern_name} format")
    
    return errors