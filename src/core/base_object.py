"""
Base class for all Intersight objects.

This module provides the core BaseIntersightObject class that all specific
Intersight object types must inherit from. It defines the common interface
for export, import, and documentation functionality.
"""

import os
import json
import yaml
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Set, Type
from pathlib import Path
import logging

from .exceptions import (
    ObjectValidationError, YAMLParsingError, FileSystemError, 
    ExportError, ImportError, SchemaValidationError
)
from .error_handler import handle_errors, safe_execute, get_global_error_handler
from .validation import ObjectValidator, create_validator_from_schema

logger = logging.getLogger(__name__)


class BaseIntersightObject(ABC):
    """
    Base class for all Intersight objects that can be exported, imported, and documented.
    
    This class provides the common interface and functionality that all specific
    Intersight object implementations must inherit and implement.
    """
    
    def __init__(self, api_client=None, openapi_schema=None):
        """
        Initialize the base Intersight object.
        
        Args:
            api_client: The Intersight API client instance
            openapi_schema: The parsed OpenAPI schema for this object type
        """
        self.api_client = api_client
        self.openapi_schema = openapi_schema
        self._field_definitions = None
        self._dependencies = set()
        self._validator = None
        
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
    
    @property
    def field_definitions(self) -> Dict[str, Any]:
        """
        Get the field definitions for this object type from OpenAPI schema.
        
        Returns:
            Dictionary containing field definitions with types, constraints, etc.
        """
        if self._field_definitions is None:
            self._field_definitions = self._extract_field_definitions()
        return self._field_definitions
    
    @property
    def dependencies(self) -> Set[str]:
        """
        Get the set of object types this object depends on.
        
        Returns:
            Set of object type strings that must be created before this object.
        """
        return self._dependencies
    
    @property
    def validator(self) -> ObjectValidator:
        """
        Get the validator instance for this object type.
        
        Returns:
            ObjectValidator instance configured for this object type
        """
        if self._validator is None:
            if self.openapi_schema and 'components' in self.openapi_schema:
                schema = self.openapi_schema['components']['schemas'].get(self.object_type, {})
                self._validator = create_validator_from_schema(schema, self.object_type)
            else:
                # Fallback to basic validator if no schema available
                self._validator = ObjectValidator({}, set())
        return self._validator
    
    def add_dependency(self, object_type: str):
        """
        Add a dependency on another object type.
        
        Args:
            object_type: The object type string this object depends on
        """
        self._dependencies.add(object_type)
    
    def _extract_field_definitions(self) -> Dict[str, Any]:
        """
        Extract field definitions from the OpenAPI schema.
        
        Returns:
            Dictionary of field definitions
        """
        if not self.openapi_schema:
            return {}
            
        try:
            schema_ref = f"#/components/schemas/{self.object_type}"
            if 'components' in self.openapi_schema and 'schemas' in self.openapi_schema['components']:
                schema = self.openapi_schema['components']['schemas'].get(self.object_type, {})
                
                # Handle allOf schemas
                if 'allOf' in schema:
                    fields = {}
                    for subschema in schema['allOf']:
                        if 'properties' in subschema:
                            fields.update(subschema['properties'])
                    return fields
                
                # Handle direct properties
                return schema.get('properties', {})
                
        except Exception as e:
            logger.warning(f"Failed to extract field definitions for {self.object_type}: {e}")
            
        return {}
    
    def _is_user_defined_field(self, field_name: str, field_def: Dict[str, Any]) -> bool:
        """
        Determine if a field is user-defined based on OpenAPI schema.
        
        Args:
            field_name: The field name
            field_def: The field definition from OpenAPI schema
            
        Returns:
            True if the field is user-defined, False otherwise
        """
        # Read-only fields are not user-defined
        if field_def.get('readOnly', False):
            return False
            
        # System-managed fields are not user-defined
        system_fields = {
            'Moid', 'CreateTime', 'ModTime', 'SharedScope', 'Owners',
            'DomainGroupMoid', 'VersionContext', 'Ancestors', 'Parent'
        }
        if field_name in system_fields:
            return False
            
        return True
    
    def get_user_defined_fields(self) -> Dict[str, Any]:
        """
        Get only the user-defined fields for this object type.
        
        Returns:
            Dictionary containing only user-defined field definitions
        """
        all_fields = self.field_definitions
        return {
            name: definition 
            for name, definition in all_fields.items() 
            if self._is_user_defined_field(name, definition)
        }
    
    def _filter_system_defaults(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter out system default objects based on tags.
        
        Args:
            objects: List of object dictionaries from Intersight API
            
        Returns:
            Filtered list excluding system default objects
        """
        filtered = []
        for obj in objects:
            tags = obj.get('Tags', [])
            is_system_default = any(
                tag.get('Key') == 'cisco.meta.SystemDefault' and tag.get('Value') == 'true'
                for tag in tags
            )
            if not is_system_default:
                filtered.append(obj)
        
        return filtered
    
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
        
        for field_name in user_fields:
            if field_name in obj and obj[field_name] is not None:
                extracted[field_name] = obj[field_name]
        
        # Always include object type for identification
        extracted['ObjectType'] = obj.get('ObjectType', self.object_type)
        
        return extracted
    
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
    
    def export_streaming(self, output_dir: str, progress_callback=None) -> Dict[str, Any]:
        """
        Export objects using streaming approach for large datasets.
        
        This method provides a streaming export that:
        - Processes objects in batches to reduce memory usage
        - Supports progress reporting via callback
        - Handles large datasets efficiently
        
        Args:
            output_dir: Directory where YAML files should be saved
            progress_callback: Optional callback function for progress reporting
            
        Returns:
            Dictionary with export results (success count, errors, etc.)
        """
        results = {
            'success_count': 0,
            'error_count': 0,
            'errors': [],
            'exported_files': []
        }
        
        try:
            logger.info(f"Starting streaming export of {self.display_name}...")
            
            # Create output directory for this object type
            folder_path = os.path.join(output_dir, self.folder_path)
            
            processed_count = 0
            
            # Query objects using streaming approach
            for batch in self.api_client.query_objects_streaming(self.object_type):
                # Filter out system default objects
                filtered_batch = self._filter_system_defaults(batch)
                
                if not filtered_batch:
                    continue
                
                # Process each object in the batch
                for obj in filtered_batch:
                    try:
                        # Extract user-defined values
                        yaml_data = self._extract_user_defined_values(obj)
                        
                        # Generate filename
                        org_name = self._extract_org_name_from_object(obj)
                        filename = self._generate_filename(obj, org_name)
                        file_path = os.path.join(folder_path, filename)
                        
                        # Save to YAML file
                        self._save_to_yaml(yaml_data, file_path)
                        
                        results['success_count'] += 1
                        results['exported_files'].append(file_path)
                        processed_count += 1
                        
                        # Report progress if callback provided
                        if progress_callback:
                            progress_callback(processed_count, self.object_type)
                        
                    except Exception as e:
                        error_msg = f"Failed to export {self.object_type} object {obj.get('Name', 'unnamed')}: {e}"
                        logger.error(error_msg)
                        results['errors'].append(error_msg)
                        results['error_count'] += 1
                
                # Optional: Add small delay between batches to prevent API rate limiting
                if processed_count > 0 and processed_count % 1000 == 0:
                    import time
                    time.sleep(0.1)  # 100ms pause every 1000 objects
            
            logger.info(f"Streaming export completed: {results['success_count']} {self.display_name} objects exported")
            
        except Exception as e:
            error_msg = f"Failed to export {self.object_type} objects: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['error_count'] += 1
        
        return results
    
    def _extract_org_name_from_object(self, obj: Dict[str, Any]) -> str:
        """
        Extract organization name from an object for filename generation.
        
        Args:
            obj: The object dictionary
            
        Returns:
            Organization name or 'default'
        """
        # Try to get organization from various possible fields
        if 'Organization' in obj and isinstance(obj['Organization'], dict):
            return obj['Organization'].get('Name', 'default')
        elif 'OrganizationMoid' in obj and self.api_client.reference_resolver:
            # Try to resolve organization MOID to name
            org_name = self.api_client.reference_resolver.resolve_moid_to_name(
                obj['OrganizationMoid'],
                'organization.Organization'
            )
            return org_name if org_name else 'default'
        else:
            return 'default'
    
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
    
    def _generate_filename(self, obj: Dict[str, Any], org_name: str = None) -> str:
        """
        Generate a filename for an object based on organization and object name.
        
        Args:
            obj: The object dictionary
            org_name: Organization name (if applicable)
            
        Returns:
            Generated filename string
        """
        name = obj.get('Name', 'unnamed')
        # Sanitize filename
        name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        name = name.replace(' ', '_')
        
        if org_name and org_name != 'default':
            return f"{org_name}_{name}.yaml"
        else:
            return f"{name}.yaml"
    
    def _save_to_yaml(self, data: Dict[str, Any], file_path: str):
        """
        Save data to a YAML file.
        
        This method creates the directory structure only when actually saving a file,
        ensuring that folders are only created when they contain YAML files.
        
        Args:
            data: Data to save
            file_path: Path where to save the file
        """
        try:
            # Create directory only when we're actually saving a file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
                
        except PermissionError as e:
            raise FileSystemError(
                f"Permission denied writing to file: {file_path}",
                file_path=file_path,
                operation="write",
                cause=e
            )
        except OSError as e:
            raise FileSystemError(
                f"Failed to write YAML file: {file_path}",
                file_path=file_path,
                operation="write",
                cause=e
            )
        except yaml.YAMLError as e:
            raise YAMLParsingError(
                f"Failed to serialize data to YAML: {e}",
                file_path=file_path,
                cause=e
            )
    
    def _load_from_yaml(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from a YAML file.
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Loaded data dictionary
        """
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError as e:
            raise FileSystemError(
                f"YAML file not found: {file_path}",
                file_path=file_path,
                operation="read",
                cause=e
            )
        except PermissionError as e:
            raise FileSystemError(
                f"Permission denied reading YAML file: {file_path}",
                file_path=file_path,
                operation="read",
                cause=e
            )
        except yaml.YAMLError as e:
            raise YAMLParsingError(
                f"Failed to parse YAML file: {file_path}",
                file_path=file_path,
                cause=e
            )
    
    def validate_object(self, obj: Dict[str, Any]) -> List[str]:
        """
        Validate an object against the OpenAPI schema using the comprehensive validation framework.
        
        Args:
            obj: Object dictionary to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        try:
            # Use the comprehensive validator
            return self.validator.validate(obj)
        except Exception as e:
            logger.error(f"Object validation error for {self.object_type}: {e}")
            return [f"Validation failed: {e}"]
    
    def is_valid_object(self, obj: Dict[str, Any]) -> bool:
        """
        Check if an object is valid according to the OpenAPI schema.
        
        Args:
            obj: Object dictionary to validate
            
        Returns:
            True if object is valid, False otherwise
        """
        try:
            return self.validator.is_valid(obj)
        except Exception as e:
            logger.error(f"Object validation check failed for {self.object_type}: {e}")
            return False
    
    def validate_and_raise(self, obj: Dict[str, Any], operation: str = "validation"):
        """
        Validate an object and raise an exception if validation fails.
        
        Args:
            obj: Object dictionary to validate
            operation: Description of the operation being performed
            
        Raises:
            ObjectValidationError: If validation fails
        """
        errors = self.validate_object(obj)
        if errors:
            object_name = obj.get('Name', 'unnamed')
            raise ObjectValidationError(
                f"Object validation failed during {operation}",
                object_name=object_name,
                object_type=self.object_type,
                validation_errors=errors
            )