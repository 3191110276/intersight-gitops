"""
LDAP Policy implementation.

This module implements the LdapPolicy class for handling Cisco Intersight
LDAP Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class LdapPolicy(BasePolicy):
    """
    Implementation for Intersight LDAP Policy objects.
    
    The LDAP policy allows you to configure LDAP settings for user authentication 
    and authorization on managed servers.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "iam.LdapPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "LDAP Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/ldap"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to LDAP Policy according to OpenAPI specification."""
        fields = self._get_common_policy_fields()
        fields.update({
            # Core LDAP Policy Properties (as per OpenAPI spec)
            'EnableDns': FieldDefinition(
                name='EnableDns',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enables DNS to access LDAP servers'
            ),
            'Enabled': FieldDefinition(
                name='Enabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='LDAP server performs authentication',
                default_value=True
            ),
            'UserSearchPrecedence': FieldDefinition(
                name='UserSearchPrecedence',
                field_type=FieldType.STRING,
                required=False,
                description='Search precedence between local user database and LDAP user database',
                enum_values=['LocalUserDb', 'LDAPUserDb'],
                default_value='LocalUserDb'
            ),
            
            # Complex Objects
            'BaseProperties': FieldDefinition(
                name='BaseProperties',
                field_type=FieldType.OBJECT,
                required=False,
                description='Base settings of LDAP required while configuring LDAP policy'
            ),
            'DnsParameters': FieldDefinition(
                name='DnsParameters',
                field_type=FieldType.OBJECT,
                required=False,
                description='Configuration settings to resolve LDAP servers, when DNS is enabled'
            ),
            
            # Relationship Arrays
            'Providers': FieldDefinition(
                name='Providers',
                field_type=FieldType.ARRAY,
                required=False,
                description='Array of LDAP provider configurations'
            ),
            'Groups': FieldDefinition(
                name='Groups',
                field_type=FieldType.ARRAY,
                required=False,
                description='Array of LDAP group mappings'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'EnableDns': False,
            'Enabled': True,
            'UserSearchPrecedence': 'LocalUserDb',
            'BaseProperties': {
                'class_id': 'iam.LdapBaseProperties',
                'object_type': 'iam.LdapBaseProperties',
                'base_dn': 'DC=example,DC=com',
                'bind_dn': 'CN=Administrator,CN=Users,DC=example,DC=com',
                'bind_method': 'ConfiguredCredentials',
                'domain': 'example.com',
                'enable_encryption': True,
                'enable_group_authorization': True,
                'enable_nested_group_search': False,
                'filter': 'sAMAccountName',
                'group_attribute': 'memberOf',
                'nested_group_search_depth': 128,
                'timeout': 0
            },
            'DnsParameters': {
                'class_id': 'iam.LdapDnsParameters',
                'object_type': 'iam.LdapDnsParameters',
                'search_domain': 'example.com',
                'search_forest': 'example.com',
                'source': 'Extracted'
            },
            'Providers': [
                {
                    'class_id': 'iam.LdapProvider',
                    'object_type': 'iam.LdapProvider',
                    'server': 'ldap.example.com',
                    'port': 636,
                    'vendor': 'OpenLDAP'
                }
            ]
        }