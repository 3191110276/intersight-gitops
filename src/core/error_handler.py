"""
Error handling utilities and decorators for the Intersight GitOps tool.

This module provides centralized error handling, retry logic, and error reporting
capabilities to improve the robustness and user experience of the tool.
"""

import functools
import time
import random
import logging
from typing import Dict, Any, List, Optional, Callable, Type, Union
from dataclasses import dataclass, field
from datetime import datetime
import traceback
import sys

from .exceptions import *


logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """Configuration for retry logic."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: tuple = field(default_factory=lambda: (
        APIConnectionError,
        APITimeoutError,
        APIRateLimitError,
    ))


@dataclass
class ErrorReport:
    """Detailed error report for tracking and analysis."""
    timestamp: datetime
    error_code: str
    message: str
    context: Dict[str, Any]
    stack_trace: str
    recovery_attempted: bool = False
    recovery_successful: bool = False
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error report to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'error_code': self.error_code,
            'message': self.message,
            'context': self.context,
            'stack_trace': self.stack_trace,
            'recovery_attempted': self.recovery_attempted,
            'recovery_successful': self.recovery_successful,
            'retry_count': self.retry_count
        }


class ErrorHandler:
    """
    Centralized error handler for the Intersight GitOps tool.
    
    Provides error reporting, recovery mechanisms, and integration
    with logging and monitoring systems.
    """
    
    def __init__(self):
        self.error_reports: List[ErrorReport] = []
        self.error_counts: Dict[str, int] = {}
        self.recovery_strategies: Dict[str, Callable] = {}
        self._setup_default_recovery_strategies()
    
    def _setup_default_recovery_strategies(self):
        """Set up default recovery strategies for common errors."""
        self.recovery_strategies.update({
            'API_CONNECTION_ERROR': self._recover_api_connection,
            'AUTHENTICATION_ERROR': self._recover_authentication,
            'API_RATE_LIMIT_ERROR': self._recover_rate_limit,
            'REFERENCE_RESOLUTION_ERROR': self._recover_reference_resolution,
        })
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorReport:
        """
        Handle an error by creating a detailed report and attempting recovery.
        
        Args:
            error: The exception that occurred
            context: Additional context information
            
        Returns:
            ErrorReport with details about the error and recovery attempt
        """
        # Determine error code and create enhanced exception if needed
        if isinstance(error, IntersightGitOpsError):
            error_code = error.error_code
            message = error.message
            error_context = error.context.copy()
            error_context.update(context or {})
        else:
            error_code = self._classify_error(error)
            message = str(error)
            error_context = context or {}
        
        # Create error report
        error_report = ErrorReport(
            timestamp=datetime.now(),
            error_code=error_code,
            message=message,
            context=error_context,
            stack_trace=traceback.format_exc()
        )
        
        # Update error counts
        self.error_counts[error_code] = self.error_counts.get(error_code, 0) + 1
        
        # Log the error
        logger.error(f"Error occurred: {error_code} - {message}", extra={
            'error_code': error_code,
            'context': error_context
        })
        
        # Attempt recovery if strategy exists
        if error_code in self.recovery_strategies:
            try:
                error_report.recovery_attempted = True
                recovery_result = self.recovery_strategies[error_code](error, error_context)
                error_report.recovery_successful = recovery_result
                
                if recovery_result:
                    logger.info(f"Successfully recovered from error: {error_code}")
                else:
                    logger.warning(f"Recovery attempt failed for error: {error_code}")
                    
            except Exception as recovery_error:
                logger.error(f"Recovery strategy failed for {error_code}: {recovery_error}")
                error_report.recovery_successful = False
        
        # Store the error report
        self.error_reports.append(error_report)
        
        return error_report
    
    def _classify_error(self, error: Exception) -> str:
        """
        Classify an unknown error based on its type and message.
        
        Args:
            error: The exception to classify
            
        Returns:
            Error code string
        """
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Connection-related errors
        if any(keyword in error_message for keyword in ['connection', 'network', 'unreachable']):
            return 'API_CONNECTION_ERROR'
        
        # Authentication errors
        if any(keyword in error_message for keyword in ['auth', 'unauthorized', 'forbidden', 'credential']):
            return 'AUTHENTICATION_ERROR'
        
        # Timeout errors
        if any(keyword in error_message for keyword in ['timeout', 'timed out']):
            return 'API_TIMEOUT_ERROR'
        
        # File system errors
        if any(keyword in error_message for keyword in ['file not found', 'permission denied', 'disk space']):
            return 'FILESYSTEM_ERROR'
        
        # YAML parsing errors
        if 'yaml' in error_type.lower() or 'parsing' in error_message:
            return 'YAML_PARSING_ERROR'
        
        # Default classification
        return 'UNKNOWN_ERROR'
    
    def _recover_api_connection(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Attempt to recover from API connection errors.
        
        Args:
            error: The connection error
            context: Error context
            
        Returns:
            True if recovery was successful, False otherwise
        """
        logger.info("Attempting to recover from API connection error...")
        
        # Wait before retrying
        time.sleep(2.0)
        
        # For now, just return False to indicate manual intervention needed
        # In a full implementation, this could attempt to reinitialize the API client
        return False
    
    def _recover_authentication(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Attempt to recover from authentication errors.
        
        Args:
            error: The authentication error
            context: Error context
            
        Returns:
            True if recovery was successful, False otherwise
        """
        logger.info("Attempting to recover from authentication error...")
        
        # Authentication errors typically require manual intervention
        # Log helpful information for the user
        logger.error("Authentication failed. Please verify:")
        logger.error("  - API_KEY environment variable is correctly set")
        logger.error("  - API_SECRET points to a valid private key file or contains valid key content")
        logger.error("  - API key has sufficient permissions")
        logger.error("  - API key is not expired or revoked")
        
        return False
    
    def _recover_rate_limit(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Attempt to recover from rate limit errors.
        
        Args:
            error: The rate limit error
            context: Error context
            
        Returns:
            True if recovery was successful, False otherwise
        """
        logger.info("Attempting to recover from rate limit error...")
        
        # Extract retry-after if available
        retry_after = context.get('retry_after', 60)
        logger.info(f"Waiting {retry_after} seconds before retrying...")
        
        time.sleep(retry_after)
        return True
    
    def _recover_reference_resolution(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Attempt to recover from reference resolution errors.
        
        Args:
            error: The reference resolution error
            context: Error context
            
        Returns:
            True if recovery was successful, False otherwise
        """
        logger.info("Attempting to recover from reference resolution error...")
        
        # Reference resolution errors often indicate missing dependencies
        # Log helpful information for the user
        reference_name = context.get('reference_name')
        reference_type = context.get('reference_type')
        
        if reference_name and reference_type:
            logger.warning(f"Could not resolve reference: {reference_name} of type {reference_type}")
            logger.warning("This may indicate:")
            logger.warning("  - The referenced object doesn't exist in Intersight")
            logger.warning("  - The referenced object is in a different organization")
            logger.warning("  - There's a typo in the reference name")
            logger.warning("  - Dependencies are not imported in the correct order")
        
        return False
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all errors encountered.
        
        Returns:
            Dictionary containing error statistics and details
        """
        total_errors = len(self.error_reports)
        
        if total_errors == 0:
            return {
                'total_errors': 0,
                'error_counts': {},
                'recovery_success_rate': 0.0,
                'critical_errors': []
            }
        
        # Calculate recovery success rate
        recovery_attempts = sum(1 for report in self.error_reports if report.recovery_attempted)
        successful_recoveries = sum(1 for report in self.error_reports if report.recovery_successful)
        recovery_success_rate = (successful_recoveries / recovery_attempts * 100) if recovery_attempts > 0 else 0.0
        
        # Identify critical errors
        critical_errors = [
            report for report in self.error_reports 
            if report.error_code == 'CRITICAL_ERROR' or 
               report.error_code in ['AUTHENTICATION_ERROR', 'CONFIGURATION_ERROR']
        ]
        
        return {
            'total_errors': total_errors,
            'error_counts': self.error_counts.copy(),
            'recovery_success_rate': recovery_success_rate,
            'critical_errors': [error.to_dict() for error in critical_errors[-5:]],  # Last 5 critical errors
            'recent_errors': [report.to_dict() for report in self.error_reports[-10:]]  # Last 10 errors
        }
    
    def clear_errors(self):
        """Clear all stored error reports and counts."""
        self.error_reports.clear()
        self.error_counts.clear()
        logger.info("Error reports cleared")
    
    def export_error_report(self, file_path: str):
        """
        Export detailed error report to a file.
        
        Args:
            file_path: Path where to save the error report
        """
        import json
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'summary': self.get_error_summary(),
            'detailed_errors': [report.to_dict() for report in self.error_reports]
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"Error report exported to: {file_path}")
        except Exception as e:
            logger.error(f"Failed to export error report: {e}")


def retry_on_error(config: RetryConfig = None):
    """
    Decorator that adds retry logic to functions.
    
    Args:
        config: Retry configuration, uses default if None
        
    Returns:
        Decorated function with retry logic
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                    
                except config.retryable_exceptions as e:
                    last_exception = e
                    
                    if attempt == config.max_attempts - 1:
                        # Last attempt failed, re-raise the exception
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        config.base_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    
                    # Add jitter to prevent thundering herd
                    if config.jitter:
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
                
                except Exception as e:
                    # Non-retryable exception, re-raise immediately
                    raise
            
            # This should never be reached, but just in case
            raise last_exception
        
        return wrapper
    return decorator


def handle_errors(error_handler: ErrorHandler = None):
    """
    Decorator that adds comprehensive error handling to functions.
    
    Args:
        error_handler: ErrorHandler instance, creates default if None
        
    Returns:
        Decorated function with error handling
    """
    if error_handler is None:
        error_handler = ErrorHandler()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Handle the error and create report
                error_report = error_handler.handle_error(e, {
                    'function': func.__name__,
                    'args': str(args)[:200],  # Truncate long arguments
                    'kwargs': str(kwargs)[:200]
                })
                
                # Re-raise the original exception (or enhanced version)
                if isinstance(e, IntersightGitOpsError):
                    raise
                else:
                    # Convert to our custom exception type
                    enhanced_error = IntersightGitOpsError(
                        str(e),
                        error_report.error_code,
                        error_report.context,
                        e
                    )
                    raise enhanced_error from e
        
        return wrapper
    return decorator


def safe_execute(func: Callable, *args, default=None, error_handler: ErrorHandler = None, **kwargs):
    """
    Safely execute a function with error handling, returning a default value on failure.
    
    Args:
        func: Function to execute
        *args: Positional arguments for the function
        default: Default value to return on error
        error_handler: ErrorHandler instance
        **kwargs: Keyword arguments for the function
        
    Returns:
        Function result or default value
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if error_handler:
            error_handler.handle_error(e, {
                'function': func.__name__ if hasattr(func, '__name__') else 'unknown',
                'safe_execution': True
            })
        else:
            logger.error(f"Safe execution failed: {e}")
        
        return default


# Global error handler instance
_global_error_handler = ErrorHandler()


def get_global_error_handler() -> ErrorHandler:
    """Get the global error handler instance."""
    return _global_error_handler


def reset_global_error_handler():
    """Reset the global error handler instance."""
    global _global_error_handler
    _global_error_handler = ErrorHandler()