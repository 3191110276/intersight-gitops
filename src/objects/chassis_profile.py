"""
Chassis Profile object implementation.

This module implements the ChassisProfile class for handling Cisco Intersight
chassis profile in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set, Optional

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_profile import BaseProfile
from src.utils.openapi_parser import OpenAPIParser

logger = logging.getLogger(__name__)


class ChassisProfile(BaseProfile):
    """
    Implementation for Intersight Chassis Profile objects.
    
    Chassis Profile defines configurations and policies for chassis profile.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "chassis.Profile"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Chassis Profile"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing Chassis Profile YAML files."""
        return "profiles/chassis"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Chassis Profile objects based on OpenAPI schema."""
        # Start with common profile fields
        fields = self._get_common_profile_fields()
        
        # Add chassis-specific fields from OpenAPI schema
        if self.openapi_schema:
            try:
                from src.utils.openapi_parser import OpenAPIParser
                # If openapi_schema is a string, treat it as a file path
                if isinstance(self.openapi_schema, str):
                    openapi_parser = OpenAPIParser(self.openapi_schema)
                elif hasattr(self.openapi_schema, 'get_user_defined_fields'):
                    # It's already a parser instance
                    openapi_parser = self.openapi_schema
                else:
                    # It's a raw schema dict, skip OpenAPI processing and use fallback
                    logger.warning("Received raw schema dict instead of OpenAPIParser instance, using fallback fields")
                    fields.update(self._get_fallback_chassis_fields())
                    fields.update(self._get_policy_reference_fields())
                    return fields
                
                user_defined_fields = openapi_parser.get_user_defined_fields(self.object_type)
                
                # Convert OpenAPI field definitions to FieldDefinition objects
                for field_name, field_def in user_defined_fields.items():
                    # Skip fields already defined in base profile
                    if field_name in fields:
                        continue
                    
                    # Skip PolicyBucket - we'll replace it with individual policy fields
                    if field_name == 'PolicyBucket':
                        continue
                    
                    # Extract field information from OpenAPI schema
                    field_type = self._convert_openapi_type_to_field_type(field_def.get('type', 'string'))
                    required = field_name in openapi_parser.get_required_fields(self.object_type)
                    description = field_def.get('description', '')
                    
                    # Create FieldDefinition
                    field_definition = FieldDefinition(
                        name=field_name,
                        field_type=field_type,
                        required=required,
                        description=description
                    )
                    
                    # Add validation constraints
                    self._add_openapi_constraints(field_definition, field_def)
                    
                    fields[field_name] = field_definition
                    
                logger.debug(f"Loaded {len(user_defined_fields)} chassis-specific fields from OpenAPI schema")
                
            except Exception as e:
                logger.warning(f"Failed to load fields from OpenAPI schema: {e}")
                # Fallback to manual field definitions for critical fields
                fields.update(self._get_fallback_chassis_fields())
        else:
            # No OpenAPI schema available, use fallback definitions
            logger.warning("No OpenAPI schema available, using fallback field definitions")
            fields.update(self._get_fallback_chassis_fields())
        
        # Add individual policy reference fields to replace PolicyBucket
        fields.update(self._get_policy_reference_fields())
        
        return fields
    
    def _convert_openapi_type_to_field_type(self, openapi_type: str) -> FieldType:
        """Convert OpenAPI type to FieldType enum."""
        type_mapping = {
            'string': FieldType.STRING,
            'integer': FieldType.INTEGER,
            'number': FieldType.NUMBER,
            'boolean': FieldType.BOOLEAN,
            'array': FieldType.ARRAY,
            'object': FieldType.OBJECT
        }
        return type_mapping.get(openapi_type, FieldType.STRING)
    
    def _add_openapi_constraints(self, field_def: FieldDefinition, openapi_field: Dict[str, Any]):
        """Add validation constraints from OpenAPI field definition."""
        # String constraints
        if 'pattern' in openapi_field:
            field_def.pattern = openapi_field['pattern']
        if 'minLength' in openapi_field:
            field_def.min_length = openapi_field['minLength']
        if 'maxLength' in openapi_field:
            field_def.max_length = openapi_field['maxLength']
        
        # Numeric constraints
        if 'minimum' in openapi_field:
            field_def.minimum = openapi_field['minimum']
        if 'maximum' in openapi_field:
            field_def.maximum = openapi_field['maximum']
        
        # Enum constraints
        if 'enum' in openapi_field:
            field_def.enum_values = openapi_field['enum']
        
        # Default value
        if 'default' in openapi_field:
            field_def.default_value = openapi_field['default']
    
    def _get_fallback_chassis_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get fallback field definitions for chassis profiles when OpenAPI is not available.
        
        Returns:
            Dictionary of chassis-specific field definitions
        """
        return {
            'Description': FieldDefinition(
                name='Description',
                field_type=FieldType.STRING,
                required=False,
                description='Description of the chassis profile',
                max_length=1024
            ),
            'UserLabel': FieldDefinition(
                name='UserLabel',
                field_type=FieldType.STRING,
                required=False,
                description='User label assigned to the chassis profile',
                pattern=r'^[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]*$',
                min_length=0,
                max_length=64
            ),
            'AssignedChassis': FieldDefinition(
                name='AssignedChassis',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Reference to the equipment chassis assigned to this profile',
                reference_type='equipment.Chassis',
                reference_field='Name'
            )
        }
    
    def _get_policy_reference_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get policy reference fields that replace PolicyBucket.
        
        Returns:
            Dictionary of policy reference field definitions
        """
        return {
            'ImcAccessPolicy': FieldDefinition(
                name='ImcAccessPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an IMC Access Policy for chassis management access',
                reference_type='access.Policy',
                reference_field='Name'
            ),
            'PowerPolicy': FieldDefinition(
                name='PowerPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Power Policy for chassis power management',
                reference_type='power.Policy',
                reference_field='Name'
            ),
            'SnmpPolicy': FieldDefinition(
                name='SnmpPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an SNMP Policy for chassis monitoring',
                reference_type='snmp.Policy',
                reference_field='Name'
            ),
            'ThermalPolicy': FieldDefinition(
                name='ThermalPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Thermal Policy for chassis cooling management',
                reference_type='thermal.Policy',
                reference_field='Name'
            )
        }
    
    def _get_example_profile_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this profile type.
        
        Returns:
            Dictionary of example field values
        """
        return {
            'Description': 'Production chassis profile for data center operations',
            'UserLabel': 'Production-Chassis-01',
            'AssignedChassis': 'chassis-rack-1-1',
            'ImcAccessPolicy': 'imc-access-production',
            'PowerPolicy': 'high-performance-power',
            'SnmpPolicy': 'datacenter-snmp',
            'ThermalPolicy': 'quiet-thermal'
        }
    
    def _process_references_for_export(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MOID references to name references for export.
        Override base method to handle PolicyBucket conversion.
        
        Args:
            obj: Object dictionary with MOID references
            
        Returns:
            Object dictionary with name references and individual policy fields
        """
        # First apply base class processing (handles Organization conversion)
        processed = super()._process_references_for_export(obj)
        
        # Convert PolicyBucket to individual policy fields
        processed = self._convert_policy_bucket_for_export(processed)
        
        return processed
    
    def _convert_policy_bucket_for_export(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert PolicyBucket array to individual policy name fields.
        
        Args:
            obj: Object dictionary with PolicyBucket
            
        Returns:
            Object dictionary with individual policy fields
        """
        processed = obj.copy()
        
        # Remove PolicyBucket from the processed object
        policy_bucket = processed.pop('PolicyBucket', [])
        
        # Initialize policy fields
        processed['ImcAccessPolicy'] = None
        processed['PowerPolicy'] = None
        processed['SnmpPolicy'] = None
        processed['ThermalPolicy'] = None
        
        # Process each policy in the bucket
        if policy_bucket and isinstance(policy_bucket, list):
            for policy_ref in policy_bucket:
                if not isinstance(policy_ref, dict):
                    continue
                
                # Handle both PascalCase and snake_case object types
                object_type = policy_ref.get('ObjectType') or policy_ref.get('object_type', '')
                policy_name = self._resolve_policy_name(policy_ref)
                
                logger.debug(f"Processing policy: object_type='{object_type}', name='{policy_name}', ref={policy_ref}")
                
                if not policy_name:
                    logger.warning(f"Could not resolve policy name for {object_type}: {policy_ref}")
                    continue
                
                # Map policy types to field names
                if object_type == 'access.Policy':
                    processed['ImcAccessPolicy'] = policy_name
                elif object_type == 'power.Policy':
                    processed['PowerPolicy'] = policy_name
                elif object_type == 'snmp.Policy':
                    processed['SnmpPolicy'] = policy_name
                elif object_type == 'thermal.Policy':
                    processed['ThermalPolicy'] = policy_name
                else:
                    logger.warning(f"Unknown policy type in PolicyBucket: '{object_type}' (policy_ref: {policy_ref})")
        
        return processed
    
    def _resolve_policy_name(self, policy_ref: Dict[str, Any]) -> Optional[str]:
        """
        Resolve a policy reference to its name.
        
        Args:
            policy_ref: Policy reference object
            
        Returns:
            Policy name or None if not resolvable
        """
        # Try to get name directly from the reference (handle both cases)
        name = policy_ref.get('Name') or policy_ref.get('name')
        if name:
            return name
        
        # If no name but has MOID, resolve via API
        moid = policy_ref.get('Moid') or policy_ref.get('moid')
        object_type = policy_ref.get('ObjectType') or policy_ref.get('object_type')
        
        if moid and object_type and self.api_client:
            try:
                # Use reference resolver if available
                if hasattr(self.api_client, 'resolve_moid_to_name'):
                    resolved_name = self.api_client.resolve_moid_to_name(object_type, moid)
                    if resolved_name:
                        return resolved_name
                
                # Fallback to direct API query
                policy_obj = self.api_client.get_object_by_moid(object_type, moid)
                if policy_obj:
                    resolved_name = policy_obj.get('Name') or policy_obj.get('name')
                    if resolved_name:
                        return resolved_name
                
                # Final fallback: query all policies of this type and find by MOID
                try:
                    policies = self.api_client.query_objects(object_type)
                    for policy in policies:
                        policy_moid = policy.get('Moid') or policy.get('moid')
                        if policy_moid == moid:
                            resolved_name = policy.get('Name') or policy.get('name')
                            if resolved_name:
                                return resolved_name
                except Exception as query_e:
                    logger.debug(f"Failed to query {object_type} policies: {query_e}")
                    
            except Exception as e:
                logger.warning(f"Failed to resolve policy MOID '{moid}' to name: {e}")
        
        return None
    
    def _process_references_for_import(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert name references to MOID references for import.
        Override base method to handle PolicyBucket reconstruction.
        
        Args:
            obj: Object dictionary with name references
            
        Returns:
            Object dictionary with MOID references and reconstructed PolicyBucket
        """
        # First apply base class processing (handles Organization conversion)
        processed = super()._process_references_for_import(obj)
        
        # Convert individual policy fields to PolicyBucket
        processed = self._convert_policy_fields_for_import(processed)
        
        return processed
    
    def _convert_policy_fields_for_import(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert individual policy name fields to PolicyBucket array.
        
        Args:
            obj: Object dictionary with individual policy fields
            
        Returns:
            Object dictionary with PolicyBucket array
        """
        processed = obj.copy()
        
        # Build PolicyBucket from individual policy fields
        policy_bucket = []
        
        # Map of field names to policy types
        policy_field_mapping = {
            'ImcAccessPolicy': 'access.Policy',
            'PowerPolicy': 'power.Policy',
            'SnmpPolicy': 'snmp.Policy',
            'ThermalPolicy': 'thermal.Policy'
        }
        
        for field_name, policy_type in policy_field_mapping.items():
            policy_name = processed.pop(field_name, None)
            
            if policy_name and policy_name.strip():
                try:
                    # Resolve policy name to MOID
                    policy_moid = self._resolve_policy_moid(policy_name, policy_type)
                    
                    if policy_moid:
                        policy_ref = {
                            'Moid': policy_moid,
                            'ObjectType': policy_type
                        }
                        policy_bucket.append(policy_ref)
                        logger.debug(f"Added {policy_type} '{policy_name}' to PolicyBucket")
                    else:
                        logger.warning(f"Could not resolve {policy_type} '{policy_name}' to MOID")
                        
                except Exception as e:
                    logger.error(f"Failed to resolve {policy_type} '{policy_name}': {e}")
        
        # Set PolicyBucket in the processed object
        if policy_bucket:
            processed['PolicyBucket'] = policy_bucket
        
        return processed
    
    def _resolve_policy_moid(self, policy_name: str, policy_type: str) -> Optional[str]:
        """
        Resolve a policy name to its MOID.
        
        Args:
            policy_name: Name of the policy
            policy_type: Type of the policy (e.g., 'access.Policy')
            
        Returns:
            Policy MOID or None if not resolvable
        """
        if not self.api_client:
            return None
        
        try:
            # Use reference resolver if available
            if hasattr(self.api_client, 'resolve_name_to_moid'):
                moid = self.api_client.resolve_name_to_moid(policy_type, policy_name)
                if moid:
                    return moid
            
            # Fallback to querying all policies of this type
            policies = self.api_client.query_objects(policy_type)
            for policy in policies:
                if policy.get('Name') == policy_name:
                    return policy.get('Moid')
            
            logger.warning(f"Policy '{policy_name}' of type '{policy_type}' not found")
            return None
            
        except Exception as e:
            logger.error(f"Error resolving policy '{policy_name}' of type '{policy_type}': {e}")
            return None
    
    def _define_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies for chassis profiles."""
        # Start with base profile dependencies (Organization)
        dependencies = super()._define_dependencies()
        
        # Add policy dependencies - policies must be imported before profiles
        policy_dependencies = {
            DependencyDefinition(
                target_type='access.Policy',
                dependency_type='references',
                required=False,
                description='Chassis profiles may reference IMC Access policies'
            ),
            DependencyDefinition(
                target_type='power.Policy',
                dependency_type='references',
                required=False,
                description='Chassis profiles may reference Power policies'
            ),
            DependencyDefinition(
                target_type='snmp.Policy',
                dependency_type='references',
                required=False,
                description='Chassis profiles may reference SNMP policies'
            ),
            DependencyDefinition(
                target_type='thermal.Policy',
                dependency_type='references',
                required=False,
                description='Chassis profiles may reference Thermal policies'
            )
        }
        
        dependencies.update(policy_dependencies)
        return dependencies
    
    def _extract_user_defined_values(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract user-defined values from chassis profile, including PolicyBucket.
        Override base method to ensure PolicyBucket is captured before transformation.
        
        Args:
            obj: The raw object dictionary from Intersight API
            
        Returns:
            Dictionary containing user-defined values including PolicyBucket
        """
        # Get the standard user-defined values first
        extracted = super()._extract_user_defined_values(obj)
        
        # Specifically include PolicyBucket even though it's not in our field definitions
        # We need this for our export transformation to convert it to individual policy fields
        # Check both PascalCase and snake_case variants
        policy_bucket = obj.get('PolicyBucket') or obj.get('policy_bucket')
        if policy_bucket is not None:
            extracted['PolicyBucket'] = policy_bucket
            logger.debug(f"Included PolicyBucket with {len(policy_bucket)} policies in extracted values")
        
        return extracted
