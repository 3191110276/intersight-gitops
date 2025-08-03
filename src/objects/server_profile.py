"""
Server Profile object implementation.

This module implements the ServerProfile class for handling Cisco Intersight
server profile in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set, Optional

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_profile import BaseProfile

logger = logging.getLogger(__name__)


class ServerProfile(BaseProfile):
    """
    Implementation for Intersight Server Profile objects.
    
    Server Profile defines configurations and policies for server profile.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "server.Profile"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Server Profile"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing Server Profile YAML files."""
        return "profiles/server"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for Server Profile objects based on OpenAPI schema."""
        # Start with common profile fields
        fields = self._get_common_profile_fields()
        
        # Add server-specific fields from OpenAPI schema
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
                    fields.update(self._get_fallback_server_fields())
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
                    
                logger.debug(f"Loaded {len(user_defined_fields)} server-specific fields from OpenAPI schema")
                
            except Exception as e:
                logger.warning(f"Failed to load fields from OpenAPI schema: {e}")
                # Fallback to manual field definitions for critical fields
                fields.update(self._get_fallback_server_fields())
        else:
            # No OpenAPI schema available, use fallback definitions
            logger.warning("No OpenAPI schema available, using fallback field definitions")
            fields.update(self._get_fallback_server_fields())
        
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
    
    def _get_fallback_server_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get fallback field definitions for server profiles when OpenAPI is not available.
        
        Returns:
            Dictionary of server-specific field definitions
        """
        return {
            'UserLabel': FieldDefinition(
                name='UserLabel',
                field_type=FieldType.STRING,
                required=False,
                description='User label assigned to the server profile',
                pattern=r'^[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]*$',
                min_length=0,
                max_length=64
            ),
            'AssignedServer': FieldDefinition(
                name='AssignedServer',
                field_type=FieldType.REFERENCE,
                required=False,
                description='Reference to the compute server assigned to this profile',
                reference_type='compute.Blade',
                reference_field='Name'
            ),
            'ConfigChangeContext': FieldDefinition(
                name='ConfigChangeContext',
                field_type=FieldType.OBJECT,
                required=False,
                description='Configuration change context information (read-only)'
            ),
            'ConfigChanges': FieldDefinition(
                name='ConfigChanges',
                field_type=FieldType.OBJECT,
                required=False,
                description='Configuration changes information (read-only)'
            )
        }
    
    def _get_policy_reference_fields(self) -> Dict[str, FieldDefinition]:
        """
        Get policy reference fields that replace PolicyBucket for server profiles.
        Based on OpenAPI analysis, server profiles support all these policy types.
        
        Returns:
            Dictionary of policy reference field definitions
        """
        return {
            # Core Infrastructure Policies
            'AccessPolicy': FieldDefinition(
                name='AccessPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an Access Policy for server or chassis management options',
                reference_type='access.Policy',
                reference_field='Name'
            ),
            'AdapterConfigPolicy': FieldDefinition(
                name='AdapterConfigPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an Adapter Configuration Policy for Ethernet and Fibre-Channel settings',
                reference_type='adapter.ConfigPolicy',
                reference_field='Name'
            ),
            'BiosPolicy': FieldDefinition(
                name='BiosPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a BIOS Policy for setting BIOS tokens on the endpoint',
                reference_type='bios.Policy',
                reference_field='Name'
            ),
            'BootPrecisionPolicy': FieldDefinition(
                name='BootPrecisionPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Boot Order Policy for reusable boot order configuration',
                reference_type='boot.PrecisionPolicy',
                reference_field='Name'
            ),
            
            # Management & Security Policies
            'CertificateManagementPolicy': FieldDefinition(
                name='CertificateManagementPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Certificate Management Policy for certificate and private key configuration',
                reference_type='certificatemanagement.Policy',
                reference_field='Name'
            ),
            'ServerPowerPolicy': FieldDefinition(
                name='ServerPowerPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Server Power Policy to determine power tasks during deploy/undeploy',
                reference_type='compute.ServerPowerPolicy',
                reference_field='Name'
            ),
            'DeviceConnectorPolicy': FieldDefinition(
                name='DeviceConnectorPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Device Connector Policy to control configuration changes from Cisco IMC',
                reference_type='deviceconnector.Policy',
                reference_field='Name'
            ),
            'LocalUserPolicy': FieldDefinition(
                name='LocalUserPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Local User Policy for creating local users on endpoints',
                reference_type='iam.EndPointUserPolicy',
                reference_field='Name'
            ),
            
            # Network & Connectivity Policies
            'LanConnectivityPolicy': FieldDefinition(
                name='LanConnectivityPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a LAN Connectivity Policy for network resources and LAN connections',
                reference_type='vnic.LanConnectivityPolicy',
                reference_field='Name'
            ),
            'SanConnectivityPolicy': FieldDefinition(
                name='SanConnectivityPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a SAN Connectivity Policy for network storage resources and SAN connections',
                reference_type='vnic.SanConnectivityPolicy',
                reference_field='Name'
            ),
            'NetworkConnectivityPolicy': FieldDefinition(
                name='NetworkConnectivityPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Network Connectivity Policy for DNS settings and network configuration',
                reference_type='networkconfig.Policy',
                reference_field='Name'
            ),
            
            # System Configuration Policies
            'KvmPolicy': FieldDefinition(
                name='KvmPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Virtual KVM Policy for KVM Launch settings',
                reference_type='kvm.Policy',
                reference_field='Name'
            ),
            'PersistentMemoryPolicy': FieldDefinition(
                name='PersistentMemoryPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Persistent Memory Policy for Persistent Memory configuration',
                reference_type='memory.PersistentMemoryPolicy',
                reference_field='Name'
            ),
            'NtpPolicy': FieldDefinition(
                name='NtpPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an NTP Policy to configure NTP Servers',
                reference_type='ntp.Policy',
                reference_field='Name'
            ),
            'PowerPolicy': FieldDefinition(
                name='PowerPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Power Policy for power management settings',
                reference_type='power.Policy',
                reference_field='Name'
            ),
            'SnmpPolicy': FieldDefinition(
                name='SnmpPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an SNMP Policy to configure SNMP settings on endpoint',
                reference_type='snmp.Policy',
                reference_field='Name'
            ),
            'SolPolicy': FieldDefinition(
                name='SolPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Serial over LAN Policy',
                reference_type='sol.Policy',
                reference_field='Name'
            ),
            'SshPolicy': FieldDefinition(
                name='SshPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to an SSH Policy for SSH configuration',
                reference_type='ssh.Policy',
                reference_field='Name'
            ),
            'StoragePolicy': FieldDefinition(
                name='StoragePolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Storage Policy for storage configuration',
                reference_type='storage.StoragePolicy',
                reference_field='Name'
            ),
            'SyslogPolicy': FieldDefinition(
                name='SyslogPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Syslog Policy for syslog configuration',
                reference_type='syslog.Policy',
                reference_field='Name'
            ),
            'VmediaPolicy': FieldDefinition(
                name='VmediaPolicy',
                field_type=FieldType.REFERENCE,
                required=False,
                description='A reference to a Virtual Media Policy for virtual media configuration',
                reference_type='vmedia.Policy',
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
            'UserLabel': 'Production-Server-01',
            'AssignedServer': 'server-blade-1-1',
            'AccessPolicy': 'imc-access-production',
            'BiosPolicy': 'bios-virtualization-enabled',
            'BootPrecisionPolicy': 'uefi-local-boot',
            'LanConnectivityPolicy': 'dual-port-lan',
            'SanConnectivityPolicy': 'dual-path-san',
            'PowerPolicy': 'high-performance-power',
            'SnmpPolicy': 'datacenter-snmp',
            'StoragePolicy': 'raid-1-storage'
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
        
        # Initialize all policy fields to None
        policy_fields = {
            'AccessPolicy': 'access.Policy',
            'AdapterConfigPolicy': 'adapter.ConfigPolicy',
            'BiosPolicy': 'bios.Policy',
            'BootPrecisionPolicy': 'boot.PrecisionPolicy',
            'CertificateManagementPolicy': 'certificatemanagement.Policy',
            'ServerPowerPolicy': 'compute.ServerPowerPolicy',
            'DeviceConnectorPolicy': 'deviceconnector.Policy',
            'LocalUserPolicy': 'iam.EndPointUserPolicy',
            'LanConnectivityPolicy': 'vnic.LanConnectivityPolicy',
            'SanConnectivityPolicy': 'vnic.SanConnectivityPolicy',
            'NetworkConnectivityPolicy': 'networkconfig.Policy',
            'KvmPolicy': 'kvm.Policy',
            'PersistentMemoryPolicy': 'memory.PersistentMemoryPolicy',
            'NtpPolicy': 'ntp.Policy',
            'PowerPolicy': 'power.Policy',
            'SnmpPolicy': 'snmp.Policy',
            'SolPolicy': 'sol.Policy',
            'SshPolicy': 'ssh.Policy',
            'StoragePolicy': 'storage.StoragePolicy',
            'SyslogPolicy': 'syslog.Policy',
            'VmediaPolicy': 'vmedia.Policy'
        }
        
        # Initialize all policy fields to None
        for field_name in policy_fields.keys():
            processed[field_name] = None
        
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
                field_name = None
                for fname, ptype in policy_fields.items():
                    if object_type == ptype:
                        field_name = fname
                        break
                
                if field_name:
                    processed[field_name] = policy_name
                    logger.debug(f"Mapped {object_type} '{policy_name}' to field '{field_name}'")
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
            'AccessPolicy': 'access.Policy',
            'AdapterConfigPolicy': 'adapter.ConfigPolicy',
            'BiosPolicy': 'bios.Policy',
            'BootPrecisionPolicy': 'boot.PrecisionPolicy',
            'CertificateManagementPolicy': 'certificatemanagement.Policy',
            'ServerPowerPolicy': 'compute.ServerPowerPolicy',
            'DeviceConnectorPolicy': 'deviceconnector.Policy',
            'LocalUserPolicy': 'iam.EndPointUserPolicy',
            'LanConnectivityPolicy': 'vnic.LanConnectivityPolicy',
            'SanConnectivityPolicy': 'vnic.SanConnectivityPolicy',
            'NetworkConnectivityPolicy': 'networkconfig.Policy',
            'KvmPolicy': 'kvm.Policy',
            'PersistentMemoryPolicy': 'memory.PersistentMemoryPolicy',
            'NtpPolicy': 'ntp.Policy',
            'PowerPolicy': 'power.Policy',
            'SnmpPolicy': 'snmp.Policy',
            'SolPolicy': 'sol.Policy',
            'SshPolicy': 'ssh.Policy',
            'StoragePolicy': 'storage.StoragePolicy',
            'SyslogPolicy': 'syslog.Policy',
            'VmediaPolicy': 'vmedia.Policy'
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
        """Define dependencies for server profiles."""
        # Start with base profile dependencies (Organization)
        dependencies = super()._define_dependencies()
        
        # Add policy dependencies - policies must be imported before profiles
        policy_dependencies = {
            DependencyDefinition(
                target_type='access.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Access policies'
            ),
            DependencyDefinition(
                target_type='adapter.ConfigPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Adapter Configuration policies'
            ),
            DependencyDefinition(
                target_type='bios.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference BIOS policies'
            ),
            DependencyDefinition(
                target_type='boot.PrecisionPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Boot Order policies'
            ),
            DependencyDefinition(
                target_type='certificatemanagement.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Certificate Management policies'
            ),
            DependencyDefinition(
                target_type='compute.ServerPowerPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Server Power policies'
            ),
            DependencyDefinition(
                target_type='deviceconnector.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Device Connector policies'
            ),
            DependencyDefinition(
                target_type='iam.EndPointUserPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Local User policies'
            ),
            DependencyDefinition(
                target_type='vnic.LanConnectivityPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference LAN Connectivity policies'
            ),
            DependencyDefinition(
                target_type='vnic.SanConnectivityPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference SAN Connectivity policies'
            ),
            DependencyDefinition(
                target_type='networkconfig.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Network Connectivity policies'
            ),
            DependencyDefinition(
                target_type='kvm.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Virtual KVM policies'
            ),
            DependencyDefinition(
                target_type='memory.PersistentMemoryPolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Persistent Memory policies'
            ),
            DependencyDefinition(
                target_type='ntp.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference NTP policies'
            ),
            DependencyDefinition(
                target_type='power.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Power policies'
            ),
            DependencyDefinition(
                target_type='snmp.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference SNMP policies'
            ),
            DependencyDefinition(
                target_type='sol.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Serial over LAN policies'
            ),
            DependencyDefinition(
                target_type='ssh.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference SSH policies'
            ),
            DependencyDefinition(
                target_type='storage.StoragePolicy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Storage policies'
            ),
            DependencyDefinition(
                target_type='syslog.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Syslog policies'
            ),
            DependencyDefinition(
                target_type='vmedia.Policy',
                dependency_type='references',
                required=False,
                description='Server profiles may reference Virtual Media policies'
            )
        }
        
        dependencies.update(policy_dependencies)
        return dependencies
    
    def _extract_user_defined_values(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract user-defined values from server profile, including PolicyBucket.
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
