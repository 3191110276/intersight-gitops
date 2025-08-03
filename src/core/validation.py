"""
Comprehensive validation framework for Intersight GitOps objects.

This module provides advanced validation capabilities based on OpenAPI schema
definitions, including pattern matching, enum validation, range constraints,
and cross-field dependency validation.
"""

import re
import logging
from typing import Dict, Any, List, Optional, Union, Set
from abc import ABC, abstractmethod

from .exceptions import (
    ObjectValidationError, SchemaValidationError
)

logger = logging.getLogger(__name__)


class ValidationRule(ABC):
    """
    Abstract base class for validation rules.
    
    Each validation rule implements a specific type of validation
    that can be applied to object fields.
    """
    
    @abstractmethod
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """
        Validate a field value against this rule.
        
        Args:
            value: The field value to validate
            field_name: Name of the field being validated
            field_def: OpenAPI field definition
            
        Returns:
            List of validation error messages (empty if valid)
        """
        pass
    
    @abstractmethod
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """
        Check if this validation rule applies to the given field definition.
        
        Args:
            field_def: OpenAPI field definition
            
        Returns:
            True if this rule should be applied to the field
        """
        pass


class TypeValidationRule(ValidationRule):
    """Validates field types according to OpenAPI schema."""
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """Validate field type."""
        errors = []
        expected_type = field_def.get('type')
        
        if expected_type == 'string' and not isinstance(value, str):
            errors.append(f"Field '{field_name}' must be a string, got {type(value).__name__}")
        elif expected_type == 'integer' and not isinstance(value, int):
            errors.append(f"Field '{field_name}' must be an integer, got {type(value).__name__}")
        elif expected_type == 'number' and not isinstance(value, (int, float)):
            errors.append(f"Field '{field_name}' must be a number, got {type(value).__name__}")
        elif expected_type == 'boolean' and not isinstance(value, bool):
            errors.append(f"Field '{field_name}' must be a boolean, got {type(value).__name__}")
        elif expected_type == 'array' and not isinstance(value, list):
            errors.append(f"Field '{field_name}' must be an array, got {type(value).__name__}")
        elif expected_type == 'object' and not isinstance(value, dict):
            errors.append(f"Field '{field_name}' must be an object, got {type(value).__name__}")
        
        return errors
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule applies to all fields with a type definition."""
        return 'type' in field_def


class PatternValidationRule(ValidationRule):
    """Validates string patterns according to OpenAPI schema."""
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """Validate string pattern."""
        errors = []
        
        if not isinstance(value, str):
            return errors  # Type validation will catch this
        
        pattern = field_def.get('pattern')
        if pattern:
            try:
                if not re.match(pattern, value):
                    errors.append(
                        f"Field '{field_name}' value '{value}' does not match required pattern: {pattern}"
                    )
            except re.error as e:
                logger.warning(f"Invalid regex pattern for field '{field_name}': {pattern} - {e}")
                errors.append(f"Field '{field_name}' has invalid validation pattern")
        
        return errors
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule applies to string fields with pattern constraints."""
        return field_def.get('type') == 'string' and 'pattern' in field_def


