"""
Schema integration utilities for OpenAPI and ObjectType integration.

This module provides utilities to automatically generate field definitions
and dependency information from OpenAPI schemas for use with the core
ObjectType system.
"""

import logging
from typing import Dict, Any, List, Set, Optional, Callable
from ..core.object_type import FieldDefinition, FieldType, DependencyDefinition
from .openapi_parser import OpenAPIParser

logger = logging.getLogger(__name__)


class SchemaIntegrator:
    """
    Integrates OpenAPI schemas with the ObjectType system.
    
    This class provides methods to automatically generate FieldDefinition
    and DependencyDefinition objects from OpenAPI schema definitions.
    """
    
    def __init__(self, openapi_parser: OpenAPIParser):
        """
        Initialize the schema integrator.
        
        Args:
            openapi_parser: OpenAPI parser instance
        """
        self.openapi_parser = openapi_parser
        self.logger = logging.getLogger(__name__)
    
    def generate_field_definitions(self, object_type: str, 
                                 user_defined_only: bool = True,
                                 custom_transforms: Optional[Dict[str, Dict[str, Callable]]] = None) -> Dict[str, FieldDefinition]:
        """
        Generate field definitions from OpenAPI schema.
        
        Args:
            object_type: The Intersight object type (e.g., 'organization.Organization')
            user_defined_only: If True, only include user-defined fields
            custom_transforms: Optional custom transformation functions
            
        Returns:
            Dictionary mapping field names to FieldDefinition objects
        """
        field_definitions = {}
        
        try:
            # Get field definitions from OpenAPI schema
            if user_defined_only:
                schema_fields = self.openapi_parser.get_user_defined_fields(object_type)
            else:
                schema_fields = self.openapi_parser.get_field_definitions(object_type)
            
            # Convert each schema field to a FieldDefinition
            for field_name, field_schema in schema_fields.items():
                field_def = self._create_field_definition(field_name, field_schema, custom_transforms)
                if field_def:
                    field_definitions[field_name] = field_def
            
            self.logger.debug(f"Generated {len(field_definitions)} field definitions for {object_type}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate field definitions for {object_type}: {e}")
        
        return field_definitions
    
    def _create_field_definition(self, field_name: str, field_schema: Dict[str, Any],
                               custom_transforms: Optional[Dict[str, Dict[str, Callable]]] = None) -> Optional[FieldDefinition]:
        """
        Create a FieldDefinition from an OpenAPI field schema.
        
        Args:
            field_name: Name of the field
            field_schema: OpenAPI schema definition for the field
            custom_transforms: Optional custom transformation functions
            
        Returns:
            FieldDefinition object or None if creation fails
        """
        try:
            # Determine field type
            field_type = self._map_openapi_type_to_field_type(field_schema)
            
            # Extract basic properties
            description = field_schema.get('description', '')
            required = field_schema.get('required', False)  # Note: OpenAPI required is handled at object level
            
            # Extract validation constraints
            min_length = field_schema.get('minLength')
            max_length = field_schema.get('maxLength')
            pattern = field_schema.get('pattern')
            enum_values = field_schema.get('enum')
            minimum = field_schema.get('minimum')
            maximum = field_schema.get('maximum')
            
            # Handle reference types
            reference_type = None
            reference_field = None
            if '$ref' in field_schema:
                reference_type = self._extract_reference_type(field_schema['$ref'])
            elif field_schema.get('type') == 'array' and 'items' in field_schema:
                if '$ref' in field_schema['items']:
                    reference_type = self._extract_reference_type(field_schema['items']['$ref'])
                    field_type = FieldType.ARRAY  # Array of references
            
            # Get custom transformations if provided
            export_transform = None
            import_transform = None
            if custom_transforms and field_name in custom_transforms:
                transforms = custom_transforms[field_name]
                export_transform = transforms.get('export')
                import_transform = transforms.get('import')
            
            # Create field definition
            field_def = FieldDefinition(
                name=field_name,
                field_type=field_type,
                required=required,
                description=description,
                min_length=min_length,
                max_length=max_length,
                pattern=pattern,
                enum_values=enum_values,
                minimum=minimum,
                maximum=maximum,
                reference_type=reference_type,
                reference_field=reference_field,
                export_transform=export_transform,
                import_transform=import_transform
            )
            
            return field_def
            
        except Exception as e:
            self.logger.warning(f"Failed to create field definition for {field_name}: {e}")
            return None
    
    def _map_openapi_type_to_field_type(self, field_schema: Dict[str, Any]) -> FieldType:
        """
        Map OpenAPI type to FieldType enum.
        
        Args:
            field_schema: OpenAPI field schema
            
        Returns:
            Corresponding FieldType enum value
        """
        openapi_type = field_schema.get('type', 'string')
        
        # Handle references
        if '$ref' in field_schema:
            if '.Relationship' in field_schema['$ref']:
                return FieldType.REFERENCE
            else:
                return FieldType.OBJECT
        
        # Map basic types
        type_mapping = {
            'string': FieldType.STRING,
            'integer': FieldType.INTEGER,
            'number': FieldType.NUMBER,
            'boolean': FieldType.BOOLEAN,
            'array': FieldType.ARRAY,
            'object': FieldType.OBJECT
        }
        
        return type_mapping.get(openapi_type, FieldType.STRING)
    
    def _extract_reference_type(self, ref: str) -> Optional[str]:
        """
        Extract the object type from an OpenAPI reference.
        
        Args:
            ref: OpenAPI reference string (e.g., '#/components/schemas/organization.Organization.Relationship')
            
        Returns:
            Object type string or None
        """
        try:
            # Parse reference like '#/components/schemas/organization.Organization.Relationship'
            if ref.startswith('#/components/schemas/'):
                schema_name = ref.split('/')[-1]
                
                # Remove .Relationship suffix if present
                if schema_name.endswith('.Relationship'):
                    return schema_name[:-len('.Relationship')]
                
                return schema_name
        except Exception as e:
            self.logger.warning(f"Failed to extract reference type from {ref}: {e}")
        
        return None
    
    def generate_dependency_definitions(self, object_type: str) -> Set[DependencyDefinition]:
        """
        Generate dependency definitions from OpenAPI schema relationships.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Set of DependencyDefinition objects
        """
        dependencies = set()
        
        try:
            # Get relationship fields from the schema
            relationship_fields = self.openapi_parser.get_relationship_fields(object_type)
            
            for field_name, field_schema in relationship_fields.items():
                # Extract dependency information from relationship
                target_types = self._extract_dependency_targets(field_schema)
                
                for target_type in target_types:
                    dependency = DependencyDefinition(
                        target_type=target_type,
                        dependency_type='references',
                        required=field_schema.get('required', False),
                        description=f"References {target_type} via {field_name} field"
                    )
                    dependencies.add(dependency)
            
            self.logger.debug(f"Generated {len(dependencies)} dependency definitions for {object_type}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate dependency definitions for {object_type}: {e}")
        
        return dependencies
    
    def _extract_dependency_targets(self, field_schema: Dict[str, Any]) -> List[str]:
        """
        Extract dependency target types from a relationship field schema.
        
        Args:
            field_schema: OpenAPI field schema for a relationship
            
        Returns:
            List of target object type strings
        """
        targets = []
        
        try:
            # Handle single reference
            if '$ref' in field_schema:
                target = self._extract_reference_type(field_schema['$ref'])
                if target:
                    targets.append(target)
            
            # Handle array of references
            elif field_schema.get('type') == 'array' and 'items' in field_schema:
                if '$ref' in field_schema['items']:
                    target = self._extract_reference_type(field_schema['items']['$ref'])
                    if target:
                        targets.append(target)
        
        except Exception as e:
            self.logger.warning(f"Failed to extract dependency targets: {e}")
        
        return targets
    
    def create_openapi_based_object_type(self, object_type: str, 
                                       display_name: str,
                                       folder_path: str,
                                       custom_transforms: Optional[Dict[str, Dict[str, Callable]]] = None) -> type:
        """
        Create an ObjectType class dynamically from OpenAPI schema.
        
        Args:
            object_type: The Intersight object type
            display_name: Human-readable display name
            folder_path: Folder path for storing files
            custom_transforms: Optional custom transformation functions
            
        Returns:
            Dynamically created ObjectType class
        """
        from ..core.object_type import ObjectType
        
        # Generate field and dependency definitions
        field_definitions = self.generate_field_definitions(object_type, True, custom_transforms)
        dependency_definitions = self.generate_dependency_definitions(object_type)
        
        class DynamicObjectType(ObjectType):
            """Dynamically created ObjectType from OpenAPI schema."""
            
            @property
            def object_type(self) -> str:
                return object_type
            
            @property
            def display_name(self) -> str:
                return display_name
            
            @property
            def folder_path(self) -> str:
                return folder_path
            
            def _define_fields(self) -> Dict[str, FieldDefinition]:
                return field_definitions
            
            def _define_dependencies(self) -> Set[DependencyDefinition]:
                return dependency_definitions
            
            def export(self, output_dir: str) -> Dict[str, Any]:
                """Default export implementation - should be overridden."""
                return {
                    'success_count': 0,
                    'error_count': 1,
                    'errors': [f'Export not implemented for {object_type}'],
                    'exported_files': []
                }
            
            def import_objects(self, yaml_data: List[Dict[str, Any]]) -> Dict[str, Any]:
                """Default import implementation - should be overridden."""
                return {
                    'created_count': 0,
                    'updated_count': 0,
                    'deleted_count': 0,
                    'error_count': 1,
                    'errors': [f'Import not implemented for {object_type}'],
                    'warnings': []
                }
            
            def document(self) -> Dict[str, Any]:
                """Generate documentation based on field definitions."""
                # Create field documentation
                field_docs = {}
                for field_name, field_def in field_definitions.items():
                    constraints = {}
                    if field_def.min_length is not None:
                        constraints['min_length'] = field_def.min_length
                    if field_def.max_length is not None:
                        constraints['max_length'] = field_def.max_length
                    if field_def.pattern is not None:
                        constraints['pattern'] = field_def.pattern
                    if field_def.enum_values is not None:
                        constraints['allowed_values'] = field_def.enum_values
                    
                    field_docs[field_name] = {
                        'type': field_def.field_type.value,
                        'description': field_def.description or 'No description available',
                        'required': field_def.required,
                        'constraints': constraints
                    }
                
                # Create example YAML
                example = {'ObjectType': object_type}
                
                # Add some example fields
                for field_name, field_def in list(field_definitions.items())[:3]:  # First 3 fields
                    if field_def.field_type == FieldType.STRING:
                        example[field_name] = f"example-{field_name.lower()}"
                    elif field_def.field_type == FieldType.INTEGER:
                        example[field_name] = 1
                    elif field_def.field_type == FieldType.BOOLEAN:
                        example[field_name] = True
                
                return {
                    'object_type': object_type,
                    'display_name': display_name,
                    'description': f'Auto-generated from OpenAPI schema for {object_type}',
                    'folder_path': folder_path,
                    'fields': field_docs,
                    'example': example,
                    'dependencies': [dep.target_type for dep in dependency_definitions]
                }
        
        # Set the class name
        DynamicObjectType.__name__ = f"{object_type.replace('.', '')}"
        DynamicObjectType.__qualname__ = DynamicObjectType.__name__
        
        return DynamicObjectType


def create_schema_based_object_types(openapi_file_path: str, 
                                    object_type_configs: List[Dict[str, Any]]) -> List[type]:
    """
    Create multiple ObjectType classes from OpenAPI schema.
    
    Args:
        openapi_file_path: Path to the OpenAPI JSON file
        object_type_configs: List of configuration dictionaries for each object type
                           Each dict should contain: object_type, display_name, folder_path
                           
    Returns:
        List of dynamically created ObjectType classes
    """
    # Initialize the OpenAPI parser
    openapi_parser = OpenAPIParser(openapi_file_path)
    integrator = SchemaIntegrator(openapi_parser)
    
    created_classes = []
    
    for config in object_type_configs:
        try:
            object_type_class = integrator.create_openapi_based_object_type(
                object_type=config['object_type'],
                display_name=config['display_name'],
                folder_path=config['folder_path'],
                custom_transforms=config.get('custom_transforms')
            )
            created_classes.append(object_type_class)
            
            logger.info(f"Created ObjectType class for {config['object_type']}")
            
        except Exception as e:
            logger.error(f"Failed to create ObjectType class for {config.get('object_type', 'unknown')}: {e}")
    
    return created_classes