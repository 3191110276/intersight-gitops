"""
Core object type class for Intersight GitOps.

This module provides the core ObjectType class that all specific Intersight 
object implementations must inherit from. It provides comprehensive functionality
for dependency management, field definitions, validation, and transformations.
"""

import os
import json
import yaml
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Set, Type, Union, Callable
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


class FieldType(Enum):
    """Enumeration of supported field types."""
    STRING = "string"
    INTEGER = "integer" 
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    REFERENCE = "reference"


class ValidationLevel(Enum):
    """Validation levels for field validation."""
    STRICT = "strict"      # All validation rules enforced
    LENIENT = "lenient"    # Basic validation only
    DISABLED = "disabled"  # No validation


@dataclass
class FieldDefinition:
    """
    Definition of a field including validation and transformation rules.
    """
    name: Optional[str] = None
    field_type: Optional[FieldType] = None
    required: bool = False
    description: str = ""
    default_value: Any = None
    default: Any = None
    api_field_name: Optional[str] = None
    
    # Validation constraints
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    enum_values: Optional[List[Any]] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    
    # Reference information (for object references)
    reference_type: Optional[str] = None
    reference_field: Optional[str] = None
    
    # Transformation functions
    export_transform: Optional[Callable[[Any], Any]] = None
    import_transform: Optional[Callable[[Any], Any]] = None
    
    # Dependency information
    depends_on: Set[str] = None
    
    def __post_init__(self):
        """Initialize fields after creation."""
        if self.depends_on is None:
            self.depends_on = set()
        
        # Handle legacy 'default' parameter - use it if default_value is not set
        if self.default_value is None and self.default is not None:
            self.default_value = self.default
        
        # Handle case where name might be provided via api_field_name
        if self.name is None and self.api_field_name is not None:
            self.name = self.api_field_name


@dataclass(frozen=True)
class DependencyDefinition:
    """
    Definition of a dependency relationship between object types.
    """
    target_type: str              # Object type this depends on
    dependency_type: str          # Type of dependency (e.g., 'references', 'requires')
    required: bool = True         # Whether this dependency is required
    description: str = ""         # Description of the dependency