class EnumValidationRule(ValidationRule):
    """Validates enum values according to OpenAPI schema."""
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """Validate enum value."""
        errors = []
        
        enum_values = field_def.get('enum', [])
        if enum_values and value not in enum_values:
            errors.append(
                f"Field '{field_name}' value '{value}' must be one of: {enum_values}"
            )
        
        return errors
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule applies to fields with enum constraints."""
        return 'enum' in field_def and field_def['enum']


class RangeValidationRule(ValidationRule):
    """Validates numeric ranges according to OpenAPI schema."""
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """Validate numeric range."""
        errors = []
        
        if not isinstance(value, (int, float)):
            return errors  # Type validation will catch this
        
        # Check minimum value
        minimum = field_def.get('minimum')
        if minimum is not None and value < minimum:
            errors.append(f"Field '{field_name}' value {value} is below minimum {minimum}")
        
        # Check maximum value
        maximum = field_def.get('maximum')
        if maximum is not None and value > maximum:
            errors.append(f"Field '{field_name}' value {value} is above maximum {maximum}")
        
        # Check exclusive minimum
        exclusive_minimum = field_def.get('exclusiveMinimum') 
        if exclusive_minimum is not None and value <= exclusive_minimum:
            errors.append(f"Field '{field_name}' value {value} must be greater than {exclusive_minimum}")
        
        # Check exclusive maximum
        exclusive_maximum = field_def.get('exclusiveMaximum')
        if exclusive_maximum is not None and value >= exclusive_maximum:
            errors.append(f"Field '{field_name}' value {value} must be less than {exclusive_maximum}")
        
        return errors
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule applies to numeric fields with range constraints."""
        field_type = field_def.get('type')
        has_range_constraint = any(key in field_def for key in 
                                 ['minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum'])
        return field_type in ['integer', 'number'] and has_range_constraint


class LengthValidationRule(ValidationRule):
    """Validates string and array lengths according to OpenAPI schema."""
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """Validate length constraints."""
        errors = []
        
        if not isinstance(value, (str, list)):
            return errors  # Type validation will catch this
        
        length = len(value)
        
        # Check minimum length
        min_length = field_def.get('minLength')
        if min_length is not None and length < min_length:
            errors.append(f"Field '{field_name}' length {length} is below minimum {min_length}")
        
        # Check maximum length
        max_length = field_def.get('maxLength')
        if max_length is not None and length > max_length:
            errors.append(f"Field '{field_name}' length {length} is above maximum {max_length}")
        
        return errors
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule applies to string/array fields with length constraints."""
        field_type = field_def.get('type')
        has_length_constraint = any(key in field_def for key in ['minLength', 'maxLength'])
        return field_type in ['string', 'array'] and has_length_constraint


class RequiredFieldValidationRule(ValidationRule):
    """Validates required fields according to OpenAPI schema."""
    
    def __init__(self, required_fields: Set[str]):
        """
        Initialize with required fields set.
        
        Args:
            required_fields: Set of field names that are required
        """
        self.required_fields = required_fields
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """This rule is handled at the object level, not field level."""
        return []
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule is handled separately."""
        return False
    
    def validate_object(self, obj: Dict[str, Any]) -> List[str]:
        """Validate required fields at object level."""
        errors = []
        
        for required_field in self.required_fields:
            if required_field not in obj or obj[required_field] is None:
                errors.append(f"Required field '{required_field}' is missing")
        
        return errors


