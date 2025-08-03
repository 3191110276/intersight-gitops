"""
Object registry for managing Intersight object types.

This module provides a central registry for all supported object types,
including dependency resolution and type discovery capabilities.
"""

import logging
from typing import Dict, List, Set, Type, Optional
from collections import defaultdict, deque

from .object_type import ObjectType, DependencyDefinition

logger = logging.getLogger(__name__)


class ObjectRegistry:
    """
    Central registry for all supported Intersight object types.
    
    This class manages the registration and discovery of object types,
    provides dependency resolution, and maintains the relationships
    between different object types.
    """
    
    def __init__(self):
        """Initialize the object registry."""
        self._registered_types: Dict[str, Type[ObjectType]] = {}
        self._instances: Dict[str, ObjectType] = {}
        self._dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self._reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        
    def register_type(self, object_type_class: Type[ObjectType]):
        """
        Register an object type class.
        
        Args:
            object_type_class: The object type class to register
        """
        # Create a temporary instance to get the object type identifier
        temp_instance = object_type_class()
        object_type_id = temp_instance.object_type
        
        if object_type_id in self._registered_types:
            logger.warning(f"Object type {object_type_id} is already registered, overwriting")
        
        self._registered_types[object_type_id] = object_type_class
        
        # Update dependency graph
        self._update_dependency_graph(object_type_id, temp_instance.get_dependencies())
        
        logger.debug(f"Registered object type: {object_type_id}")
    
    def get_registered_types(self) -> Dict[str, Type[ObjectType]]:
        """Get all registered object type classes."""
        return self._registered_types.copy()
    
    def get_object_type_class(self, object_type_id: str) -> Optional[Type[ObjectType]]:
        """
        Get the class for a specific object type.
        
        Args:
            object_type_id: The object type identifier
            
        Returns:
            Object type class or None if not registered
        """
        return self._registered_types.get(object_type_id)
    
    def is_registered(self, object_type_id: str) -> bool:
        """Check if an object type is registered."""
        return object_type_id in self._registered_types
    
    def create_instance(self, object_type_id: str, **kwargs) -> Optional[ObjectType]:
        """
        Create an instance of a registered object type.
        
        Args:
            object_type_id: The object type identifier
            **kwargs: Arguments to pass to the object type constructor
            
        Returns:
            Object type instance or None if not registered
        """
        if object_type_id not in self._registered_types:
            logger.error(f"Object type {object_type_id} is not registered")
            return None
        
        try:
            object_type_class = self._registered_types[object_type_id]
            instance = object_type_class(**kwargs)
            self._instances[object_type_id] = instance
            return instance
        except Exception as e:
            logger.error(f"Failed to create instance of {object_type_id}: {e}")
            return None
    
    def get_instance(self, object_type_id: str) -> Optional[ObjectType]:
        """
        Get an existing instance of an object type.
        
        Args:
            object_type_id: The object type identifier
            
        Returns:
            Object type instance or None if not found
        """
        return self._instances.get(object_type_id)
    
    def get_or_create_instance(self, object_type_id: str, **kwargs) -> Optional[ObjectType]:
        """
        Get an existing instance or create a new one.
        
        Args:
            object_type_id: The object type identifier
            **kwargs: Arguments to pass to the constructor if creating new instance
            
        Returns:
            Object type instance or None if not registered
        """
        instance = self.get_instance(object_type_id)
        if instance is None:
            instance = self.create_instance(object_type_id, **kwargs)
        return instance
    
    def _update_dependency_graph(self, object_type_id: str, dependencies: Set[DependencyDefinition]):
        """
        Update the dependency graph with new dependency information.
        
        Args:
            object_type_id: The object type identifier
            dependencies: Set of dependency definitions
        """
        # Clear existing dependencies for this type
        self._dependency_graph[object_type_id].clear()
        
        # Add new dependencies
        for dep in dependencies:
            self._dependency_graph[object_type_id].add(dep.target_type)
            self._reverse_dependencies[dep.target_type].add(object_type_id)
    
    def get_dependencies(self, object_type_id: str) -> Set[str]:
        """
        Get the dependencies for an object type.
        
        Args:
            object_type_id: The object type identifier
            
        Returns:
            Set of object type identifiers this type depends on
        """
        return self._dependency_graph.get(object_type_id, set()).copy()
    
    def get_dependents(self, object_type_id: str) -> Set[str]:
        """
        Get the object types that depend on a specific type.
        
        Args:
            object_type_id: The object type identifier
            
        Returns:
            Set of object type identifiers that depend on this type
        """
        return self._reverse_dependencies.get(object_type_id, set()).copy()
    
    def has_dependency(self, source_type: str, target_type: str) -> bool:
        """
        Check if one object type depends on another.
        
        Args:
            source_type: The source object type
            target_type: The target object type
            
        Returns:
            True if source_type depends on target_type
        """
        return target_type in self._dependency_graph.get(source_type, set())
    
    def get_dependency_order(self, object_types: Optional[List[str]] = None) -> List[str]:
        """
        Get object types in dependency order (topological sort).
        
        Args:
            object_types: List of object types to order (None for all registered types)
            
        Returns:
            List of object type identifiers in dependency order
        """
        if object_types is None:
            object_types = list(self._registered_types.keys())
        
        # Filter to only include registered types
        valid_types = [t for t in object_types if t in self._registered_types]
        
        return self._topological_sort(valid_types)
    
    def _topological_sort(self, object_types: List[str]) -> List[str]:
        """
        Perform topological sort on object types based on dependencies.
        
        Args:
            object_types: List of object types to sort
            
        Returns:
            List of object types in dependency order
        """
        # Build in-degree count for each node
        in_degree = defaultdict(int)
        for obj_type in object_types:
            in_degree[obj_type] = 0
        
        # Calculate in-degrees
        for obj_type in object_types:
            for dependency in self._dependency_graph.get(obj_type, set()):
                if dependency in in_degree:  # Only count dependencies that are in our subset
                    in_degree[obj_type] += 1
        
        # Kahn's algorithm
        queue = deque([obj_type for obj_type in object_types if in_degree[obj_type] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            # Update in-degrees for dependent types
            for dependent in self._reverse_dependencies.get(current, set()):
                if dependent in in_degree:  # Only process if it's in our subset
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        # Check for circular dependencies
        if len(result) != len(object_types):
            remaining = set(object_types) - set(result)
            logger.warning(f"Circular dependencies detected for object types: {remaining}")
            # Add remaining types to the end
            result.extend(remaining)
        
        return result
    
    def validate_dependencies(self) -> List[str]:
        """
        Validate all dependencies and return any issues found.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        for obj_type, dependencies in self._dependency_graph.items():
            for dep_type in dependencies:
                if dep_type not in self._registered_types:
                    errors.append(f"Object type '{obj_type}' depends on unregistered type '{dep_type}'")
        
        # Check for circular dependencies
        try:
            sorted_types = self._topological_sort(list(self._registered_types.keys()))
            if len(sorted_types) != len(self._registered_types):
                errors.append("Circular dependencies detected in object type graph")
        except Exception as e:
            errors.append(f"Failed to validate dependency graph: {e}")
        
        return errors
    
    def get_dependency_info(self) -> Dict[str, Dict[str, any]]:
        """
        Get comprehensive dependency information for all registered types.
        
        Returns:
            Dictionary with dependency information for each type
        """
        info = {}
        
        for obj_type in self._registered_types:
            info[obj_type] = {
                'dependencies': list(self._dependency_graph.get(obj_type, set())),
                'dependents': list(self._reverse_dependencies.get(obj_type, set())),
                'dependency_count': len(self._dependency_graph.get(obj_type, set())),
                'dependent_count': len(self._reverse_dependencies.get(obj_type, set()))
            }
        
        return info
    
    def clear(self):
        """Clear all registered types and instances."""
        self._registered_types.clear()
        self._instances.clear()
        self._dependency_graph.clear()
        self._reverse_dependencies.clear()
        logger.debug("Object registry cleared")
    
    def __str__(self) -> str:
        """String representation of the registry."""
        return f"ObjectRegistry(types={len(self._registered_types)}, instances={len(self._instances)})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the registry."""
        return (f"ObjectRegistry("
               f"types={list(self._registered_types.keys())}, "
               f"instances={list(self._instances.keys())}, "
               f"dependencies={dict(self._dependency_graph)})")


# Global registry instance
_global_registry = ObjectRegistry()


def get_global_registry() -> ObjectRegistry:
    """Get the global object registry instance."""
    return _global_registry


def register_object_type(object_type_class: Type[ObjectType]):
    """
    Register an object type with the global registry.
    
    Args:
        object_type_class: The object type class to register
    """
    _global_registry.register_type(object_type_class)


def get_registered_types() -> Dict[str, Type[ObjectType]]:
    """Get all registered object types from the global registry."""
    return _global_registry.get_registered_types()


def create_object_instance(object_type_id: str, **kwargs) -> Optional[ObjectType]:
    """
    Create an instance of a registered object type using the global registry.
    
    Args:
        object_type_id: The object type identifier
        **kwargs: Arguments to pass to the constructor
        
    Returns:
        Object type instance or None if not registered
    """
    return _global_registry.create_instance(object_type_id, **kwargs)


def get_dependency_order(object_types: Optional[List[str]] = None) -> List[str]:
    """
    Get object types in dependency order using the global registry.
    
    Args:
        object_types: List of object types to order (None for all)
        
    Returns:
        List of object type identifiers in dependency order
    """
    return _global_registry.get_dependency_order(object_types)