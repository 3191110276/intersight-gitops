"""
Custom exceptions for the Intersight GitOps tool.

This module defines custom exception classes that provide more specific
error information and better error handling capabilities throughout the tool.
"""

from typing import Dict, Any, List, Optional
import logging


class IntersightGitOpsError(Exception):
    """
    Base exception class for all Intersight GitOps tool errors.
    
    This provides a common base for all tool-specific exceptions and includes
    enhanced error context and logging capabilities.
    """
    
    def __init__(self, message: str, error_code: str = None, context: Dict[str, Any] = None, 
                 cause: Exception = None):
        """
        Initialize the exception with enhanced error information.
        
        Args:
            message: Human-readable error message
            error_code: Unique error code for categorization
            context: Additional context information
            cause: The underlying exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.context = context or {}
        self.cause = cause
        
        # Log the error when created
        logger = logging.getLogger(__name__)
        logger.debug(f"Exception created: {self.error_code} - {message}", extra={
            'error_code': self.error_code,
            'context': self.context,
            'cause': str(cause) if cause else None
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the exception to a dictionary for serialization.
        
        Returns:
            Dictionary representation of the exception
        """
        return {
            'error_code': self.error_code,
            'message': self.message,
            'context': self.context,
            'cause': str(self.cause) if self.cause else None
        }


class APIConnectionError(IntersightGitOpsError):
    """Exception raised when API connection fails."""
    
    def __init__(self, message: str, endpoint: str = None, cause: Exception = None):
        context = {'endpoint': endpoint} if endpoint else {}
        super().__init__(message, "API_CONNECTION_ERROR", context, cause)


class AuthenticationError(IntersightGitOpsError):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str, api_key: str = None, cause: Exception = None):
        context = {'api_key': api_key[:8] + "..." if api_key else None}
        super().__init__(message, "AUTHENTICATION_ERROR", context, cause)


class APITimeoutError(IntersightGitOpsError):
    """Exception raised when API requests timeout."""
    
    def __init__(self, message: str, timeout: int = None, operation: str = None, cause: Exception = None):
        context = {'timeout': timeout, 'operation': operation}
        super().__init__(message, "API_TIMEOUT_ERROR", context, cause)


class APIRateLimitError(IntersightGitOpsError):
    """Exception raised when API rate limits are exceeded."""
    
    def __init__(self, message: str, retry_after: int = None, cause: Exception = None):
        context = {'retry_after': retry_after}
        super().__init__(message, "API_RATE_LIMIT_ERROR", context, cause)


class ObjectValidationError(IntersightGitOpsError):
    """Exception raised when object validation fails."""
    
    def __init__(self, message: str, object_name: str = None, object_type: str = None, 
                 validation_errors: List[str] = None, cause: Exception = None):
        context = {
            'object_name': object_name,
            'object_type': object_type,
            'validation_errors': validation_errors or []
        }
        super().__init__(message, "OBJECT_VALIDATION_ERROR", context, cause)


class ObjectNotFoundError(IntersightGitOpsError):
    """Exception raised when a referenced object is not found."""
    
    def __init__(self, message: str, object_name: str = None, object_type: str = None, 
                 search_criteria: Dict[str, Any] = None, cause: Exception = None):
        context = {
            'object_name': object_name,
            'object_type': object_type,
            'search_criteria': search_criteria
        }
        super().__init__(message, "OBJECT_NOT_FOUND_ERROR", context, cause)


class ReferenceResolutionError(IntersightGitOpsError):
    """Exception raised when object references cannot be resolved."""
    
    def __init__(self, message: str, reference_name: str = None, reference_type: str = None, 
                 referring_object: str = None, cause: Exception = None):
        context = {
            'reference_name': reference_name,
            'reference_type': reference_type,
            'referring_object': referring_object
        }
        super().__init__(message, "REFERENCE_RESOLUTION_ERROR", context, cause)


class DependencyResolutionError(IntersightGitOpsError):
    """Exception raised when dependency resolution fails."""
    
    def __init__(self, message: str, object_type: str = None, dependencies: List[str] = None, 
                 circular_deps: List[str] = None, cause: Exception = None):
        context = {
            'object_type': object_type,
            'dependencies': dependencies or [],
            'circular_dependencies': circular_deps or []
        }
        super().__init__(message, "DEPENDENCY_RESOLUTION_ERROR", context, cause)


