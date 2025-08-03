"""
Organization object implementation.

This module implements the Organization class for handling Cisco Intersight
organization objects in the GitOps workflow.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

from src.core.object_type import ObjectType, FieldDefinition, FieldType, DependencyDefinition, ValidationLevel

logger = logging.getLogger(__name__)


class Organization(ObjectType):
    """
    Implementation for Intersight Organization objects.
    
    Organizations provide multi-tenancy within an account and are foundational
    to the Intersight object hierarchy. Most other objects are scoped to an organization.
    """
    
    def __init__(self, api_client=None, openapi_schema=None, validation_level=ValidationLevel.STRICT):
        """Initialize the Organization object type."""
        super().__init__(api_client, openapi_schema, validation_level)
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "organization.Organization"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Organization"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing organization YAML files."""
        return "organizations"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Organization objects."""
        return {
            'Name': FieldDefinition(
                name='Name',
                field_type=FieldType.STRING,
                required=True,
                description='The name of the organization',
                min_length=1,
                max_length=64,
                pattern=r'^[a-zA-Z0-9_.:-]{1,64}$'
            ),
            'Description': FieldDefinition(
                name='Description',
                field_type=FieldType.STRING,
                required=False,
                description='The informative description about the usage of this organization'
            ),
            'ObjectType': FieldDefinition(
                name='ObjectType',
                field_type=FieldType.STRING,
                required=True,
                description='The concrete type of this complex type'
            ),
            'ResourceGroups': FieldDefinition(
                name='ResourceGroups',
                field_type=FieldType.ARRAY,
                required=False,
                description='Array of resource group names associated with this organization'
            ),
            'Tags': FieldDefinition(
                name='Tags',
                field_type=FieldType.ARRAY,
                required=False,
                description='An array of tags, which allow to add key, value meta-data to managed objects'
            )
        }
    
    def _define_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies for Organization objects."""
        # Organizations are foundational and typically don't depend on other objects
        return set()
    
    def export(self, output_dir: str) -> Dict[str, Any]:
        """
        Export organizations from Intersight to YAML files.
        
        Args:
            output_dir: Directory where YAML files should be saved
            
        Returns:
            Dictionary with export results
        """
        results = {
            'success_count': 0,
            'error_count': 0,
            'errors': [],
            'exported_files': []
        }
        
        try:
            logger.info("Starting organization export...")
            
            # Query all organizations from Intersight
            raw_objects = self.api_client.query_objects(self.object_type)
            logger.info(f"Retrieved {len(raw_objects)} raw organizations from Intersight")
            
            # Filter out system default organizations
            filtered_objects = self.filter_system_defaults(raw_objects)
            logger.info(f"Filtered to {len(filtered_objects)} user-defined organizations")
            
            # Only create directory when we have objects to export
            if not filtered_objects:
                logger.info("No user-defined organizations to export, skipping folder creation")
                return results
            
            # Process each organization
            for org_obj in filtered_objects:
                try:
                    # Extract user-defined values  
                    user_data = self._extract_user_defined_values(org_obj)
                    
                    # Convert MOID references to name references 
                    processed_data = self.convert_moid_references_to_names(user_data)
                    
                    # Generate filename with directory path
                    filename = self.generate_filename(processed_data)
                    org_dir = os.path.join(output_dir, self.folder_path)
                    file_path = os.path.join(org_dir, filename)
                    
                    # Save to YAML
                    self.save_to_yaml(processed_data, file_path)
                    
                    results['exported_files'].append(file_path)
                    results['success_count'] += 1
                    
                    logger.debug(f"Exported organization '{processed_data.get('Name')}' to {file_path}")
                    
                except Exception as e:
                    error_msg = f"Failed to export organization '{org_obj.get('Name', 'unknown')}': {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
            
            logger.info(f"Organization export completed: {results['success_count']} succeeded, {results['error_count']} failed")
            
        except Exception as e:
            error_msg = f"Failed to export organizations: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['error_count'] += 1
        
        return results
    
    def import_objects(self, yaml_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Import organizations from YAML data to Intersight.
        
        Args:
            yaml_data: List of organization dictionaries from YAML files
            
        Returns:
            Dictionary with import results
        """
        results = {
            'created_count': 0,
            'updated_count': 0,
            'deleted_count': 0,
            'error_count': 0,
            'errors': [],
            'warnings': [],
            'objects_to_delete': set()
        }
        
        try:
            logger.info(f"Starting organization import for {len(yaml_data)} objects...")
            
            # Get current organizations from Intersight
            current_objects = self.api_client.query_objects(self.object_type)
            current_objects = self.filter_system_defaults(current_objects)
            
            # Create lookup maps (API uses lowercase 'name', YAML uses uppercase 'Name')
            current_by_name = {obj.get('name'): obj for obj in current_objects if obj.get('name')}
            yaml_by_name = {obj['Name']: obj for obj in yaml_data if 'Name' in obj}
            
            # Identify operations needed
            to_create = set(yaml_by_name.keys()) - set(current_by_name.keys())
            to_update = set(yaml_by_name.keys()) & set(current_by_name.keys())
            to_delete = set(current_by_name.keys()) - set(yaml_by_name.keys())
            
            logger.info(f"Import plan: {len(to_create)} to create, {len(to_update)} to update, {len(to_delete)} to delete")
            
            # Handle creations
            for name in to_create:
                try:
                    yaml_obj = yaml_by_name[name]
                    
                    # Normalize ObjectType field if present (convert from export format to API format)
                    if 'ObjectType' in yaml_obj:
                        yaml_obj['ObjectType'] = self._expand_object_type_for_import(yaml_obj['ObjectType'])
                    
                    # Validate the object
                    validation_errors = self.validate_object(yaml_obj)
                    if validation_errors:
                        error_msg = f"Validation failed for organization '{name}': {validation_errors}"
                        logger.error(error_msg)
                        results['errors'].append(error_msg)
                        results['error_count'] += 1
                        continue
                    
                    # Process references (resolve names to MOIDs)
                    processed_obj = self._process_references_for_import(yaml_obj)
                    
                    # Create the organization
                    created_obj = self.api_client.create_object(self.object_type, processed_obj)
                    results['created_count'] += 1
                    
                    logger.info(f"Created organization: {name}")
                    
                except Exception as e:
                    error_msg = f"Failed to create organization '{name}': {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
            
            # Handle updates
            for name in to_update:
                try:
                    current_obj = current_by_name[name]
                    yaml_obj = yaml_by_name[name]
                    
                    # Normalize ObjectType field if present (convert from export format to API format)
                    if 'ObjectType' in yaml_obj:
                        yaml_obj['ObjectType'] = self._expand_object_type_for_import(yaml_obj['ObjectType'])
                    
                    # Check if update is needed
                    if self._objects_are_equivalent(current_obj, yaml_obj):
                        logger.debug(f"Organization '{name}' is already up to date")
                        continue
                    
                    # Validate the object
                    validation_errors = self.validate_object(yaml_obj)
                    if validation_errors:
                        error_msg = f"Validation failed for organization '{name}': {validation_errors}"
                        logger.error(error_msg)
                        results['errors'].append(error_msg)
                        results['error_count'] += 1
                        continue
                    
                    # Process references
                    processed_obj = self._process_references_for_import(yaml_obj)
                    
                    # Update the organization (API uses lowercase 'moid')
                    updated_obj = self.api_client.update_object(
                        self.object_type, current_obj['moid'], processed_obj
                    )
                    results['updated_count'] += 1
                    
                    logger.info(f"Updated organization: {name}")
                    
                except Exception as e:
                    error_msg = f"Failed to update organization '{name}': {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
            
            # Store objects to delete for later processing in reverse dependency order
            results['objects_to_delete'] = to_delete
            
            logger.info(f"Organization import completed: {results['created_count']} created, "
                       f"{results['updated_count']} updated, {len(to_delete)} marked for deletion")
            
        except Exception as e:
            error_msg = f"Failed to import organizations: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['error_count'] += 1
        
        return results
    
    def delete_objects(self, to_delete: set) -> Dict[str, Any]:
        """
        Delete organizations that are not present in YAML data.
        
        This method is called during the delete phase and will be processed
        in reverse dependency order by the main import orchestrator.
        
        Args:
            to_delete: Set of organization names to delete
            
        Returns:
            Dictionary with deletion results
        """
        results = {
            'deleted_count': 0,
            'error_count': 0,
            'errors': [],
            'warnings': []
        }
        
        if not to_delete:
            return results
        
        try:
            # Get current organizations for deletion operations
            current_objects = self.api_client.query_objects(self.object_type)
            current_objects = self.filter_system_defaults(current_objects)
            current_by_name = {obj.get('name'): obj for obj in current_objects if obj.get('name')}
            
            # Check safe mode
            safe_mode = os.getenv('SAFE_MODE', 'false').lower() == 'true'
            
            for name in to_delete:
                try:
                    if name not in current_by_name:
                        continue  # Organization was already deleted or doesn't exist
                        
                    current_obj = current_by_name[name]
                    
                    if safe_mode:
                        warning_msg = f"SAFE MODE: Would delete organization '{name}' (set SAFE_MODE=false to allow deletions)"
                        logger.warning(warning_msg)
                        results['warnings'].append(warning_msg)
                    else:
                        # Check if organization can be safely deleted (no dependent objects)
                        if self._can_delete_organization(current_obj):
                            self.api_client.delete_object(self.object_type, current_obj['moid'])
                            results['deleted_count'] += 1
                            logger.info(f"Deleted organization: {name}")
                        else:
                            warning_msg = f"Cannot delete organization '{name}': has dependent objects"
                            logger.warning(warning_msg)
                            results['warnings'].append(warning_msg)
                    
                except Exception as e:
                    error_msg = f"Failed to delete organization '{name}': {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
                    
        except Exception as e:
            error_msg = f"Failed to process organization deletions: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['error_count'] += 1
        
        return results
    
    def document(self) -> Dict[str, Any]:
        """
        Generate documentation for the Organization object type.
        
        Returns:
            Dictionary containing documentation information
        """
        try:
            # Get field definitions from OpenAPI schema
            user_fields = self.get_user_defined_fields()
            
            # Generate field documentation
            field_docs = {}
            for field_name, field_def in user_fields.items():
                field_docs[field_name] = {
                    'type': field_def.field_type.value,
                    'description': field_def.description or 'No description available',
                    'required': field_def.required,
                    'constraints': self._get_field_constraints_from_definition(field_def)
                }
            
            # Generate example YAML
            example = {
                'ObjectType': self._simplify_object_type_for_export(self.object_type),
                'Name': 'my-organization',
                'Description': 'Example organization for development environment',
                'ResourceGroups': ['default-resource-group', 'development-resources']
            }
            
            return {
                'object_type': self.object_type,
                'display_name': self.display_name,
                'description': 'Organizations provide multi-tenancy within an account. Resources are associated to organizations using resource groups.',
                'folder_path': self.folder_path,
                'fields': field_docs,
                'example': example,
                'dependencies': [dep.target_type for dep in self.get_dependencies()]
            }
            
        except Exception as e:
            logger.error(f"Failed to generate documentation for {self.object_type}: {e}")
            return {
                'object_type': self.object_type,
                'error': str(e)
            }
    
    def _process_references_for_export(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MOID references to name references for export.
        
        Organizations can reference ResourceGroups, which should be simplified to names.
        
        Args:
            obj: Object dictionary with MOID references
            
        Returns:
            Object dictionary with name references
        """
        processed_obj = obj.copy()
        
        # Handle ResourceGroups - convert from full objects to simple name array
        if 'ResourceGroups' in processed_obj and processed_obj['ResourceGroups']:
            resource_group_names = []
            for resource_group in processed_obj['ResourceGroups']:
                if isinstance(resource_group, dict):
                    # Handle MOID reference objects (mo.MoRef format)
                    if 'moid' in resource_group and 'object_type' in resource_group:
                        # Query Intersight to resolve MOID to name
                        try:
                            moid = resource_group['moid']
                            resource_groups = self.api_client.query_objects('resource.Group')
                            matching_group = next(
                                (rg for rg in resource_groups if rg.get('Moid') == moid),
                                None
                            )
                            if matching_group and matching_group.get('Name'):
                                resource_group_names.append(matching_group['Name'])
                            else:
                                logger.warning(f"Could not resolve ResourceGroup MOID {moid} to name")
                        except Exception as e:
                            logger.warning(f"Failed to resolve ResourceGroup MOID {resource_group.get('moid')}: {e}")
                    # Handle direct name reference
                    elif 'Name' in resource_group:
                        resource_group_names.append(resource_group['Name'])
                elif isinstance(resource_group, str):
                    # Already a string (name)
                    resource_group_names.append(resource_group)
            processed_obj['ResourceGroups'] = resource_group_names
        
        return processed_obj
    
    def _process_references_for_import(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert name references to MOID references for import.
        
        Args:
            obj: Object dictionary with name references
            
        Returns:
            Object dictionary with MOID references
        """
        processed_obj = obj.copy()
        
        # Handle ResourceGroups - convert from name array to MOID references
        if 'ResourceGroups' in processed_obj and processed_obj['ResourceGroups']:
            resource_group_refs = []
            
            for resource_group_name in processed_obj['ResourceGroups']:
                if isinstance(resource_group_name, str):
                    # Query Intersight to find the resource group by name
                    try:
                        resource_groups = self.api_client.query_objects('resource.Group')
                        matching_group = next(
                            (rg for rg in resource_groups if rg.get('Name') == resource_group_name),
                            None
                        )
                        
                        if matching_group:
                            # Create proper reference object
                            resource_group_refs.append({
                                'Moid': matching_group['Moid'],
                                'ObjectType': 'resource.Group'
                            })
                        else:
                            logger.warning(f"ResourceGroup '{resource_group_name}' not found, skipping")
                    except Exception as e:
                        logger.warning(f"Failed to resolve ResourceGroup '{resource_group_name}': {e}")
                elif isinstance(resource_group_name, dict):
                    # Already a reference object
                    resource_group_refs.append(resource_group_name)
            
            processed_obj['ResourceGroups'] = resource_group_refs
        
        return processed_obj
    
    def convert_moid_references_to_names(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Override base class method to handle organization-specific reference processing.
        
        Args:
            obj: Object with MOID references
            
        Returns:
            Object with name-based references
        """
        # First apply base class processing for standard reference fields
        converted = super().convert_moid_references_to_names(obj)
        
        # Then apply organization-specific processing for ResourceGroups
        return self._process_references_for_export(converted)
    
    def _objects_are_equivalent(self, current_obj: Dict[str, Any], yaml_obj: Dict[str, Any]) -> bool:
        """
        Check if two organization objects are equivalent.
        
        Args:
            current_obj: Current object from Intersight
            yaml_obj: Object from YAML file
            
        Returns:
            True if objects are equivalent
        """
        # Compare user-defined fields
        user_fields = self.get_user_defined_fields()
        
        for field_name, field_def in user_fields.items():
            current_value = current_obj.get(field_name)
            yaml_value = yaml_obj.get(field_name)
            
            # Handle None values
            if current_value is None and yaml_value is None:
                continue
            if current_value is None or yaml_value is None:
                return False
            
            # Compare values
            if current_value != yaml_value:
                return False
        
        return True
    
    def _can_delete_organization(self, org_obj: Dict[str, Any]) -> bool:
        """
        Check if an organization can be safely deleted.
        
        Args:
            org_obj: Organization object dictionary
            
        Returns:
            True if organization can be deleted
        """
        # For now, just check if it's not the default organization
        # In a real implementation, you'd check for dependent objects
        return org_obj.get('Name') != 'default'
    
    def _get_field_constraints_from_definition(self, field_def: FieldDefinition) -> Dict[str, Any]:
        """
        Extract field constraints from FieldDefinition object.
        
        Args:
            field_def: FieldDefinition object
            
        Returns:
            Dictionary of constraints
        """
        constraints = {}
        
        if field_def.pattern:
            constraints['pattern'] = field_def.pattern
        if field_def.min_length is not None:
            constraints['min_length'] = field_def.min_length
        if field_def.max_length is not None:
            constraints['max_length'] = field_def.max_length
        if field_def.enum_values:
            constraints['allowed_values'] = field_def.enum_values
        if field_def.minimum is not None:
            constraints['minimum'] = field_def.minimum
        if field_def.maximum is not None:
            constraints['maximum'] = field_def.maximum
        
        return constraints
    
    def _extract_user_defined_values(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract user-defined values from organization, including filtered user tags.
        
        Override base method to add Tags field filtering to exclude system tags.
        
        Args:
            obj: The raw object dictionary from Intersight API
            
        Returns:
            Dictionary containing user-defined values with filtered tags
        """
        # Get the standard user-defined values first
        extracted = super()._extract_user_defined_values(obj)
        
        # Filter Tags to exclude system tags
        if 'Tags' in extracted and extracted['Tags']:
            user_tags = []
            for tag in extracted['Tags']:
                if isinstance(tag, dict):
                    # Exclude system tags like cisco.meta.SystemDefault
                    tag_key = tag.get('Key', '')
                    if not tag_key.startswith('cisco.meta.') and not tag_key.startswith('system.'):
                        user_tags.append(tag)
            
            # Only include Tags field if there are user-defined tags
            if user_tags:
                extracted['Tags'] = user_tags
            else:
                # Remove empty Tags field to keep YAML clean
                extracted.pop('Tags', None)
        
        return extracted