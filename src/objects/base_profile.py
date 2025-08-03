"""
Base Profile class for all Intersight profile objects.

This module provides the base Profile class that all specific profile 
implementations inherit from. It handles common profile attributes and
provides a foundation for profile-specific implementations.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Set
from abc import abstractmethod

from src.core.object_type import ObjectType, FieldDefinition, FieldType, DependencyDefinition, ValidationLevel

logger = logging.getLogger(__name__)


class BaseProfile(ObjectType):
    """
    Base class for all Intersight profile objects.
    
    This class provides common functionality for all profile types including:
    - Organization field handling
    - Common profile attributes (Name, Description, Tags)
    - Policy relationship management
    - Profile-specific validation and transformation
    """
    
    def __init__(self, api_client=None, openapi_schema=None, validation_level=ValidationLevel.STRICT):
        """Initialize the base profile object."""
        super().__init__(api_client, openapi_schema, validation_level)
        
        # Set up import transformation for Organization field
        self.add_import_transform('Organization', self._transform_organization_for_import)
    
    @property
    def folder_path(self) -> str:
        """Return the base folder path for profiles."""
        return "profiles"
    
    def _get_common_profile_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get common fields that all profiles share.
        
        Returns:
            Dictionary of common profile field definitions
        """
        return {
            'Name': FieldDefinition(
                name='Name',
                field_type=FieldType.STRING,
                required=True,
                description='Name of the profile',
                min_length=1,
                max_length=64,
                pattern=r'^[a-zA-Z0-9_.:-]{1,64}$'
            ),
            'Description': FieldDefinition(
                name='Description',
                field_type=FieldType.STRING,
                required=False,
                description='Description of the profile'
            ),
            'Organization': FieldDefinition(
                name='Organization',
                field_type=FieldType.REFERENCE,
                required=True,
                description='A reference to a organizationOrganization resource',
                reference_type='organization.Organization',
                reference_field='Name'
            ),
            'ObjectType': FieldDefinition(
                name='ObjectType',
                field_type=FieldType.STRING,
                required=True,
                description='The concrete type of this complex type'
            ),
            'Tags': FieldDefinition(
                name='Tags',
                field_type=FieldType.ARRAY,
                required=False,
                description='An array of tags, which allow to add key, value meta-data to managed objects'
            )
        }
    
    def _define_dependencies(self) -> Set[DependencyDefinition]:
        """Define common dependencies for profiles."""
        return {
            DependencyDefinition(
                target_type='organization.Organization',
                dependency_type='references',
                required=True,
                description='Profiles must belong to an organization'
            )
        }
    
    def get_organization_name(self, obj: Dict[str, Any]) -> Optional[str]:
        """
        Extract organization name from a profile object.
        Organization can be either a string or an object.
        
        Args:
            obj: Profile object dictionary
            
        Returns:
            Organization name or None if not found
        """
        org_ref = obj.get('Organization')
        
        # Handle organization as simple string (new format)
        if isinstance(org_ref, str):
            return org_ref
        
        # Handle organization as object (legacy format)
        if isinstance(org_ref, dict):
            return org_ref.get('Name') or org_ref.get('Moid')
        
        return None
    
    def _transform_organization_for_import(self, value):
        """
        Transform organization reference for import.
        
        Converts string organization name to proper reference object.
        
        Args:
            value: Organization reference (string name or dict object)
            
        Returns:
            Proper organization reference object
        """
        if isinstance(value, str):
            # Convert string name to reference object
            if self.api_client and hasattr(self.api_client, 'organization_resolver'):
                moid = self.api_client.organization_resolver.resolve_name_to_moid(value)
                if moid:
                    return {
                        'Moid': moid,
                        'ObjectType': 'organization.Organization'
                    }
                else:
                    logger.warning(f"Could not resolve organization name '{value}' to MOID")
                    return {
                        'Name': value,
                        'ObjectType': 'organization.Organization'
                    }
            else:
                # Fallback: create name-based reference
                return {
                    'Name': value,
                    'ObjectType': 'organization.Organization'
                }
        elif isinstance(value, dict):
            # Already a reference object, return as-is
            return value
        else:
            logger.warning(f"Unknown organization reference format: {value}")
            return value
    
    def generate_filename(self, obj: Dict[str, Any], organization_name: str = None) -> str:
        """
        Generate a filename for a profile object.
        
        Profiles are named with organization prefix: {org_name}_{profile_name}.yaml
        
        Args:
            obj: The profile object dictionary
            organization_name: Organization name (extracted if not provided)
            
        Returns:
            Generated filename string
        """
        name = obj.get('Name', 'unnamed')
        # Sanitize filename
        name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        name = name.replace(' ', '_')
        
        # Get or extract organization name
        if not organization_name:
            organization_name = self.get_organization_name(obj) or 'default'
        
        # Sanitize organization name
        org_name = "".join(c for c in organization_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        org_name = org_name.replace(' ', '_')
        
        return f"{org_name}_{name}.yaml"
    
    def export(self, output_dir: str) -> Dict[str, Any]:
        """
        Export profiles from Intersight to YAML files.
        
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
            logger.info(f"Starting {self.display_name} export...")
            
            # Query all profiles from Intersight
            raw_objects = self.api_client.query_objects(self.object_type)
            logger.info(f"Retrieved {len(raw_objects)} raw {self.display_name} profiles from Intersight")
            
            # Filter out system default profiles
            filtered_objects = self.filter_system_defaults(raw_objects)
            logger.info(f"Filtered to {len(filtered_objects)} user-defined {self.display_name} profiles")
            
            # Only create directory when we have objects to export
            if not filtered_objects:
                logger.info(f"No user-defined {self.display_name} profiles to export, skipping folder creation")
                return results
            
            # Process each profile
            for profile_obj in filtered_objects:
                try:
                    # Extract user-defined values
                    user_data = self._extract_user_defined_values(profile_obj)
                    
                    # Convert MOID references to name references (including organization string conversion)
                    processed_data = self._process_references_for_export(user_data)
                    
                    # Generate filename with organization prefix
                    org_name = self.get_organization_name(processed_data)
                    filename = self.generate_filename(processed_data, org_name)
                    profile_dir = os.path.join(output_dir, self.folder_path)
                    file_path = os.path.join(profile_dir, filename)
                    
                    # Save to YAML
                    self.save_to_yaml(processed_data, file_path)
                    
                    results['exported_files'].append(file_path)
                    results['success_count'] += 1
                    
                    logger.debug(f"Exported {self.display_name} profile '{processed_data.get('Name')}' to {file_path}")
                    
                except Exception as e:
                    error_msg = f"Failed to export {self.display_name} profile '{profile_obj.get('Name', 'unknown')}': {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
            
            logger.info(f"{self.display_name} export completed: {results['success_count']} succeeded, {results['error_count']} failed")
            
        except Exception as e:
            error_msg = f"Failed to export {self.display_name} profiles: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['error_count'] += 1
        
        return results
    
    def import_objects(self, yaml_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Import profiles from YAML data to Intersight.
        
        This method orchestrates the full import process but delegates to separate
        methods for create, update, and delete operations.
        
        Args:
            yaml_data: List of profile dictionaries from YAML files
            
        Returns:
            Dictionary with import results
        """
        results = {
            'created_count': 0,
            'updated_count': 0,
            'deleted_count': 0,
            'error_count': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            logger.info(f"Starting {self.display_name} import for {len(yaml_data)} objects...")
            
            # Get current profiles from Intersight
            current_objects = self.api_client.query_objects(self.object_type)
            current_objects = self.filter_system_defaults(current_objects)
            
            # Create lookup maps (API might use lowercase 'name' like organizations and policies)
            current_by_name = {obj.get('name', obj.get('Name')): obj for obj in current_objects if obj.get('name') or obj.get('Name')}
            yaml_by_name = {obj['Name']: obj for obj in yaml_data if 'Name' in obj}
            
            # Debug logging to see what we're comparing
            logger.debug(f"Current {self.display_name} profiles from API: {list(current_by_name.keys())}")
            logger.debug(f"YAML {self.display_name} profiles: {list(yaml_by_name.keys())}")
            
            # Identify operations needed
            to_create = set(yaml_by_name.keys()) - set(current_by_name.keys())
            to_update = set(yaml_by_name.keys()) & set(current_by_name.keys())
            to_delete = set(current_by_name.keys()) - set(yaml_by_name.keys())
            
            logger.info(f"Import plan: {len(to_create)} to create, {len(to_update)} to update, {len(to_delete)} to delete")
            
            # Store the lookup maps for use by individual operation methods
            self._current_by_name = current_by_name
            self._yaml_by_name = yaml_by_name
            
            # Perform operations in correct order: Creates > Updates > Deletes
            # (Deletes will be handled separately in reverse dependency order)
            
            # Handle creations
            create_results = self.create_objects(to_create)
            results['created_count'] += create_results['created_count']
            results['error_count'] += create_results['error_count']
            results['errors'].extend(create_results['errors'])
            results['warnings'].extend(create_results['warnings'])
            
            # Handle updates
            update_results = self.update_objects(to_update)
            results['updated_count'] += update_results['updated_count']
            results['error_count'] += update_results['error_count']
            results['errors'].extend(update_results['errors'])
            results['warnings'].extend(update_results['warnings'])
            
            # Store objects to delete for later processing in reverse dependency order
            results['objects_to_delete'] = to_delete
            
            logger.info(f"{self.display_name} import completed: {results['created_count']} created, "
                       f"{results['updated_count']} updated, {len(to_delete)} marked for deletion")
            
        except Exception as e:
            error_msg = f"Failed to import {self.display_name} profiles: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            results['error_count'] += 1
        
        return results
    
    def create_objects(self, to_create: set) -> Dict[str, Any]:
        """
        Create new objects from YAML data.
        
        Args:
            to_create: Set of object names to create
            
        Returns:
            Dictionary with creation results
        """
        results = {
            'created_count': 0,
            'error_count': 0,
            'errors': [],
            'warnings': []
        }
        
        for name in to_create:
            try:
                yaml_obj = self._yaml_by_name[name]
                
                # Apply import transformations before validation
                transformed_obj = self.transform_for_import(yaml_obj)
                
                # Validate the transformed object
                validation_errors = self.validate_object(transformed_obj)
                
                # Add organization-specific validation
                org_validation_errors = self.validate_organization_reference(transformed_obj)
                validation_errors.extend(org_validation_errors)
                
                if validation_errors:
                    error_msg = f"Validation failed for {self.display_name} profile '{name}': {validation_errors}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
                    continue
                
                # Process references (resolve names to MOIDs)
                processed_obj = self._process_references_for_import(transformed_obj)
                
                # Create the profile
                created_obj = self.api_client.create_object(self.object_type, processed_obj)
                results['created_count'] += 1
                
                logger.info(f"Created {self.display_name} profile: {name}")
                
            except Exception as e:
                error_msg = f"Failed to create {self.display_name} profile '{name}': {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
                results['error_count'] += 1
        
        return results
    
    def update_objects(self, to_update: set) -> Dict[str, Any]:
        """
        Update existing objects from YAML data.
        
        Args:
            to_update: Set of object names to update
            
        Returns:
            Dictionary with update results
        """
        results = {
            'updated_count': 0,
            'error_count': 0,
            'errors': [],
            'warnings': []
        }
        
        for name in to_update:
            try:
                current_obj = self._current_by_name[name]
                yaml_obj = self._yaml_by_name[name]
                
                # Check if update is needed
                if self._objects_are_equivalent(current_obj, yaml_obj):
                    logger.debug(f"{self.display_name} profile '{name}' is already up to date")
                    continue
                
                # Apply import transformations before validation
                transformed_obj = self.transform_for_import(yaml_obj)
                
                # Validate the object
                validation_errors = self.validate_object(transformed_obj)
                
                # Add organization-specific validation
                org_validation_errors = self.validate_organization_reference(transformed_obj)
                validation_errors.extend(org_validation_errors)
                
                if validation_errors:
                    error_msg = f"Validation failed for {self.display_name} profile '{name}': {validation_errors}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
                    results['error_count'] += 1
                    continue
                
                # Process references
                processed_obj = self._process_references_for_import(transformed_obj)
                
                # Update the profile
                updated_obj = self.api_client.update_object(
                    self.object_type, current_obj['moid'], processed_obj
                )
                results['updated_count'] += 1
                
                logger.info(f"Updated {self.display_name} profile: {name}")
                
            except Exception as e:
                error_msg = f"Failed to update {self.display_name} profile '{name}': {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
                results['error_count'] += 1
        
        return results
    
    def delete_objects(self, to_delete: set) -> Dict[str, Any]:
        """
        Delete objects that are not present in YAML data.
        
        This method is called during the delete phase and will be processed
        in reverse dependency order by the main import orchestrator.
        
        Args:
            to_delete: Set of object names to delete
            
        Returns:
            Dictionary with deletion results
        """
        results = {
            'deleted_count': 0,
            'error_count': 0,
            'errors': [],
            'warnings': []
        }
        
        # Check safe mode
        safe_mode = os.getenv('SAFE_MODE', 'false').lower() == 'true'
        
        for name in to_delete:
            try:
                current_obj = self._current_by_name[name]
                
                if safe_mode:
                    warning_msg = f"SAFE MODE: Would delete {self.display_name} profile '{name}' (set SAFE_MODE=false to allow deletions)"
                    logger.warning(warning_msg)
                    results['warnings'].append(warning_msg)
                else:
                    # Check if profile can be safely deleted
                    if self._can_delete_profile(current_obj):
                        self.api_client.delete_object(self.object_type, current_obj['moid'])
                        results['deleted_count'] += 1
                        logger.info(f"Deleted {self.display_name} profile: {name}")
                    else:
                        warning_msg = f"Cannot delete {self.display_name} profile '{name}': profile is in use"
                        logger.warning(warning_msg)
                        results['warnings'].append(warning_msg)
                
            except Exception as e:
                error_msg = f"Failed to delete {self.display_name} profile '{name}': {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
                results['error_count'] += 1
        
        return results
    
    def document(self) -> Dict[str, Any]:
        """
        Generate documentation for the profile object type.
        
        Returns:
            Dictionary containing documentation information
        """
        try:
            # Get field definitions
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
                'Name': f'example-{self.display_name.lower().replace(" ", "-")}',
                'Description': f'Example {self.display_name} profile for development environment',
                'Organization': 'default'
            }
            
            # Add profile-specific example fields
            example.update(self._get_example_profile_fields())
            
            return {
                'object_type': self.object_type,
                'display_name': self.display_name,
                'description': f'{self.display_name} profiles for Cisco Intersight infrastructure management',
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
        Organization references are simplified to just the organization name string.
        
        Args:
            obj: Object dictionary with MOID references
            
        Returns:
            Object dictionary with simplified organization reference
        """
        processed = obj.copy()
        
        # Handle Organization reference - convert to simple string format
        if 'Organization' in processed:
            org_ref = processed['Organization']
            
            # Use the reference resolver utility for consistent conversion
            if self.api_client and hasattr(self.api_client, 'reference_resolver'):
                org_name = self.api_client.reference_resolver.convert_moid_reference_to_name(org_ref, 'default')
                processed['Organization'] = org_name
                logger.debug(f"Converted organization reference to string: '{org_name}'")
            else:
                # Fallback if no reference resolver available
                if isinstance(org_ref, dict):
                    # Try to get name directly
                    org_name = org_ref.get('Name') or org_ref.get('name')
                    if org_name:
                        processed['Organization'] = org_name
                    else:
                        processed['Organization'] = 'default'
                        logger.warning(f"No reference resolver available and could not extract name from reference, using 'default'")
                elif isinstance(org_ref, str):
                    # Already a string, keep as-is
                    processed['Organization'] = org_ref
                else:
                    processed['Organization'] = 'default'
                    logger.warning(f"Invalid organization reference type: {type(org_ref)}, using 'default'")
        
        return processed
    
    def _process_references_for_import(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert name references to MOID references for import.
        Organization references can be either strings or objects.
        
        Args:
            obj: Object dictionary with name references
            
        Returns:
            Object dictionary with MOID references
        """
        processed = obj.copy()
        
        # Handle Organization reference
        if 'Organization' in processed:
            org_ref = processed['Organization']
            org_name = None
            
            # Handle organization as simple string
            if isinstance(org_ref, str):
                org_name = org_ref
                logger.debug(f"Found organization as string: '{org_name}'")
            # Handle organization as object (legacy format)
            elif isinstance(org_ref, dict) and 'Name' in org_ref:
                org_name = org_ref['Name']
                logger.debug(f"Found organization as object with name: '{org_name}'")
            
            # Convert to MOID reference if we have a name
            if org_name and self.api_client:
                try:
                    # Use organization resolver for better performance
                    org_moid = None
                    if hasattr(self.api_client, 'organization_resolver'):
                        org_moid = self.api_client.organization_resolver.resolve_name_to_moid(org_name)
                    
                    # Fallback to direct API resolution
                    if not org_moid:
                        org_moid = self.api_client.resolve_name_to_moid('organization.Organization', org_name)
                    
                    if org_moid:
                        processed['Organization'] = {
                            'Moid': org_moid,
                            'ObjectType': 'organization.Organization'
                        }
                        logger.debug(f"Resolved organization '{org_name}' to MOID: {org_moid}")
                    else:
                        raise ValueError(f"Organization '{org_name}' not found")
                except Exception as e:
                    logger.error(f"Failed to resolve organization name '{org_name}' to MOID: {e}")
                    raise
        
        return processed
    
    def validate_organization_reference(self, obj: Dict[str, Any]) -> List[str]:
        """
        Validate organization references in a profile object.
        
        Args:
            obj: Profile object to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        org_ref = obj.get('Organization')
        if not org_ref:
            errors.append("Organization field is missing or null")
            return errors
        
        # Handle string organization reference (new format)
        if isinstance(org_ref, str):
            if not org_ref.strip():
                errors.append("Organization name cannot be empty")
            elif self.api_client and hasattr(self.api_client, 'organization_resolver'):
                # Validate that organization name can be resolved
                if not self.api_client.organization_resolver.validate_organization_reference(org_ref):
                    errors.append(f"Organization '{org_ref}' cannot be resolved to a valid MOID")
        
        # Handle object organization reference (legacy format)
        elif isinstance(org_ref, dict):
            if 'Name' in org_ref:
                org_name = org_ref['Name']
                if not org_name or not org_name.strip():
                    errors.append("Organization name in object reference cannot be empty")
                elif self.api_client and hasattr(self.api_client, 'organization_resolver'):
                    if not self.api_client.organization_resolver.validate_organization_reference(org_name):
                        errors.append(f"Organization '{org_name}' cannot be resolved to a valid MOID")
            elif 'Moid' in org_ref:
                org_moid = org_ref['Moid']
                if not org_moid or not org_moid.strip():
                    errors.append("Organization MOID in object reference cannot be empty")
            else:
                errors.append("Organization object reference must contain either 'Name' or 'Moid' field")
        
        else:
            errors.append(f"Organization reference must be a string or object, got {type(org_ref).__name__}")
        
        return errors
    
    def _objects_are_equivalent(self, current_obj: Dict[str, Any], yaml_obj: Dict[str, Any]) -> bool:
        """
        Check if two profile objects are equivalent.
        
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
            
            # Handle Organization reference comparison
            if field_name == 'Organization':
                if not self._compare_organization_references(current_value, yaml_value):
                    return False
            else:
                # Compare other values
                if current_value != yaml_value:
                    return False
        
        return True
    
    def _compare_organization_references(self, current_ref: Any, yaml_ref: Any) -> bool:
        """
        Compare organization references (handling MOID vs Name vs String).
        
        Args:
            current_ref: Organization reference from current Intersight object
            yaml_ref: Organization reference from YAML file (can be string or object)
            
        Returns:
            True if references point to the same organization
        """
        # Handle cases where yaml_ref is a simple string
        if isinstance(yaml_ref, str):
            # If current_ref is an object, extract the name
            if isinstance(current_ref, dict):
                current_name = current_ref.get('Name')
                return current_name == yaml_ref
            # If current_ref is also a string, direct comparison
            return current_ref == yaml_ref
        
        # Handle cases where both are objects (legacy format)
        if isinstance(current_ref, dict) and isinstance(yaml_ref, dict):
            # Extract organization identifier from both references
            current_id = current_ref.get('Name') or current_ref.get('Moid')
            yaml_id = yaml_ref.get('Name') or yaml_ref.get('Moid')
            return current_id == yaml_id
        
        # Fallback to direct comparison
        return current_ref == yaml_ref
    
    def _can_delete_profile(self, profile_obj: Dict[str, Any]) -> bool:
        """
        Check if a profile can be safely deleted.
        
        Args:
            profile_obj: Profile object dictionary
            
        Returns:
            True if profile can be deleted
        """
        # Check if profile is deployed or has associated physical entities
        # This is a basic implementation - specific profile types may have additional checks
        
        # Check deployment status
        deploy_state = profile_obj.get('DeployState', '')
        if deploy_state in ['Deployed', 'Deploying']:
            logger.debug(f"Profile '{profile_obj.get('Name')}' is deployed or deploying")
            return False
        
        return True
    
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
        Extract user-defined values from profile, including filtered user tags.
        
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
    
    @abstractmethod
    def _get_example_profile_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this profile type.
        
        Returns:
            Dictionary of example field values
        """
        pass
