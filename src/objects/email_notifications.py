"""
E-Mail Notifications implementation.

This module implements the EmailNotifications class for handling Cisco Intersight
E-Mail Notification objects in the GitOps workflow.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import ObjectType, FieldDefinition, FieldType, DependencyDefinition

logger = logging.getLogger(__name__)


class EmailNotifications(ObjectType):
    """
    Implementation for Intersight E-Mail Notification objects.
    
    E-Mail Notifications allow you to configure email settings for 
    sending alerts and notifications from Intersight.
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "notification.EmailSettings"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "E-Mail Notifications"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing notification YAML files."""
        return "notifications/email"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the fields for E-Mail Notification objects."""
        return {
            'Name': FieldDefinition(
                name='Name',
                field_type=FieldType.STRING,
                required=True,
                description='Name of the email notification configuration',
                min_length=1,
                max_length=64
            ),
            'Description': FieldDefinition(
                name='Description',
                field_type=FieldType.STRING,
                required=False,
                description='Description of the email notification configuration'
            ),
            'EmailAddresses': FieldDefinition(
                name='EmailAddresses',
                field_type=FieldType.ARRAY,
                required=False,
                description='List of email addresses to send notifications to'
            ),
            'Enabled': FieldDefinition(
                name='Enabled',
                field_type=FieldType.BOOLEAN,
                required=False,
                description='Enable or disable email notifications',
                default_value=True
            ),
            'ObjectType': FieldDefinition(
                name='ObjectType',
                field_type=FieldType.STRING,
                required=True,
                description='The concrete type of this complex type'
            ),
            'Organization': FieldDefinition(
                name='Organization',
                field_type=FieldType.REFERENCE,
                required=True,
                description='A reference to a organizationOrganization resource',
                reference_type='organization.Organization',
                reference_field='Name'
            ),
            'SenderEmailAddress': FieldDefinition(
                name='SenderEmailAddress',
                field_type=FieldType.STRING,
                required=False,
                description='The email address from which emails are sent'
            ),
            'SmtpPort': FieldDefinition(
                name='SmtpPort',
                field_type=FieldType.INTEGER,
                required=False,
                description='Port number used for SMTP communication',
                default_value=25,
                minimum=1,
                maximum=65535
            ),
            'SmtpServer': FieldDefinition(
                name='SmtpServer',
                field_type=FieldType.STRING,
                required=False,
                description='IP address or hostname of the SMTP server'
            ),
            'Subject': FieldDefinition(
                name='Subject',
                field_type=FieldType.STRING,
                required=False,
                description='Subject line template for email notifications'
            )
        }
    
    def _define_dependencies(self) -> Set[DependencyDefinition]:
        """Define dependencies for E-Mail Notification objects."""
        return {
            DependencyDefinition(
                target_type='organization.Organization',
                dependency_type='references',
                required=True,
                description='E-Mail Notifications must belong to an organization'
            )
        }
    
    def document(self) -> Dict[str, Any]:
        """
        Generate documentation for the E-Mail Notifications object type.
        
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
                'Name': 'example-email-notifications',
                'Description': 'Example email notification configuration',
                'Organization': 'default',
                'Enabled': True,
                'SmtpServer': 'smtp.example.com',
                'SmtpPort': 587,
                'SenderEmailAddress': 'noreply@example.com',
                'Subject': 'Intersight Alert: {AlertType}',
                'EmailAddresses': [
                    'admin@example.com',
                    'ops-team@example.com'
                ]
            }
            
            return {
                'object_type': self.object_type,
                'display_name': self.display_name,
                'description': 'E-Mail Notifications configuration for sending alerts and notifications from Intersight',
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