class ObjectType(ABC):
    """
    Core class for all Intersight object types.
    
    This class provides the foundation for all specific Intersight object
    implementations with comprehensive dependency management, field definitions,
    validation, and transformation capabilities.
    """
    
    def __init__(self, api_client=None, openapi_schema=None, validation_level: ValidationLevel = ValidationLevel.STRICT):
        """
        Initialize the object type.
        
        Args:
            api_client: The Intersight API client instance
            openapi_schema: The parsed OpenAPI schema for validation
            validation_level: Level of validation to apply
        """
        self.api_client = api_client
        self.openapi_schema = openapi_schema
        self.validation_level = validation_level
        
        # Field and dependency management
        self._field_definitions: Dict[str, FieldDefinition] = {}
        self._dependencies: Set[DependencyDefinition] = set()
        self._reverse_dependencies: Set[str] = set()
        
        # Transformation and validation rules
        self._validation_rules: Dict[str, List[Callable]] = defaultdict(list)
        self._transformation_rules: Dict[str, Dict[str, Callable]] = defaultdict(dict)
        
        # Initialize the object type
        self._initialize_object_type()
    
    @property
    @abstractmethod
    def object_type(self) -> str:
        """
        Return the Intersight object type string (e.g., 'organization.Organization').
        
        This must match the ObjectType field in the Intersight API.
        """
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """
        Return the human-readable display name for this object type.
        
        Used for logging and documentation purposes.
        """
        pass
    
    @property
    @abstractmethod
    def folder_path(self) -> str:
        """
        Return the folder path where this object type should be stored.
        
        Should follow the hierarchy defined in OBJECT_TYPES.md.
        Example: 'organizations' or 'policies/bios'
        """
        pass
    
    @abstractmethod
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """
        Define the fields for this object type.
        
        This method should return a dictionary mapping field names to
        FieldDefinition objects that describe the field properties,
        validation rules, and transformation functions.
        
        Returns:
            Dictionary of field name to FieldDefinition mappings
        """
        pass
    
    @abstractmethod
    def _define_dependencies(self) -> Set[DependencyDefinition]:
        """
        Define the dependencies for this object type.
        
        This method should return a set of DependencyDefinition objects
        that describe what other object types this object depends on.
        
        Returns:
            Set of DependencyDefinition objects
        """
        pass
    
    def _initialize_object_type(self):
        """Initialize the object type by loading field and dependency definitions."""
        try:
            # Load field definitions
            self._field_definitions = self._define_fields()
            logger.debug(f"Loaded {len(self._field_definitions)} field definitions for {self.object_type}")
            
            # Load dependency definitions
            self._dependencies = self._define_dependencies()
            logger.debug(f"Loaded {len(self._dependencies)} dependencies for {self.object_type}")
            
            # Validate definitions
            self._validate_definitions()
            
        except Exception as e:
            logger.error(f"Failed to initialize object type {self.object_type}: {e}")
            raise
    
    def _validate_definitions(self):
        """Validate field and dependency definitions for consistency."""
        # Validate field definitions
        for field_name, field_def in self._field_definitions.items():
            if field_def.reference_type and field_def.field_type != FieldType.REFERENCE:
                logger.warning(f"Field {field_name} has reference_type but is not REFERENCE type")
            
            if field_def.enum_values and field_def.field_type not in [FieldType.STRING, FieldType.INTEGER]:
                logger.warning(f"Field {field_name} has enum_values but type doesn't support enums")
        
        # Validate dependency definitions
        for dep in self._dependencies:
            if not dep.target_type:
                logger.warning(f"Dependency for {self.object_type} has empty target_type")
    
    # Field Management
    
    def get_field_definition(self, field_name: str) -> Optional[FieldDefinition]:
        """Get the field definition for a specific field."""
        return self._field_definitions.get(field_name)
    
    def get_all_field_definitions(self) -> Dict[str, FieldDefinition]:
        """Get all field definitions for this object type."""
        return self._field_definitions.copy()
    
    def get_required_fields(self) -> List[str]:
        """Get list of required field names."""
        return [name for name, defn in self._field_definitions.items() if defn.required]
    
    def get_user_defined_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get only user-defined fields (excluding system-managed fields).
        
        Returns:
            Dictionary of user-defined field definitions
        """
        system_fields = {
            'Moid', 'CreateTime', 'ModTime', 'SharedScope', 'Owners',
            'DomainGroupMoid', 'VersionContext', 'Ancestors', 'Parent',
            'PermissionResources', 'DisplayNames', 'DeviceRegistration',
            'RegisteredDevice', 'ClassId'
        }
        
        return {
            name: defn for name, defn in self._field_definitions.items() 
            if name not in system_fields
        }
    
    def get_reference_fields(self) -> Dict[str, FieldDefinition]:
        """Get fields that reference other objects."""
        return {
            name: defn for name, defn in self._field_definitions.items()
            if defn.field_type == FieldType.REFERENCE
        }
    
    # Dependency Management
    
    def add_dependency(self, target_type: str, dependency_type: str = "references", 
                      required: bool = True, description: str = ""):
        """
        Add a dependency on another object type.
        
        Args:
            target_type: The object type this depends on
            dependency_type: Type of dependency
            required: Whether this dependency is required
            description: Description of the dependency
        """
        dep = DependencyDefinition(
            target_type=target_type,
            dependency_type=dependency_type,
            required=required,
            description=description
        )
        self._dependencies.add(dep)
    
    def get_dependencies(self) -> Set[DependencyDefinition]:
        """Get all dependencies for this object type."""
        return self._dependencies.copy()
    
    def get_dependency_types(self) -> Set[str]:
        """Get all object types this object depends on."""
        return {dep.target_type for dep in self._dependencies}
    
    def has_dependency(self, target_type: str) -> bool:
        """Check if this object type depends on another type."""
        return any(dep.target_type == target_type for dep in self._dependencies)
    
    def get_required_dependencies(self) -> Set[str]:
        """Get required dependency types."""
        return {dep.target_type for dep in self._dependencies if dep.required}
    
    # Validation Framework
    
    def add_validation_rule(self, field_name: str, validation_func: Callable[[Any], bool]):
        """
        Add a custom validation rule for a field.
        
        Args:
            field_name: Name of the field to validate
            validation_func: Function that takes a value and returns True if valid
        """
        self._validation_rules[field_name].append(validation_func)
    
    def validate_object(self, obj: Dict[str, Any]) -> List[str]:
        """
        Validate an object against field definitions and rules.
        
        Args:
            obj: Object dictionary to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        if self.validation_level == ValidationLevel.DISABLED:
            return []
        
        errors = []
        
        # Check required fields
        required_fields = self.get_required_fields()
        for field_name in required_fields:
            if field_name not in obj or obj[field_name] is None:
                errors.append(f"Required field '{field_name}' is missing or null")
        
        # Validate each field
        for field_name, value in obj.items():
            field_def = self.get_field_definition(field_name)
            if field_def is None:
                if self.validation_level == ValidationLevel.STRICT:
                    errors.append(f"Unknown field '{field_name}' not defined in schema")
                continue
            
            # Skip validation for null values (unless required)
            if value is None:
                continue
            
            # Field-specific validation
            field_errors = self._validate_field_value(field_name, value, field_def)
            errors.extend(field_errors)
            
            # Custom validation rules
            for validation_func in self._validation_rules.get(field_name, []):
                try:
                    if not validation_func(value):
                        errors.append(f"Field '{field_name}' failed custom validation")
                except Exception as e:
                    errors.append(f"Field '{field_name}' validation error: {e}")
        
        return errors
    
    def _validate_field_value(self, field_name: str, value: Any, field_def: FieldDefinition) -> List[str]:
        """
        Validate a single field value against its definition.
        
        Args:
            field_name: The field name
            value: The field value
            field_def: The field definition
            
        Returns:
            List of validation error messages for this field
        """
        errors = []
        
        # Type validation
        if not self._validate_field_type(value, field_def.field_type):
            errors.append(f"Field '{field_name}' has incorrect type, expected {field_def.field_type.value}")
        
        # String validation
        if field_def.field_type == FieldType.STRING and isinstance(value, str):
            if field_def.min_length is not None and len(value) < field_def.min_length:
                errors.append(f"Field '{field_name}' is too short (min: {field_def.min_length})")
            
            if field_def.max_length is not None and len(value) > field_def.max_length:
                errors.append(f"Field '{field_name}' is too long (max: {field_def.max_length})")
            
            if field_def.pattern is not None:
                import re
                if not re.match(field_def.pattern, value):
                    errors.append(f"Field '{field_name}' does not match required pattern")
        
        # Numeric validation
        if field_def.field_type in [FieldType.INTEGER, FieldType.NUMBER] and isinstance(value, (int, float)):
            if field_def.minimum is not None and value < field_def.minimum:
                errors.append(f"Field '{field_name}' is below minimum value: {field_def.minimum}")
            
            if field_def.maximum is not None and value > field_def.maximum:
                errors.append(f"Field '{field_name}' exceeds maximum value: {field_def.maximum}")
        
        # Enum validation
        if field_def.enum_values is not None and value not in field_def.enum_values:
            errors.append(f"Field '{field_name}' must be one of: {field_def.enum_values}")
        
        return errors
    
    def _validate_field_type(self, value: Any, expected_type: FieldType) -> bool:
        """Validate that a value matches the expected field type."""
        if expected_type == FieldType.STRING:
            return isinstance(value, str)
        elif expected_type == FieldType.INTEGER:
            return isinstance(value, int)
        elif expected_type == FieldType.NUMBER:
            return isinstance(value, (int, float))
        elif expected_type == FieldType.BOOLEAN:
            return isinstance(value, bool)
        elif expected_type == FieldType.ARRAY:
            return isinstance(value, list)
        elif expected_type == FieldType.OBJECT:
            return isinstance(value, dict)
        elif expected_type == FieldType.REFERENCE:
            # During import, references can be strings (names) that get converted to objects later
            # During export, references are objects with Moid and ObjectType
            return isinstance(value, (dict, str))
        else:
            return True  # Unknown types pass validation
    
    # Transformation Framework
    
    def add_export_transform(self, field_name: str, transform_func: Callable[[Any], Any]):
        """
        Add a transformation function for export operations.
        
        Args:
            field_name: Name of the field to transform
            transform_func: Function that transforms the value for export
        """
        self._transformation_rules[field_name]['export'] = transform_func
    
    def add_import_transform(self, field_name: str, transform_func: Callable[[Any], Any]):
        """
        Add a transformation function for import operations.
        
        Args:
            field_name: Name of the field to transform
            transform_func: Function that transforms the value for import
        """
        self._transformation_rules[field_name]['import'] = transform_func
    
    def transform_for_export(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform an object for export operations.
        
        Args:
            obj: Object to transform
            
        Returns:
            Transformed object
        """
        transformed = obj.copy()
        
        for field_name, value in obj.items():
            field_def = self.get_field_definition(field_name)
            
            # Apply field definition export transform
            if field_def and field_def.export_transform:
                try:
                    transformed[field_name] = field_def.export_transform(value)
                except Exception as e:
                    logger.warning(f"Export transform failed for field {field_name}: {e}")
            
            # Apply custom transformation rules
            transform_func = self._transformation_rules.get(field_name, {}).get('export')
            if transform_func:
                try:
                    transformed[field_name] = transform_func(value)
                except Exception as e:
                    logger.warning(f"Custom export transform failed for field {field_name}: {e}")
        
        return transformed
    
    def transform_for_import(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform an object for import operations.
        
        Args:
            obj: Object to transform
            
        Returns:
            Transformed object
        """
        transformed = obj.copy()
        
        for field_name, value in obj.items():
            field_def = self.get_field_definition(field_name)
            
            # Apply field definition import transform
            if field_def and field_def.import_transform:
                try:
                    transformed[field_name] = field_def.import_transform(value)
                except Exception as e:
                    logger.warning(f"Import transform failed for field {field_name}: {e}")
            
            # Apply custom transformation rules
            transform_func = self._transformation_rules.get(field_name, {}).get('import')
            if transform_func:
                try:
                    transformed[field_name] = transform_func(value)
                except Exception as e:
                    logger.warning(f"Custom import transform failed for field {field_name}: {e}")
        
        return transformed
    
    # System Default Filtering
    
    def is_system_default(self, obj: Dict[str, Any]) -> bool:
        """
        Check if an object is a system-defined object that should not be managed via GitOps.
        
        System-defined objects include:
        - cisco.meta.SystemDefault: true - System default configurations  
        - cisco.meta.CiscoProvided: true - Cisco-provided policies and profiles
        
        Args:
            obj: Object to check
            
        Returns:
            True if the object is system-defined
        """
        # Handle both uppercase and lowercase tags field names
        tags = obj.get('Tags', []) or obj.get('tags', [])
        
        # Define system-defined tag patterns
        system_tags = {
            'cisco.meta.SystemDefault': 'true',
            'cisco.meta.CiscoProvided': 'true'
        }
        
        for tag in tags:
            if isinstance(tag, dict):
                # Handle both uppercase and lowercase tag field names
                key = tag.get('Key') or tag.get('key', '')
                value = tag.get('Value') or tag.get('value', '')
                
                # Check if this tag marks the object as system-defined
                if key in system_tags and str(value).lower() == system_tags[key].lower():
                    return True
        
        return False
    
    def filter_system_defaults(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter out system-defined objects from a list.
        
        This removes both system defaults and Cisco-provided objects that should
        not be managed via GitOps.
        
        Args:
            objects: List of objects to filter
            
        Returns:
            Filtered list excluding system-defined objects
        """
        return [obj for obj in objects if not self.is_system_default(obj)]
    
    # Name-based Reference Management
    
    def convert_moid_references_to_names(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MOID references to name-based references for export.
        
        Args:
            obj: Object with MOID references
            
        Returns:
            Object with name-based references
        """
        converted = obj.copy()
        reference_fields = self.get_reference_fields()
        
        for field_name, field_def in reference_fields.items():
            if field_name in converted:
                value = converted[field_name]
                
                # Handle single reference
                if isinstance(value, dict) and 'Moid' in value:
                    converted[field_name] = self._convert_single_reference_to_name(value, field_def)
                
                # Handle array of references
                elif isinstance(value, list):
                    converted[field_name] = [
                        self._convert_single_reference_to_name(ref, field_def) if isinstance(ref, dict) else ref
                        for ref in value
                    ]
        
        return converted
    
    def convert_name_references_to_moids(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert name-based references to MOID references for import.
        
        Args:
            obj: Object with name-based references
            
        Returns:
            Object with MOID references
        """
        converted = obj.copy()
        reference_fields = self.get_reference_fields()
        
        for field_name, field_def in reference_fields.items():
            if field_name in converted:
                value = converted[field_name]
                
                # Handle single reference
                if isinstance(value, dict) and 'Name' in value:
                    converted[field_name] = self._convert_single_reference_to_moid(value, field_def)
                
                # Handle array of references
                elif isinstance(value, list):
                    converted[field_name] = [
                        self._convert_single_reference_to_moid(ref, field_def) if isinstance(ref, dict) else ref
                        for ref in value
                    ]
        
        return converted
    
    def _convert_single_reference_to_name(self, ref: Dict[str, Any], field_def: FieldDefinition) -> Dict[str, Any]:
        """Convert a single MOID reference to name reference."""
        if not self.api_client or not field_def.reference_type:
            return ref
        
        try:
            # Handle both uppercase 'Moid' and lowercase 'moid' for compatibility
            moid = ref.get('Moid') or ref.get('moid')
            if moid:
                # Try the efficient resolver method first
                if hasattr(self.api_client, 'resolve_moid_to_name'):
                    name = self.api_client.resolve_moid_to_name(field_def.reference_type, moid)
                    if name:
                        return {
                            'Name': name,
                            'ObjectType': field_def.reference_type
                        }
                
                # Fallback to querying the full object
                if hasattr(self.api_client, 'get_object_by_moid'):
                    referenced_obj = self.api_client.get_object_by_moid(field_def.reference_type, moid)
                    if referenced_obj and 'Name' in referenced_obj:
                        return {
                            'Name': referenced_obj.get('Name'),
                            'ObjectType': field_def.reference_type
                        }
        except Exception as e:
            logger.warning(f"Failed to convert MOID reference to name: {e}")
        
        return ref
    
    def _convert_single_reference_to_moid(self, ref: Dict[str, Any], field_def: FieldDefinition) -> Dict[str, Any]:
        """Convert a single name reference to MOID reference.""" 
        if not self.api_client or not field_def.reference_type:
            return ref
        
        try:
            # Resolve the name to MOID
            name = ref.get('Name')
            if name:
                moid = self.api_client.resolve_name_to_moid(field_def.reference_type, name)
                if moid:
                    return {
                        'Moid': moid,
                        'ObjectType': field_def.reference_type
                    }
        except Exception as e:
            logger.warning(f"Failed to convert name reference to MOID: {e}")
        
        return ref
    
    # File Operations
    
    def generate_filename(self, obj: Dict[str, Any], organization_name: str = None) -> str:
        """
        Generate a filename for an object.
        
        Args:
            obj: The object dictionary
            organization_name: Organization name (if applicable)
            
        Returns:
            Generated filename string
        """
        name = obj.get('Name', 'unnamed')
        # Sanitize filename
        name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        name = name.replace(' ', '_')
        
        if organization_name and organization_name != 'default':
            return f"{organization_name}_{name}.yaml"
        else:
            return f"{name}.yaml"
    
    def _is_empty_value(self, value: Any) -> bool:
        """
        Check if a value is considered empty and should be excluded from export.
        
        Args:
            value: Value to check
            
        Returns:
            True if the value is empty and should be excluded
        """
        # None values are empty
        if value is None:
            return True
        
        # Empty strings are empty
        if isinstance(value, str) and value == '':
            return True
        
        # Empty lists are empty
        if isinstance(value, list) and len(value) == 0:
            return True
        
        # Empty dictionaries are empty (but not if they have keys with None values)
        if isinstance(value, dict):
            if len(value) == 0:
                return True
            # Check if all values in the dict are empty
            return all(self._is_empty_value(v) for v in value.values())
        
        # All other values (numbers, booleans, non-empty strings/lists/dicts) are not empty
        return False
    
    def _filter_empty_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter out empty values from the data dictionary.
        
        Args:
            data: Data dictionary to filter
            
        Returns:
            Filtered dictionary with empty values removed
        """
        filtered_data = {}
        
        for key, value in data.items():
            # Always keep ObjectType and Name fields, even if empty
            if key in ('ObjectType', 'Name'):
                filtered_data[key] = value
            # For other fields, only include if not empty
            elif not self._is_empty_value(value):
                # If it's a dictionary, recursively filter it
                if isinstance(value, dict):
                    filtered_value = self._filter_empty_values(value)
                    if filtered_value:  # Only include if the filtered dict is not empty
                        filtered_data[key] = filtered_value
                # If it's a list, filter out empty items
                elif isinstance(value, list):
                    filtered_list = []
                    for item in value:
                        if isinstance(item, dict):
                            filtered_item = self._filter_empty_values(item)
                            if filtered_item:  # Only include if the filtered dict is not empty
                                filtered_list.append(filtered_item)
                        elif not self._is_empty_value(item):
                            filtered_list.append(item)
                    
                    if filtered_list:  # Only include the list if it has items
                        filtered_data[key] = filtered_list
                else:
                    filtered_data[key] = value
        
        return filtered_data

    def _reorder_fields_for_export(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reorder fields according to export requirements: ObjectType first, Name second.
        Also converts ObjectType from x.y format to x format for simplified YAML.
        Filters out empty values to keep YAML files clean.
        
        Args:
            data: Object data dictionary
            
        Returns:
            Reordered and filtered dictionary with ObjectType first, Name second
        """
        # First filter out empty values
        filtered_data = self._filter_empty_values(data)
        
        ordered_data = {}
        
        # Add ObjectType first if present, converting from x.y to x format
        if 'ObjectType' in filtered_data:
            object_type = filtered_data['ObjectType']
            simplified_type = self._simplify_object_type_for_export(object_type)
            ordered_data['ObjectType'] = simplified_type
        
        # Add Name second if present
        if 'Name' in filtered_data:
            ordered_data['Name'] = filtered_data['Name']
        
        # Add all other fields
        for key, value in filtered_data.items():
            if key not in ('ObjectType', 'Name'):
                ordered_data[key] = value
        
        return ordered_data
    
    def _simplify_object_type_for_export(self, object_type: str) -> str:
        """
        Convert ObjectType from x.y format to folder-aware format for export.
        
        Examples:
            bios.Policy -> policies/bios
            organization.Organization -> organizations/organization
            boot.PrecisionPolicy -> policies/boot
            chassis.Profile -> profiles/chassis
            macpool.Pool -> pools/mac
        
        Args:
            object_type: Full object type string (e.g., "bios.Policy")
            
        Returns:
            Folder-aware object type string (e.g., "policies/bios")
        """
        # Get the simplified type (first part before the dot)
        simplified_type = object_type.split('.')[0] if '.' in object_type else object_type
        
        # Use folder path if available
        if hasattr(self, 'folder_path') and self.folder_path:
            # If folder_path already contains a specific type path (like "policies/power" or "pools/mac"),
            # and it ends with a type-specific folder, use it as-is
            folder_parts = self.folder_path.split('/')
            if len(folder_parts) >= 2:
                # For paths like "policies/power" or "pools/mac", use the full path
                return self.folder_path
            else:
                # For basic paths like "policies" or "organizations", append the simplified type
                return f"{self.folder_path}/{simplified_type}"
        
        return simplified_type
    
    def _expand_object_type_for_import(self, simplified_type: str) -> str:
        """
        Convert ObjectType from folder/x format to x.y format for import.
        
        Examples:
            policies/bios -> bios.Policy  
            organizations/organization -> organization.Organization
            profiles/chassis -> chassis.Profile
            pools/macpool -> macpool.Pool
            
        Also supports legacy format:
            bios -> bios.Policy (for backward compatibility)
        
        Args:
            simplified_type: Folder-aware or simplified object type string (e.g., "policies/bios" or "bios")
            
        Returns:
            Full object type string (e.g., "bios.Policy")
        """
        # Extract the base type from folder/type format if present
        if '/' in simplified_type:
            _, base_type = simplified_type.split('/', 1)
        else:
            base_type = simplified_type
        
        # Common mapping of base types to full types
        type_mapping = {
            # Organizations
            'organization': 'organization.Organization',
            
            # Policies
            'bios': 'bios.Policy',
            'boot': 'boot.PrecisionPolicy',
            'memory': 'memory.Policy',
            'persistent_memory': 'memory.PersistentMemoryPolicy',
            'access': 'access.Policy',
            'certificate': 'certificatemanagement.Policy',
            'deviceconnector': 'deviceconnector.Policy',
            'firmware': 'firmware.Policy',
            'ipmi': 'ipmioverlan.Policy',
            'kvm': 'kvm.Policy',
            'network': 'networkconfig.Policy',
            'ntp': 'ntp.Policy',
            'power': 'power.Policy',
            'sdcard': 'sdcard.Policy',
            'smtp': 'smtp.Policy',
            'snmp': 'snmp.Policy',
            'sol': 'sol.Policy',
            'ssh': 'ssh.Policy',
            'syslog': 'syslog.Policy',
            'thermal': 'thermal.Policy',
            'vmedia': 'vmedia.Policy',
            
            # Profiles
            'server': 'server.Profile',
            'chassis': 'chassis.Profile',
            
            # Pools
            'fcpool': 'fcpool.Pool',
            'ippool': 'ippool.Pool',
            'iqnpool': 'iqnpool.Pool',
            'macpool': 'macpool.Pool',
            'resourcepool': 'resourcepool.Pool',
            'uuidpool': 'uuidpool.Pool'
        }
        
        # Return mapped value or assume it's already in full format
        return type_mapping.get(base_type, simplified_type)

    def save_to_yaml(self, data: Dict[str, Any], file_path: str):
        """
        Save data to a YAML file with proper field ordering.
        
        Args:
            data: Data to save
            file_path: Path where to save the file
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Ensure proper field ordering (ObjectType first, Name second)
        ordered_data = self._reorder_fields_for_export(data)
        
        with open(file_path, 'w') as f:
            yaml.dump(ordered_data, f, default_flow_style=False, sort_keys=False, indent=2)
    
    def load_from_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Loaded data dictionary
        """
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    # Utility Methods
    
    def _pascal_to_snake_case(self, pascal_str: str) -> str:
        """Convert PascalCase to snake_case."""
        import re
        # Insert underscore before uppercase letters (except first) and convert to lowercase
        snake_str = re.sub('([a-z0-9])([A-Z])', r'\1_\2', pascal_str).lower()
        return snake_str
    
    def _extract_user_defined_values(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract only user-defined values from an Intersight object.
        
        Args:
            obj: The raw object dictionary from Intersight API
            
        Returns:
            Dictionary containing only user-defined values
        """
        user_fields = self.get_user_defined_fields()
        extracted = {}
        
        # Extract user-defined field values with case conversion
        for field_name, field_def in user_fields.items():
            # Try PascalCase first
            if field_name in obj and obj[field_name] is not None:
                extracted[field_name] = obj[field_name]
            else:
                # Try snake_case conversion (PascalCase -> snake_case)
                snake_case_name = self._pascal_to_snake_case(field_name)
                if snake_case_name in obj and obj[snake_case_name] is not None:
                    extracted[field_name] = obj[snake_case_name]
        
        # Always include object type for identification
        object_type_value = obj.get('ObjectType') or obj.get('object_type') or self.object_type
        extracted['ObjectType'] = object_type_value
        
        return extracted
    
    # Abstract methods that subclasses must implement
    
    @abstractmethod
    def export(self, output_dir: str) -> Dict[str, Any]:
        """
        Export objects of this type from Intersight to YAML files.
        
        Args:
            output_dir: Directory where YAML files should be saved
            
        Returns:
            Dictionary with export results (success count, errors, etc.)
        """
        pass
    
    @abstractmethod
    def import_objects(self, yaml_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Import objects of this type from YAML data to Intersight.
        
        Args:
            yaml_data: List of object dictionaries from YAML files
            
        Returns:
            Dictionary with import results (created, updated, errors, etc.)
        """
        pass
    
    @abstractmethod
    def document(self) -> Dict[str, Any]:
        """
        Generate documentation for this object type.
        
        Returns:
            Dictionary containing documentation information
        """
        pass