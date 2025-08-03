"""
Local User Policy implementation.

This module implements the LocalUserPolicy class for handling Cisco Intersight
Local User Policy objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.objects.base_policy import BasePolicy
from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class LocalUserPolicy(BasePolicy):
    """
    Implementation for Intersight Local User Policy objects.
    
    The Local User policy allows you to configure local user accounts 
    for authentication and authorization on managed servers.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "iam.EndPointUserPolicy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "Local User Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing policy YAML files."""
        return "policies/local_user"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define fields specific to Local User Policy."""
        fields = self._get_common_policy_fields()
        fields.update({
            'PasswordProperties': FieldDefinition(
                name='PasswordProperties',
                field_type=FieldType.OBJECT,
                required=False,
                description='Password properties for the local user policy'
            ),
            'EndPointUserRoles': FieldDefinition(
                name='EndPointUserRoles',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of local users to be configured'
            )
        })
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to this policy type."""
        return {
            'PasswordProperties': {
                'EnforceStrongPassword': True,
                'EnablePasswordExpiry': False,
                'PasswordExpiryDuration': 90,
                'PasswordHistory': 5,
                'NotificationPeriod': 15,
                'GracePeriod': 0
            },
            'EndPointUserRoles': [
                {
                    'Name': 'admin',
                    'Role': 'admin',
                    'Enabled': True
                }
            ]
        }