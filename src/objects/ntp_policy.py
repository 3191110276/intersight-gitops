"""
NTP Policy object implementation.

This module implements the NtpPolicy class for handling Cisco Intersight
ntp policy in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class NtpPolicy(BasePolicy):
    """
    Implementation for Intersight NTP Policy objects.
    
    NTP Policy defines settings and configurations for the ntp policy.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "ntp.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "NTP Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing NTP Policy YAML files."""
        return "policies/ntp"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for NTP Policy objects."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add NTP-specific fields based on OpenAPI schema
        fields.update({
            "enabled": FieldDefinition(
                field_type=FieldType.BOOLEAN,
                description="State of NTP service on the endpoint",
                required=False,
                default=True,
                api_field_name="Enabled"
            ),
            "ntp_servers": FieldDefinition(
                field_type=FieldType.ARRAY,
                description="Collection of unauthenticated NTP server IP addresses or hostnames",
                required=False,
                api_field_name="NtpServers"
            ),
            "authenticated_ntp_servers": FieldDefinition(
                field_type=FieldType.ARRAY,
                description="Collection of authenticated NTP servers with respective Key Information",
                required=False,
                api_field_name="AuthenticatedNtpServers"
            ),
            "timezone": FieldDefinition(
                field_type=FieldType.STRING,
                description="Timezone of services on the endpoint",
                required=False,
                default="Pacific/Niue",
                api_field_name="Timezone"
            )
        })
        
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """
        Get example fields specific to this policy type.
        
        Returns:
            Dictionary of example field values
        """
        return {
            "enabled": True,
            "ntp_servers": [
                "pool.ntp.org",
                "time.nist.gov",
                "0.pool.ntp.org"
            ],
            "authenticated_ntp_servers": [
                {
                    "class_id": "ntp.AuthNtpServer",
                    "object_type": "ntp.AuthNtpServer",
                    "server_name": "secure-ntp.example.com",
                    "key_type": "SHA1",
                    "sym_key_id": 1,
                    "sym_key_value": "secret-key-value"
                }
            ],
            "timezone": "America/Los_Angeles"
        }
