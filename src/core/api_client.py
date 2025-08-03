"""
Intersight API client wrapper.

This module provides a wrapper around the Intersight Python SDK that handles
authentication, configuration, and common API operations for the GitOps tool.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import timedelta
import tempfile
import time

import intersight
from intersight.api_client import ApiClient
from intersight.configuration import Configuration
from intersight.signing import HttpSigningConfiguration

from .exceptions import (
    APIConnectionError, AuthenticationError, APITimeoutError, 
    APIRateLimitError, ObjectNotFoundError, ConfigurationError
)
from .error_handler import retry_on_error, RetryConfig, handle_errors, get_global_error_handler


logger = logging.getLogger(__name__)


class IntersightAPIClient:
    """
    Wrapper class for Intersight API client with authentication and error handling.
    
    This class encapsulates the Intersight SDK client and provides methods
    for common operations needed by the GitOps tool.
    """
    
    def __init__(self):
        """Initialize the API client with environment-based configuration."""
        self.config = None
        self.client = None
        self._temp_key_file = None
        self.reference_resolver = None
        self._initialize_client()
        
        # Initialize reference resolver after client is ready
        if self.client:
            from .reference_resolver import ReferenceResolver
            self.reference_resolver = ReferenceResolver(self)
            
            # Initialize organization resolver
            from .organization_resolver import OrganizationResolver
            self.organization_resolver = OrganizationResolver(self)
        
    def _initialize_client(self):
        """Initialize the Intersight API client with authentication."""
        try:
            # Get configuration from environment variables
            api_key = os.getenv('API_KEY')
            api_secret = os.getenv('API_SECRET')
            endpoint = os.getenv('IS_ENDPOINT', 'https://intersight.com')
            
            if not api_key or not api_secret:
                raise ConfigurationError(
                    "API_KEY and API_SECRET environment variables must be set",
                    config_key="API_KEY/API_SECRET",
                    expected_format="API_KEY=<key_id> API_SECRET=<private_key_file_or_content>"
                )
            
            # Handle private key - create temporary file if needed
            api_secret_file = self._prepare_api_secret_file(api_secret)
            
            # Read the private key content from file
            try:
                with open(api_secret_file, 'r') as f:
                    private_key_content = f.read()
            except FileNotFoundError:
                raise ConfigurationError(
                    f"Private key file not found: {api_secret_file}",
                    config_key="API_SECRET",
                    config_value=api_secret,
                    expected_format="Valid file path or PEM-formatted private key content"
                )
            except PermissionError:
                raise ConfigurationError(
                    f"Permission denied reading private key file: {api_secret_file}",
                    config_key="API_SECRET",
                    config_value=api_secret_file
                )
            
            # Configure HTTP signing based on key type (following working example)
            if 'RSA PRIVATE KEY' in private_key_content:
                signing_scheme = intersight.signing.SCHEME_RSA_SHA256
                signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15
                hash_algorithm = intersight.signing.HASH_SHA256
                logger.debug("Detected RSA private key")
            elif 'EC PRIVATE KEY' in private_key_content:
                signing_scheme = intersight.signing.SCHEME_HS2019
                signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_FIPS_186_3
                hash_algorithm = intersight.signing.HASH_SHA256
                logger.debug("Detected EC private key")
            else:
                raise ConfigurationError(
                    "Unsupported private key format. Only RSA and EC private keys are supported.",
                    config_key="API_SECRET",
                    expected_format="PEM-formatted RSA or EC private key"
                )
            
            # Create HTTP signing configuration
            signing_config = HttpSigningConfiguration(
                key_id=api_key,
                private_key_string=private_key_content,
                signing_scheme=signing_scheme,
                signing_algorithm=signing_algorithm,
                hash_algorithm=hash_algorithm,
                signed_headers=[
                    intersight.signing.HEADER_REQUEST_TARGET,
                    intersight.signing.HEADER_HOST,
                    intersight.signing.HEADER_DATE,
                    intersight.signing.HEADER_DIGEST,
                ]
            )
            
            # Create configuration
            self.config = Configuration(
                host=endpoint,
                signing_info=signing_config
            )
            
            # Set additional configuration
            timeout = int(os.getenv('API_TIMEOUT', '30'))
            
            # Enable debug logging if requested
            if os.getenv('DEBUG', 'false').lower() == 'true':
                self.config.debug = True
                
            # Create the API client
            self.client = ApiClient(self.config)
            
            logger.info(f"Initialized Intersight API client for endpoint: {endpoint}")
            
        except (ConfigurationError, AuthenticationError):
            # Re-raise our custom exceptions as-is
            raise
        except Exception as e:
            # Convert other exceptions to APIConnectionError
            raise APIConnectionError(
                f"Failed to initialize Intersight API client: {e}",
                endpoint=os.getenv('IS_ENDPOINT', 'https://intersight.com'),
                cause=e
            )
    
    def _prepare_api_secret_file(self, api_secret: str) -> str:
        """
        Prepare the API secret file for use with Intersight SDK.
        
        Args:
            api_secret: Either file path or the actual private key content
            
        Returns:
            Path to the API secret file
        """
        # Check if it's already a file path
        if os.path.isfile(api_secret):
            logger.debug(f"Using existing API secret file: {api_secret}")
            return api_secret
        else:
            # Handle key content - create temporary file
            key_content = api_secret.replace(r'\n', '\n')
            
            # If it doesn't start with BEGIN, it might be base64 encoded or malformed
            if not key_content.strip().startswith('-----BEGIN'):
                # Try to detect if it's a base64 encoded key without headers
                import base64
                try:
                    # If it's pure base64, add PEM headers
                    decoded = base64.b64decode(key_content + '==')  # Add padding if needed
                    key_content = f"-----BEGIN PRIVATE KEY-----\n{key_content}\n-----END PRIVATE KEY-----"
                except:
                    # If base64 decode fails, assume it's already formatted correctly
                    pass
            
            # Create temporary file for the private key
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False)
            temp_file.write(key_content)
            temp_file.close()
            
            logger.debug(f"Created temporary API secret file: {temp_file.name}")
            
            # Store the temp file path for cleanup later
            self._temp_key_file = temp_file.name
            
            return temp_file.name
    
    @retry_on_error(RetryConfig(
        max_attempts=3,
        retryable_exceptions=(APIConnectionError, APITimeoutError, APIRateLimitError)
    ))
    def query_objects(self, object_type: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Query objects of a specific type from Intersight.
        
        Args:
            object_type: The Intersight object type (e.g., 'organization.Organization')
            **kwargs: Additional query parameters (filter, select, etc.)
            
        Returns:
            List of object dictionaries
        """
        # For large datasets, use the optimized streaming method
        max_objects = kwargs.pop('max_objects', None)
        if max_objects is None or max_objects > 5000:
            # Convert generator to list to maintain consistent return type
            results = []
            for batch in self.query_objects_streaming(object_type, **kwargs):
                results.extend(batch)
            return results
        
        try:
            # Import the appropriate API class based on object type
            api_instance = self._get_api_instance(object_type)
            
            # Build query parameters
            query_params = {}
            
            # Add any additional parameters
            if 'filter' in kwargs:
                query_params['filter'] = kwargs['filter']
            if 'select' in kwargs:
                query_params['select'] = kwargs['select']
            if 'expand' in kwargs:
                query_params['expand'] = kwargs['expand']
            if 'orderby' in kwargs:
                query_params['orderby'] = kwargs['orderby']
                
            # Execute the query
            method_name = f"get_{self._get_collection_name(object_type)}"
            get_method = getattr(api_instance, method_name)
            
            results = []
            skip = 0
            top = min(1000, max_objects) if max_objects else 1000  # Optimal batch size
            
            while True:
                query_params['skip'] = skip
                query_params['top'] = top
                
                response = get_method(**query_params)
                
                if hasattr(response, 'results') and response.results:
                    # Convert to dictionaries
                    batch_results = [obj.to_dict() for obj in response.results]
                    results.extend(batch_results)
                    
                    # Check if we've reached max_objects limit
                    if max_objects and len(results) >= max_objects:
                        results = results[:max_objects]
                        break
                    
                    # Check if we have more data
                    if len(batch_results) < top:
                        break
                    skip += top
                else:
                    break
            
            logger.info(f"Retrieved {len(results)} objects of type {object_type}")
            return results
            
        except intersight.ApiException as e:
            if e.status == 401:
                raise AuthenticationError(
                    f"Authentication failed while querying {object_type}: {e.reason}",
                    api_key=os.getenv('API_KEY', '')[:8] + "...",
                    cause=e
                )
            elif e.status == 403:
                raise AuthenticationError(
                    f"Insufficient permissions to query {object_type}: {e.reason}",
                    cause=e
                )
            elif e.status == 429:
                # Extract retry-after from headers if available
                retry_after = None
                if hasattr(e, 'headers') and 'Retry-After' in e.headers:
                    try:
                        retry_after = int(e.headers['Retry-After'])
                    except (ValueError, KeyError):
                        retry_after = 60
                
                raise APIRateLimitError(
                    f"Rate limit exceeded while querying {object_type}",
                    retry_after=retry_after,
                    cause=e
                )
            elif e.status >= 500:
                raise APIConnectionError(
                    f"Server error while querying {object_type}: {e.reason}",
                    cause=e
                )
            else:
                raise APIConnectionError(
                    f"API error while querying {object_type}: {e.reason}",
                    cause=e
                )
        except Exception as e:
            if 'timeout' in str(e).lower():
                raise APITimeoutError(
                    f"Timeout while querying objects of type {object_type}",
                    operation="query_objects",
                    cause=e
                )
            else:
                raise APIConnectionError(
                    f"Failed to query objects of type {object_type}: {e}",
                    cause=e
                )
    
    def query_objects_streaming(self, object_type: str, **kwargs):
        """
        Query objects using a streaming approach for large datasets.
        
        This method is optimized for handling large datasets by:
        - Using smaller batch sizes to reduce memory usage
        - Implementing progressive loading with callbacks
        - Supporting early termination
        
        Args:
            object_type: The Intersight object type
            **kwargs: Additional query parameters
            
        Yields:
            Batches of object dictionaries
        """
        try:
            # Import the appropriate API class based on object type
            api_instance = self._get_api_instance(object_type)
            
            # Build query parameters
            query_params = {}
            
            # Add any additional parameters
            if 'filter' in kwargs:
                query_params['filter'] = kwargs['filter']
            if 'select' in kwargs:
                query_params['select'] = kwargs['select']
            if 'expand' in kwargs:
                query_params['expand'] = kwargs['expand']
            if 'orderby' in kwargs:
                query_params['orderby'] = kwargs['orderby']
                
            # Execute the query
            method_name = f"get_{self._get_collection_name(object_type)}"
            get_method = getattr(api_instance, method_name)
            
            skip = 0
            top = 500  # Smaller batch size for streaming
            total_retrieved = 0
            
            while True:
                query_params['skip'] = skip
                query_params['top'] = top
                
                response = get_method(**query_params)
                
                if hasattr(response, 'results') and response.results:
                    # Convert to dictionaries
                    batch_results = [obj.to_dict() for obj in response.results]
                    total_retrieved += len(batch_results)
                    
                    # Yield this batch
                    yield batch_results
                    
                    # Check if we have more data
                    if len(batch_results) < top:
                        break
                    skip += top
                else:
                    break
            
            logger.info(f"Streamed {total_retrieved} objects of type {object_type}")
            
        except Exception as e:
            logger.error(f"Failed to stream objects of type {object_type}: {e}")
            raise
    
    def query_objects_batched(self, object_type: str, batch_size: int = 1000, **kwargs) -> List[Dict[str, Any]]:
        """
        Query objects with explicit batch processing for better memory management.
        
        Args:
            object_type: The Intersight object type
            batch_size: Size of each batch (default: 1000)
            **kwargs: Additional query parameters
            
        Returns:
            List of all object dictionaries
        """
        results = []
        
        # Use streaming but collect all results
        for batch in self.query_objects_streaming(object_type, **kwargs):
            results.extend(batch)
            
            # Optional: implement memory pressure detection
            if len(results) > 50000:  # Warn about large datasets
                logger.warning(f"Large dataset detected: {len(results)} objects. Consider using streaming approach.")
        
        return results
    
    def get_object_by_moid(self, object_type: str, moid: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific object by its MOID.
        
        Args:
            object_type: The Intersight object type
            moid: The managed object identifier
            
        Returns:
            Object dictionary or None if not found
        """
        try:
            api_instance = self._get_api_instance(object_type)
            method_name = f"get_{self._get_singular_name(object_type)}_by_moid"
            get_method = getattr(api_instance, method_name)
            
            response = get_method(moid)
            return response.to_dict() if response else None
            
        except Exception as e:
            logger.warning(f"Failed to get object {moid} of type {object_type}: {e}")
            return None
    
    @retry_on_error(RetryConfig(
        max_attempts=5,
        base_delay=2.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=True,
        retryable_exceptions=(
            APIConnectionError,
            APITimeoutError, 
            APIRateLimitError,
        )
    ))
    def create_object(self, object_type: str, object_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new object in Intersight with retry logic.
        
        Args:
            object_type: The Intersight object type
            object_data: Object data dictionary
            
        Returns:
            Created object dictionary
        """
        try:
            api_instance = self._get_api_instance(object_type)
            model_class = self._get_model_class(object_type)
            
            # Create model instance from data
            obj_instance = model_class(**object_data)
            
            # Create the object
            method_name = f"create_{self._get_singular_name(object_type)}"
            create_method = getattr(api_instance, method_name)
            
            response = create_method(obj_instance)
            logger.info(f"Created object of type {object_type}: {response.name}")
            
            return response.to_dict()
            
        except intersight.ApiException as e:
            # Convert Intersight API exceptions to our custom exceptions for retry handling
            if e.status == 401:
                raise AuthenticationError(
                    f"Authentication failed while creating {object_type}: {e.reason}",
                    api_key=os.getenv('API_KEY', '')[:8] + "...",
                    cause=e
                )
            elif e.status == 403:
                raise AuthenticationError(
                    f"Insufficient permissions to create {object_type}: {e.reason}",
                    cause=e
                )
            elif e.status == 429:
                # Extract retry-after from headers if available
                retry_after = 60  # Default
                if hasattr(e, 'headers') and 'Retry-After' in e.headers:
                    try:
                        retry_after = int(e.headers['Retry-After'])
                    except (ValueError, KeyError):
                        pass
                
                raise APIRateLimitError(
                    f"Rate limit exceeded while creating {object_type}",
                    retry_after=retry_after,
                    cause=e
                )
            elif e.status >= 500:
                raise APIConnectionError(
                    f"Server error while creating {object_type}: {e.reason}",
                    cause=e
                )
            else:
                # Non-retryable client error (400-499)
                logger.error(f"Failed to create object of type {object_type}: {e}")
                raise
        except Exception as e:
            if 'timeout' in str(e).lower():
                raise APITimeoutError(
                    f"Timeout while creating object of type {object_type}",
                    operation="create_object",
                    cause=e
                )
            else:
                logger.error(f"Failed to create object of type {object_type}: {e}")
                raise
    
    @retry_on_error(RetryConfig(
        max_attempts=5,
        base_delay=2.0,
        max_delay=60.0,
        exponential_base=2.0,
        jitter=True,
        retryable_exceptions=(
            APIConnectionError,
            APITimeoutError,
            APIRateLimitError,
        )
    ))
    def update_object(self, object_type: str, moid: str, object_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing object in Intersight with retry logic.
        
        Args:
            object_type: The Intersight object type
            moid: The managed object identifier
            object_data: Updated object data dictionary
            
        Returns:
            Updated object dictionary
        """
        try:
            api_instance = self._get_api_instance(object_type)
            model_class = self._get_model_class(object_type)
            
            # Create model instance from data
            obj_instance = model_class(**object_data)
            
            # Update the object
            method_name = f"update_{self._get_singular_name(object_type)}"
            update_method = getattr(api_instance, method_name)
            
            response = update_method(moid, obj_instance)
            logger.info(f"Updated object of type {object_type}: {moid}")
            
            return response.to_dict()
            
        except intersight.ApiException as e:
            # Convert Intersight API exceptions to our custom exceptions for retry handling
            if e.status == 401:
                raise AuthenticationError(
                    f"Authentication failed while updating {object_type}: {e.reason}",
                    api_key=os.getenv('API_KEY', '')[:8] + "...",
                    cause=e
                )
            elif e.status == 403:
                raise AuthenticationError(
                    f"Insufficient permissions to update {object_type}: {e.reason}",
                    cause=e
                )
            elif e.status == 429:
                # Extract retry-after from headers if available
                retry_after = 60  # Default
                if hasattr(e, 'headers') and 'Retry-After' in e.headers:
                    try:
                        retry_after = int(e.headers['Retry-After'])
                    except (ValueError, KeyError):
                        pass
                
                raise APIRateLimitError(
                    f"Rate limit exceeded while updating {object_type}",
                    retry_after=retry_after,
                    cause=e
                )
            elif e.status >= 500:
                raise APIConnectionError(
                    f"Server error while updating {object_type}: {e.reason}",
                    cause=e
                )
            else:
                # Non-retryable client error (400-499)  
                logger.error(f"Failed to update object {moid} of type {object_type}: {e}")
                raise
        except Exception as e:
            if 'timeout' in str(e).lower():
                raise APITimeoutError(
                    f"Timeout while updating object {moid} of type {object_type}",
                    operation="update_object", 
                    cause=e
                )
            else:
                logger.error(f"Failed to update object {moid} of type {object_type}: {e}")
                raise
    
    @retry_on_error(RetryConfig(
        max_attempts=3,
        base_delay=1.0,
        max_delay=30.0,
        exponential_base=2.0,
        jitter=True,
        retryable_exceptions=(
            APIConnectionError,
            APITimeoutError,
            APIRateLimitError,
        )
    ))
    def delete_object(self, object_type: str, moid: str):
        """
        Delete an object from Intersight with retry logic.
        
        Args:
            object_type: The Intersight object type
            moid: The managed object identifier
        """
        try:
            api_instance = self._get_api_instance(object_type)
            method_name = f"delete_{self._get_singular_name(object_type)}"
            delete_method = getattr(api_instance, method_name)
            
            delete_method(moid)
            logger.info(f"Deleted object of type {object_type}: {moid}")
            
        except intersight.ApiException as e:
            # Convert Intersight API exceptions to our custom exceptions for retry handling  
            if e.status == 401:
                raise AuthenticationError(
                    f"Authentication failed while deleting {object_type}: {e.reason}",
                    api_key=os.getenv('API_KEY', '')[:8] + "...",
                    cause=e
                )
            elif e.status == 403:
                raise AuthenticationError(
                    f"Insufficient permissions to delete {object_type}: {e.reason}",
                    cause=e
                )
            elif e.status == 404:
                # Object not found - this is not an error for delete operations
                logger.info(f"Object {moid} of type {object_type} not found (already deleted)")
                return
            elif e.status == 429:
                # Extract retry-after from headers if available
                retry_after = 30  # Default
                if hasattr(e, 'headers') and 'Retry-After' in e.headers:
                    try:
                        retry_after = int(e.headers['Retry-After'])
                    except (ValueError, KeyError):
                        pass
                
                raise APIRateLimitError(
                    f"Rate limit exceeded while deleting {object_type}",
                    retry_after=retry_after,
                    cause=e
                )
            elif e.status >= 500:
                raise APIConnectionError(
                    f"Server error while deleting {object_type}: {e.reason}",
                    cause=e
                )
            else:
                # Non-retryable client error (400-499)
                logger.error(f"Failed to delete object {moid} of type {object_type}: {e}")
                raise
        except Exception as e:
            if 'timeout' in str(e).lower():
                raise APITimeoutError(
                    f"Timeout while deleting object {moid} of type {object_type}",
                    operation="delete_object",
                    cause=e
                )
            else:
                logger.error(f"Failed to delete object {moid} of type {object_type}: {e}")
                raise
    
    def _get_api_instance(self, object_type: str):
        """
        Get the appropriate API instance for an object type.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            API instance
        """
        # Extract module name from object type (e.g., 'organization' from 'organization.Organization')
        module_name = object_type.split('.')[0]
        
        try:
            # Dynamically import the API class
            api_module = __import__(f'intersight.api.{module_name}_api', fromlist=[f'{module_name.title()}Api'])
            api_class = getattr(api_module, f'{module_name.title()}Api')
            return api_class(self.client)
            
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to get API instance for {object_type}: {e}")
            raise
    
    def _get_model_class(self, object_type: str):
        """
        Get the model class for an object type.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Model class
        """
        import re
        
        def camel_to_snake(name):
            """Convert CamelCase to snake_case."""
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
        try:
            # For object_type like "boot.PrecisionPolicy", we want:
            # - module_name: "boot_precision_policy" (snake_case with underscores)
            # - class_name: "BootPrecisionPolicy" (PascalCase, preserve original structure)
            
            type_parts = object_type.split('.')
            
            # Create module name: convert to snake_case
            module_parts = [type_parts[0].lower(), camel_to_snake(type_parts[1])]
            module_name = f'intersight.model.{"_".join(module_parts)}'
            
            # Create class name: preserve PascalCase structure
            class_name = type_parts[0].title() + type_parts[1]
            
            try:
                model_module = __import__(module_name, fromlist=[class_name])
                return getattr(model_module, class_name)
            except ImportError:
                # Try with simple lowercase joining for backwards compatibility
                fallback_module = f'intersight.model.{type_parts[0].lower()}_{type_parts[1].lower()}'
                model_module = __import__(fallback_module, fromlist=[class_name])
                return getattr(model_module, class_name)
            
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to get model class for {object_type}: {e}")
            raise
    
    def _get_collection_name(self, object_type: str) -> str:
        """
        Get the collection name for API methods.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Collection name (plural)
        """
        # Convert object type to API method name format
        parts = object_type.split('.')
        module = parts[0].lower()
        class_name = parts[1]
        
        # Handle special cases for known multi-word class names
        special_cases = {
            'PrecisionPolicy': 'precision_policy',
            'Organization': 'organization',
            'Policy': 'policy'
        }
        
        if class_name in special_cases:
            snake_case = special_cases[class_name]
        else:
            # Convert CamelCase to snake_case for API method names
            import re
            snake_case = re.sub('([A-Z]+)', r'_\1', class_name).lower().lstrip('_')
        
        return f"{module}_{snake_case}_list"
    
    def _get_singular_name(self, object_type: str) -> str:
        """
        Get the singular name for API methods.
        
        Args:
            object_type: The Intersight object type
            
        Returns:
            Singular name
        """
        # Convert object type to API method name format
        parts = object_type.split('.')
        module = parts[0].lower()
        class_name = parts[1]
        
        # Handle special cases for known multi-word class names
        special_cases = {
            'PrecisionPolicy': 'precision_policy',
            'Organization': 'organization',
            'Policy': 'policy'
        }
        
        if class_name in special_cases:
            snake_case = special_cases[class_name]
        else:
            # Convert CamelCase to snake_case for API method names
            import re
            snake_case = re.sub('([A-Z]+)', r'_\1', class_name).lower().lstrip('_')
        
        return f"{module}_{snake_case}"
    
    def resolve_name_to_moid(self, object_type: str, name: str, organization_name: str = None) -> Optional[str]:
        """
        Resolve an object name to its MOID.
        
        Args:
            object_type: The Intersight object type
            name: The object name to resolve
            organization_name: Organization name for scoped objects
            
        Returns:
            MOID string or None if not found
        """
        # Use reference resolver if available for better performance and caching
        if self.reference_resolver:
            return self.reference_resolver.resolve_name_to_moid(object_type, name, organization_name)
        
        # Fallback to direct query if resolver not available
        try:
            filter_expr = f"Name eq '{name}'"
            
            # Add organization filter if applicable
            if organization_name and object_type != 'organization.Organization':
                filter_expr += f" and Organization.Name eq '{organization_name}'"
            
            objects = self.query_objects(object_type, filter=filter_expr)
            
            if objects:
                return objects[0].get('Moid')
            else:
                logger.warning(f"Object '{name}' of type {object_type} not found")
                return None
                
        except Exception as e:
            logger.error(f"Failed to resolve name '{name}' to MOID: {e}")
            return None
    
    def resolve_moid_to_name(self, object_type: str, moid: str) -> Optional[str]:
        """
        Resolve a MOID to its object name.
        
        Args:
            object_type: The Intersight object type
            moid: The MOID to resolve
            
        Returns:
            Object name or None if not found
        """
        # Use reference resolver if available for better performance and caching
        if self.reference_resolver:
            return self.reference_resolver.resolve_moid_to_name(object_type, moid)
        
        # Fallback to direct query if resolver not available
        try:
            obj = self.get_object_by_moid(object_type, moid)
            if obj:
                return obj.get('Name')
            else:
                logger.warning(f"Object with MOID '{moid}' of type {object_type} not found")
                return None
                
        except Exception as e:
            logger.error(f"Failed to resolve MOID '{moid}' to name: {e}")
            return None
    
    def get_organization_moid(self, org_name: str = 'default') -> Optional[str]:
        """
        Get the MOID for an organization by name.
        
        Args:
            org_name: Organization name (defaults to 'default')
            
        Returns:
            Organization MOID or None if not found
        """
        return self.resolve_name_to_moid('organization.Organization', org_name)
    
    def close(self):
        """Close the API client and clean up resources."""
        if self.client:
            # The Intersight SDK doesn't have an explicit close method
            # but we can clean up our references
            self.client = None
            self.config = None
            
        # Clean up temporary key file if created
        if self._temp_key_file and os.path.exists(self._temp_key_file):
            try:
                os.unlink(self._temp_key_file)
                logger.debug(f"Cleaned up temporary key file: {self._temp_key_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary key file: {e}")
            self._temp_key_file = None
            
        logger.info("Closed Intersight API client")