class YAMLParsingError(IntersightGitOpsError):
    """Exception raised when YAML parsing fails."""
    
    def __init__(self, message: str, file_path: str = None, line_number: int = None, 
                 column_number: int = None, cause: Exception = None):
        context = {
            'file_path': file_path,
            'line_number': line_number,
            'column_number': column_number
        }
        super().__init__(message, "YAML_PARSING_ERROR", context, cause)


class FileSystemError(IntersightGitOpsError):
    """Exception raised when file system operations fail."""
    
    def __init__(self, message: str, file_path: str = None, operation: str = None, 
                 permissions: str = None, cause: Exception = None):
        context = {
            'file_path': file_path,
            'operation': operation,
            'permissions': permissions
        }
        super().__init__(message, "FILESYSTEM_ERROR", context, cause)


class SchemaValidationError(IntersightGitOpsError):
    """Exception raised when OpenAPI schema validation fails."""
    
    def __init__(self, message: str, schema_path: str = None, field_name: str = None, 
                 expected_type: str = None, actual_value: Any = None, cause: Exception = None):
        context = {
            'schema_path': schema_path,
            'field_name': field_name,
            'expected_type': expected_type,
            'actual_value': str(actual_value) if actual_value is not None else None
        }
        super().__init__(message, "SCHEMA_VALIDATION_ERROR", context, cause)


class ImportError(IntersightGitOpsError):
    """Exception raised during object import operations."""
    
    def __init__(self, message: str, object_name: str = None, object_type: str = None, 
                 operation: str = None, cause: Exception = None):
        context = {
            'object_name': object_name,
            'object_type': object_type,
            'operation': operation  # 'create', 'update', 'delete'
        }
        super().__init__(message, "IMPORT_ERROR", context, cause)


class ExportError(IntersightGitOpsError):
    """Exception raised during object export operations."""
    
    def __init__(self, message: str, object_type: str = None, export_count: int = None, 
                 output_dir: str = None, cause: Exception = None):
        context = {
            'object_type': object_type,
            'export_count': export_count,
            'output_dir': output_dir
        }
        super().__init__(message, "EXPORT_ERROR", context, cause)


class ConfigurationError(IntersightGitOpsError):
    """Exception raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: str = None, config_value: str = None, 
                 expected_format: str = None, cause: Exception = None):
        context = {
            'config_key': config_key,
            'config_value': config_value,
            'expected_format': expected_format
        }
        super().__init__(message, "CONFIGURATION_ERROR", context, cause)


class UnsupportedOperationError(IntersightGitOpsError):
    """Exception raised when an unsupported operation is attempted."""
    
    def __init__(self, message: str, operation: str = None, object_type: str = None, 
                 reason: str = None, cause: Exception = None):
        context = {
            'operation': operation,
            'object_type': object_type,
            'reason': reason
        }
        super().__init__(message, "UNSUPPORTED_OPERATION_ERROR", context, cause)


class CriticalError(IntersightGitOpsError):
    """Exception raised for critical errors that require immediate attention."""
    
    def __init__(self, message: str, recovery_suggestions: List[str] = None, cause: Exception = None):
        context = {
            'recovery_suggestions': recovery_suggestions or [],
            'critical': True
        }
        super().__init__(message, "CRITICAL_ERROR", context, cause)


# Error code mappings for quick lookup
ERROR_CODES = {
    'API_CONNECTION_ERROR': APIConnectionError,
    'AUTHENTICATION_ERROR': AuthenticationError,
    'API_TIMEOUT_ERROR': APITimeoutError,
    'API_RATE_LIMIT_ERROR': APIRateLimitError,
    'OBJECT_VALIDATION_ERROR': ObjectValidationError,
    'OBJECT_NOT_FOUND_ERROR': ObjectNotFoundError,
    'REFERENCE_RESOLUTION_ERROR': ReferenceResolutionError,
    'DEPENDENCY_RESOLUTION_ERROR': DependencyResolutionError,
    'YAML_PARSING_ERROR': YAMLParsingError,
    'FILESYSTEM_ERROR': FileSystemError,
    'SCHEMA_VALIDATION_ERROR': SchemaValidationError,
    'IMPORT_ERROR': ImportError,
    'EXPORT_ERROR': ExportError,
    'CONFIGURATION_ERROR': ConfigurationError,
    'UNSUPPORTED_OPERATION_ERROR': UnsupportedOperationError,
    'CRITICAL_ERROR': CriticalError,
}


def get_exception_class(error_code: str) -> type:
    """
    Get the exception class for a given error code.
    
    Args:
        error_code: The error code to look up
        
    Returns:
        Exception class, or IntersightGitOpsError if not found
    """
    return ERROR_CODES.get(error_code, IntersightGitOpsError)