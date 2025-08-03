"""
OpenAPI schema parser for Intersight objects.

This module provides utilities to parse the Intersight OpenAPI specification
and extract field definitions, validation rules, and schema information
for use by the GitOps tool.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

logger = logging.getLogger(__name__)


class OpenAPIParser:
    """
    Parser for Intersight OpenAPI specification.
    
    This class loads and parses the OpenAPI JSON file to provide
    schema information for Intersight objects.
    """
    
    def __init__(self, openapi_file_path: str):
        """
        Initialize the OpenAPI parser.
        
        Args:
            openapi_file_path: Path to the openapi.json file
        """
        self.openapi_file_path = openapi_file_path
        self.schema = None
        self._load_schema()
    
    def _load_schema(self):
        """Load the OpenAPI schema from file."""
        try:
            with open(self.openapi_file_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
            logger.info(f"Loaded OpenAPI schema from {self.openapi_file_path}")
        except Exception as e:
            logger.error(f"Failed to load OpenAPI schema: {e}")
            raise
    
    def get_object_schema(self, object_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the schema definition for a specific object type.
        
        Args:
            object_type: The Intersight object type (e.g., 'organization.Organization')
            
        Returns:
            Schema definition dictionary or None if not found
        """
        if not self.schema or 'components' not in self.schema:
            return None
        
        schemas = self.schema['components'].get('schemas', {})
        return schemas.get(object_type)
    
    def get_field_definitions(self, object_type: str) -> Dict[str, Any]:
        """
        Get field definitions for an object type.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Dictionary of field definitions
        """
        schema = self.get_object_schema(object_type)
        if not schema:
            return {}
        
        fields = {}
        
        # Handle allOf schemas (common in Intersight)
        if 'allOf' in schema:
            for subschema in schema['allOf']:
                if 'properties' in subschema:
                    fields.update(subschema['properties'])
                elif '$ref' in subschema:
                    # Resolve references
                    ref_schema = self._resolve_reference(subschema['$ref'])
                    if ref_schema and 'properties' in ref_schema:
                        fields.update(ref_schema['properties'])
        
        # Handle direct properties
        if 'properties' in schema:
            fields.update(schema['properties'])
        
        return fields
    
    def _resolve_reference(self, ref: str) -> Optional[Dict[str, Any]]:
        """
        Resolve a JSON schema reference.
        
        Args:
            ref: Reference string (e.g., '#/components/schemas/mo.BaseMo')
            
        Returns:
            Referenced schema definition or None
        """
        if not ref.startswith('#/'):
            return None
        
        # Parse reference path
        path_parts = ref[2:].split('/')  # Remove '#/' prefix
        
        current = self.schema
        for part in path_parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        
        return current if isinstance(current, dict) else None
    
    def get_required_fields(self, object_type: str) -> Set[str]:
        """
        Get the set of required fields for an object type.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Set of required field names
        """
        schema = self.get_object_schema(object_type)
        if not schema:
            return set()
        
        required = set()
        
        # Handle allOf schemas
        if 'allOf' in schema:
            for subschema in schema['allOf']:
                if 'required' in subschema:
                    required.update(subschema['required'])
                elif '$ref' in subschema:
                    ref_schema = self._resolve_reference(subschema['$ref'])
                    if ref_schema and 'required' in ref_schema:
                        required.update(ref_schema['required'])
        
        # Handle direct required fields
        if 'required' in schema:
            required.update(schema['required'])
        
        return required
    
    def get_field_constraints(self, object_type: str, field_name: str) -> Dict[str, Any]:
        """
        Get validation constraints for a specific field.
        
        Args:
            object_type: The Intersight object type
            field_name: The field name
            
        Returns:
            Dictionary of constraints (pattern, enum, min/max, etc.)
        """
        fields = self.get_field_definitions(object_type)
        field_def = fields.get(field_name, {})
        
        constraints = {}
        
        # String constraints
        if 'pattern' in field_def:
            constraints['pattern'] = field_def['pattern']
        if 'minLength' in field_def:
            constraints['min_length'] = field_def['minLength']
        if 'maxLength' in field_def:
            constraints['max_length'] = field_def['maxLength']
        
        # Numeric constraints
        if 'minimum' in field_def:
            constraints['minimum'] = field_def['minimum']
        if 'maximum' in field_def:
            constraints['maximum'] = field_def['maximum']
        
        # Enum constraints
        if 'enum' in field_def:
            constraints['enum'] = field_def['enum']
        
        # Type information
        if 'type' in field_def:
            constraints['type'] = field_def['type']
        
        # Read-only flag
        if 'readOnly' in field_def:
            constraints['read_only'] = field_def['readOnly']
        
        return constraints
    
    def is_user_defined_field(self, object_type: str, field_name: str) -> bool:
        """
        Determine if a field is user-defined based on schema analysis.
        
        Args:
            object_type: The Intersight object type
            field_name: The field name
            
        Returns:
            True if the field is user-defined, False if system-managed
        """
        field_def = self.get_field_definitions(object_type).get(field_name, {})
        
        # Read-only fields are not user-defined
        if field_def.get('readOnly', False):
            return False
        
        # System-managed fields (common across all Intersight objects)
        system_fields = {
            'Moid', 'CreateTime', 'ModTime', 'SharedScope', 'Owners',
            'DomainGroupMoid', 'VersionContext', 'Ancestors', 'Parent',
            'PermissionResources', 'DisplayNames', 'DeviceRegistration',
            'RegisteredDevice'
        }
        
        if field_name in system_fields:
            return False
        
        # ClassId and ObjectType are system-managed but needed for object identification
        if field_name in ['ClassId', 'ObjectType']:
            return False
        
        return True
    
    def get_user_defined_fields(self, object_type: str) -> Dict[str, Any]:
        """
        Get only user-defined fields for an object type.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Dictionary of user-defined field definitions
        """
        all_fields = self.get_field_definitions(object_type)
        return {
            name: definition
            for name, definition in all_fields.items()
            if self.is_user_defined_field(object_type, name)
        }
    
    def get_object_description(self, object_type: str) -> Optional[str]:
        """
        Get the description for an object type.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Description string or None
        """
        schema = self.get_object_schema(object_type)
        return schema.get('description') if schema else None
    
    def get_field_description(self, object_type: str, field_name: str) -> Optional[str]:
        """
        Get the description for a specific field.
        
        Args:
            object_type: The Intersight object type
            field_name: The field name
            
        Returns:
            Field description string or None
        """
        fields = self.get_field_definitions(object_type)
        field_def = fields.get(field_name, {})
        return field_def.get('description')
    
    def get_all_object_types(self) -> List[str]:
        """
        Get all available object types from the schema.
        
        Returns:
            List of object type strings
        """
        if not self.schema or 'components' not in self.schema:
            return []
        
        schemas = self.schema['components'].get('schemas', {})
        
        # Filter for actual Intersight object types (contain '.')
        object_types = [
            name for name in schemas.keys()
            if '.' in name and not name.startswith('telemetry.')
        ]
        
        return sorted(object_types)
    
    def get_relationship_fields(self, object_type: str) -> Dict[str, Any]:
        """
        Get fields that represent relationships to other objects.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Dictionary of relationship field definitions
        """
        fields = self.get_field_definitions(object_type)
        relationships = {}
        
        for field_name, field_def in fields.items():
            # Check if field is a relationship (contains $ref to .Relationship)
            if '$ref' in field_def and '.Relationship' in field_def['$ref']:
                relationships[field_name] = field_def
            elif isinstance(field_def.get('items'), dict) and '$ref' in field_def['items']:
                # Array of relationships
                if '.Relationship' in field_def['items']['$ref']:
                    relationships[field_name] = field_def
        
        return relationships
    
    def extract_object_dependencies(self, object_type: str) -> Set[str]:
        """
        Extract object dependencies based on relationship fields.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Set of object types this object depends on
        """
        relationships = self.get_relationship_fields(object_type)
        dependencies = set()
        
        for field_name, field_def in relationships.items():
            # Extract the target object type from relationship reference
            if '$ref' in field_def:
                ref = field_def['$ref']
                # Parse references like '#/components/schemas/organization.Organization.Relationship'
                if '.Relationship' in ref:
                    target_type = ref.split('/')[-1].replace('.Relationship', '')
                    dependencies.add(target_type)
            elif isinstance(field_def.get('items'), dict) and '$ref' in field_def['items']:
                ref = field_def['items']['$ref']
                if '.Relationship' in ref:
                    target_type = ref.split('/')[-1].replace('.Relationship', '')
                    dependencies.add(target_type)
        
        return dependencies
    
    def validate_object_against_schema(self, object_type: str, obj_data: Dict[str, Any]) -> List[str]:
        """
        Validate an object against its OpenAPI schema.
        
        Args:
            object_type: The Intersight object type
            obj_data: Object data to validate
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Get schema information
        required_fields = self.get_required_fields(object_type)
        field_definitions = self.get_field_definitions(object_type)
        
        # Check required fields
        for field in required_fields:
            if field not in obj_data:
                errors.append(f"Required field '{field}' is missing")
        
        # Validate field values
        for field_name, value in obj_data.items():
            if field_name in field_definitions:
                field_errors = self._validate_field_value(
                    field_name, value, field_definitions[field_name]
                )
                errors.extend(field_errors)
        
        return errors
    
    def _validate_field_value(self, field_name: str, value: Any, field_def: Dict[str, Any]) -> List[str]:
        """
        Validate a single field value against its definition.
        
        Args:
            field_name: The field name
            value: The field value
            field_def: The field definition from schema
            
        Returns:
            List of validation error messages for this field
        """
        errors = []
        
        if value is None:
            return errors  # Null values are generally allowed unless required
        
        # Type validation
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
        
        # String-specific validation
        if isinstance(value, str):
            if 'pattern' in field_def:
                import re
                if not re.match(field_def['pattern'], value):
                    errors.append(f"Field '{field_name}' does not match required pattern: {field_def['pattern']}")
            
            if 'minLength' in field_def and len(value) < field_def['minLength']:
                errors.append(f"Field '{field_name}' is too short (min: {field_def['minLength']})")
            
            if 'maxLength' in field_def and len(value) > field_def['maxLength']:
                errors.append(f"Field '{field_name}' is too long (max: {field_def['maxLength']})")
        
        # Numeric validation
        if isinstance(value, (int, float)):
            if 'minimum' in field_def and value < field_def['minimum']:
                errors.append(f"Field '{field_name}' is below minimum value: {field_def['minimum']}")
            
            if 'maximum' in field_def and value > field_def['maximum']:
                errors.append(f"Field '{field_name}' exceeds maximum value: {field_def['maximum']}")
        
        # Enum validation
        if 'enum' in field_def and value not in field_def['enum']:
            errors.append(f"Field '{field_name}' must be one of: {field_def['enum']}")
        
        return errors