class ArrayItemValidationRule(ValidationRule):
    """Validates array items according to OpenAPI schema."""
    
    def validate(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """Validate array items."""
        errors = []
        
        if not isinstance(value, list):
            return errors  # Type validation will catch this
        
        items_schema = field_def.get('items', {})
        if not items_schema:
            return errors
        
        # Validate each item in the array
        for i, item in enumerate(value):
            item_validator = FieldValidator([])
            item_errors = item_validator.validate_field(item, f"{field_name}[{i}]", items_schema)
            errors.extend(item_errors)
        
        return errors
    
    def applies_to(self, field_def: Dict[str, Any]) -> bool:
        """This rule applies to array fields with items schema."""
        return field_def.get('type') == 'array' and 'items' in field_def


class FieldValidator:
    """
    Validates individual fields using multiple validation rules.
    """
    
    def __init__(self, validation_rules: List[ValidationRule]):
        """
        Initialize with validation rules.
        
        Args:
            validation_rules: List of validation rules to apply
        """
        self.validation_rules = validation_rules
    
    def validate_field(self, value: Any, field_name: str, field_def: Dict[str, Any]) -> List[str]:
        """
        Validate a single field using all applicable rules.
        
        Args:
            value: Field value to validate
            field_name: Name of the field
            field_def: OpenAPI field definition
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        for rule in self.validation_rules:
            if rule.applies_to(field_def):
                rule_errors = rule.validate(value, field_name, field_def)
                errors.extend(rule_errors)
        
        return errors


class CrossFieldValidationRule(ABC):
    """
    Abstract base class for cross-field validation rules.
    
    These rules can validate relationships between multiple fields
    within the same object.
    """
    
    @abstractmethod
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """
        Validate cross-field relationships within an object.
        
        Args:
            obj: The object to validate
            field_definitions: OpenAPI field definitions for the object
            
        Returns:
            List of validation error messages
        """
        pass


class ConditionalRequiredFieldsRule(CrossFieldValidationRule):
    """
    Validates conditional required fields based on other field values.
    
    Example: If field A has value X, then field B is required.
    """
    
    def __init__(self, conditions: Dict[str, Dict[str, List[str]]]):
        """
        Initialize with conditional requirements.
        
        Args:
            conditions: Dictionary mapping condition field -> {value -> [required_fields]}
        """
        self.conditions = conditions
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate conditional required fields."""
        errors = []
        
        for condition_field, value_requirements in self.conditions.items():
            if condition_field in obj:
                condition_value = obj[condition_field]
                
                for trigger_value, required_fields in value_requirements.items():
                    if condition_value == trigger_value:
                        for required_field in required_fields:
                            if required_field not in obj or obj[required_field] is None:
                                errors.append(
                                    f"Field '{required_field}' is required when "
                                    f"'{condition_field}' is '{trigger_value}'"
                                )
        
        return errors


class MutuallyExclusiveFieldsRule(CrossFieldValidationRule):
    """
    Validates that certain fields are mutually exclusive.
    
    Example: Only one of field A, B, or C can be specified.
    """
    
    def __init__(self, exclusive_groups: List[List[str]]):
        """
        Initialize with mutually exclusive field groups.
        
        Args:
            exclusive_groups: List of field groups where only one field per group can be set
        """
        self.exclusive_groups = exclusive_groups
    
    def validate_object(self, obj: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate mutually exclusive fields."""
        errors = []
        
        for exclusive_group in self.exclusive_groups:
            present_fields = [field for field in exclusive_group if field in obj and obj[field] is not None]
            
            if len(present_fields) > 1:
                errors.append(
                    f"Fields {present_fields} are mutually exclusive. "
                    f"Only one of {exclusive_group} can be specified."
                )
        
        return errors


class ObjectValidator:
    """
    Main validation class that coordinates all validation rules for an object.
    """
    
    def __init__(self, field_definitions: Dict[str, Any], required_fields: Set[str] = None):
        """
        Initialize validator with field definitions.
        
        Args:
            field_definitions: OpenAPI field definitions for the object type
            required_fields: Set of required field names
        """
        self.field_definitions = field_definitions
        self.required_fields = required_fields or set()
        
        # Initialize field validation rules
        self.field_validation_rules = [
            TypeValidationRule(),
            PatternValidationRule(),
            EnumValidationRule(),
            RangeValidationRule(),
            LengthValidationRule(),
            ArrayItemValidationRule(),
        ]
        
        self.field_validator = FieldValidator(self.field_validation_rules)
        
        # Initialize cross-field validation rules
        self.cross_field_rules: List[CrossFieldValidationRule] = []
        
        # Required field rule
        if self.required_fields:
            self.required_field_rule = RequiredFieldValidationRule(self.required_fields)
        else:
            self.required_field_rule = None
    
    def add_cross_field_rule(self, rule: CrossFieldValidationRule):
        """
        Add a cross-field validation rule.
        
        Args:
            rule: Cross-field validation rule to add
        """
        self.cross_field_rules.append(rule)
    
    def validate(self, obj: Dict[str, Any]) -> List[str]:
        """
        Validate an object using all configured rules.
        
        Args:
            obj: Object to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        all_errors = []
        
        try:
            # Validate required fields
            if self.required_field_rule:
                required_errors = self.required_field_rule.validate_object(obj)
                all_errors.extend(required_errors)
            
            # Validate individual fields
            for field_name, value in obj.items():
                if field_name in self.field_definitions:
                    field_def = self.field_definitions[field_name]
                    field_errors = self.field_validator.validate_field(value, field_name, field_def)
                    all_errors.extend(field_errors)
            
            # Validate cross-field rules
            for rule in self.cross_field_rules:
                cross_field_errors = rule.validate_object(obj, self.field_definitions)
                all_errors.extend(cross_field_errors)
        
        except Exception as e:
            logger.error(f"Validation failed with exception: {e}")
            all_errors.append(f"Validation failed: {e}")
        
        return all_errors
    
    def is_valid(self, obj: Dict[str, Any]) -> bool:
        """
        Check if an object is valid.
        
        Args:
            obj: Object to validate
            
        Returns:
            True if object is valid, False otherwise
        """
        errors = self.validate(obj)
        return len(errors) == 0


def create_validator_from_schema(schema: Dict[str, Any], object_type: str) -> ObjectValidator:
    """
    Create an ObjectValidator from an OpenAPI schema definition.
    
    Args:
        schema: OpenAPI schema definition for the object type
        object_type: The object type name
        
    Returns:
        Configured ObjectValidator instance
    """
    try:
        # Extract field definitions
        field_definitions = {}
        required_fields = set()
        
        # Handle direct properties
        if 'properties' in schema:
            field_definitions.update(schema['properties'])
        
        # Handle allOf schemas
        if 'allOf' in schema:
            for subschema in schema['allOf']:
                if 'properties' in subschema:
                    field_definitions.update(subschema['properties'])
                if 'required' in subschema:
                    required_fields.update(subschema['required'])
        
        # Handle required fields at top level
        if 'required' in schema:
            required_fields.update(schema['required'])
        
        # Create base validator
        validator = ObjectValidator(field_definitions, required_fields)
        
        # Add object-type specific cross-field rules
        validator = _add_object_specific_rules(validator, object_type, field_definitions)
        
        # Apply enhanced validation rules (import here to avoid circular dependency)
        try:
            from .enhanced_validation import create_enhanced_validator
            validator = create_enhanced_validator(object_type, validator)
        except ImportError as e:
            logger.warning(f"Could not load enhanced validation for {object_type}: {e}")
        
        return validator
        
    except Exception as e:
        logger.error(f"Failed to create validator for {object_type}: {e}")
        # Return basic validator with empty definitions
        return ObjectValidator({}, set())


def _add_object_specific_rules(validator: ObjectValidator, object_type: str, 
                             field_definitions: Dict[str, Any]) -> ObjectValidator:
    """
    Add object-type specific validation rules.
    
    Args:
        validator: Base validator to enhance
        object_type: The object type name
        field_definitions: Field definitions for the object
        
    Returns:
        Enhanced validator with object-specific rules
    """
    try:
        # Example: BIOS Policy specific rules
        if object_type == 'bios.Policy':
            # Add conditional requirements for BIOS settings
            conditions = {
                'BootMode': {
                    'Uefi': ['SecureBoot'],  # If UEFI boot, secure boot setting required
                }
            }
            validator.add_cross_field_rule(ConditionalRequiredFieldsRule(conditions))
        
        # Example: Network Policy specific rules  
        elif object_type == 'vnic.EthIf':
            # VLAN and native VLAN are mutually exclusive in some contexts
            exclusive_groups = [
                ['Vlan', 'NativeVlan']  # Example - adjust based on actual schema
            ]
            validator.add_cross_field_rule(MutuallyExclusiveFieldsRule(exclusive_groups))
        
        # Add more object-specific rules as needed
        
    except Exception as e:
        logger.warning(f"Failed to add object-specific rules for {object_type}: {e}")
    
    return validator