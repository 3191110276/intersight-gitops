#!/usr/bin/env python3
"""
Intersight GitOps Import Script.

This script imports YAML files containing Intersight object definitions
and synchronizes them with Intersight. It supports creating, updating,
and deleting objects based on the difference between YAML files and
current Intersight state.

Usage:
    python import.py [--input-dir INPUT_DIR] [--object-types TYPE1,TYPE2] [--dry-run] [--safe-mode]

Environment Variables:
    API_KEY: Intersight API Key ID
    API_SECRET: Intersight API Secret Key (file path or key content)
    IS_ENDPOINT: Intersight API endpoint (default: https://intersight.com)
    FILES_DIR: Input directory for YAML files (default: ./files)
    SAFE_MODE: Prevent destructive operations (default: false)
    LOG_LEVEL: Logging level (default: INFO)
    DEBUG: Enable debug mode (default: false)
"""

import os
import sys
import argparse
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, List, Set
from collections import defaultdict, deque

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.api_client import IntersightAPIClient
from objects.organization import Organization
from objects.bios_policy import BiosPolicy
from objects.boot_policy import BootPolicy
from objects.memory_policy import MemoryPolicy
from objects.persistent_memory_policy import PersistentMemoryPolicy

# Import all policy types
from objects.adapter_config_policy import AdapterConfigPolicy
from objects.access_policy import AccessPolicy
from objects.certificate_policy import CertificatePolicy
from objects.device_connector_policy import DeviceConnectorPolicy
from objects.ethernet_adapter_policy import EthernetAdapterPolicy
from objects.fibre_channel_adapter_policy import FibreChannelAdapterPolicy
from objects.firmware_policy import FirmwarePolicy
from objects.ipmi_policy import IpmiPolicy
from objects.iscsi_adapter_policy import IscsiAdapterPolicy
from objects.iscsi_boot_policy import IscsiBootPolicy
from objects.iscsi_static_target_policy import IscsiStaticTargetPolicy
from objects.kvm_policy import KvmPolicy
from objects.network_policy import NetworkPolicy
from objects.ntp_policy import NtpPolicy
from objects.power_policy import PowerPolicy
from objects.sdcard_policy import SdCardPolicy
from objects.smtp_policy import SmtpPolicy
from objects.snmp_policy import SnmpPolicy
from objects.sol_policy import SolPolicy
from objects.ssh_policy import SshPolicy
from objects.syslog_policy import SyslogPolicy
from objects.thermal_policy import ThermalPolicy
from objects.vmedia_policy import VmediaPolicy
from objects.vsan_policy import VsanPolicy
from objects.vlan_policy import VlanPolicy
from objects.local_user_policy import LocalUserPolicy
from objects.ldap_policy import LdapPolicy
from objects.scrub_policy import ScrubPolicy
from objects.link_control_policy import LinkControlPolicy
from objects.flow_control_policy import FlowControlPolicy
from objects.link_aggregation_policy import LinkAggregationPolicy
from objects.multicast_policy import MulticastPolicy
from objects.system_qos_policy import SystemQosPolicy
from objects.port_policy import PortPolicy
from objects.switch_control_policy import SwitchControlPolicy
from objects.ethernet_network_group_policy import EthernetNetworkGroupPolicy
from objects.ethernet_qos_policy import EthernetQosPolicy
from objects.fc_qos_policy import FcQosPolicy
from objects.fc_zone_policy import FcZonePolicy
from objects.drive_security_policy import DriveSecurityPolicy
from objects.storage_policy import StoragePolicy
from objects.server_pool_qualification_policy import ServerPoolQualificationPolicy

# Import all profile types
from objects.chassis_profile import ChassisProfile
from objects.server_profile import ServerProfile
from objects.domain_profile import DomainProfile

# Import all pool types
from objects.fc_pool import FcPool
from objects.ip_pool import IpPool
from objects.iqn_pool import IqnPool
from objects.mac_pool import MacPool
from objects.resource_pool import ResourcePool
from objects.uuid_pool import UuidPool


def setup_logging(log_level: str = None, debug: bool = False):
    """Set up logging configuration."""
    if debug or os.getenv('DEBUG', 'false').lower() == 'true':
        level = logging.DEBUG
    else:
        level = getattr(logging, (log_level or os.getenv('LOG_LEVEL', 'INFO')).upper())
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )




def _expand_object_type(simplified_type: str) -> str:
    """
    Convert ObjectType from x format or folder/x format to x.y format for import processing.
    
    Examples:
        bios -> bios.Policy
        policies/bios -> bios.Policy
        organization -> organization.Organization
        organizations/organization -> organization.Organization
        boot -> boot.PrecisionPolicy
        memory -> memory.Policy
    
    Args:
        simplified_type: Simplified object type string (e.g., "bios" or "policies/bios")
        
    Returns:
        Full object type string (e.g., "bios.Policy")
    """
    # Handle folder-aware format (e.g., "policies/bios" -> "bios")
    if '/' in simplified_type:
        _, base_type = simplified_type.split('/', 1)
    else:
        base_type = simplified_type
    
    # Common mapping of simplified types to full types
    type_mapping = {
        # Organizations
        'organization': 'organization.Organization',
        
        # Policies
        'adapter_config': 'adapter.ConfigPolicy',
        'bios': 'bios.Policy',
        'boot': 'boot.PrecisionPolicy',
        'memory': 'memory.Policy',
        'persistent_memory': 'memory.PersistentMemoryPolicy',
        'access': 'access.Policy',
        'certificate': 'certificatemanagement.Policy',
        'device_connector': 'deviceconnector.Policy',
        'firmware': 'firmware.Policy',
        'ipmi': 'ipmioverlan.Policy',
        'iscsi_adapter': 'vnic.IscsiAdapterPolicy',
        'iscsi_boot': 'vnic.IscsiBootPolicy',
        'iscsi_static_target': 'vnic.IscsiStaticTargetPolicy',
        'kvm': 'kvm.Policy',
        'network': 'networkconfig.Policy',
        'ntp': 'ntp.Policy',
        'power': 'power.Policy',
        'sdcard': 'sdcard.Policy',
        'smtp': 'smtp.Policy',
        'snmp': 'snmp.Policy',
        'sol': 'sol.Policy',
        'ssh': 'ssh.Policy',
        'syslog': 'syslog.Policy',
        'thermal': 'thermal.Policy',
        'vmedia': 'vmedia.Policy',
        'scrub': 'compute.ScrubPolicy',
        'drive_security': 'storage.DriveSecurityPolicy',
        'ethernet_adapter': 'vnic.EthAdapterPolicy',
        'ethernet_qos': 'vnic.EthQosPolicy',
        'link_control': 'fabric.LinkControlPolicy',
        'link_aggregation': 'fabric.LinkAggregationPolicy',
        'flow_control': 'fabric.FlowControlPolicy',
        'multicast': 'fabric.MulticastPolicy',
        'system_qos': 'fabric.SystemQosPolicy',
        'switch_control': 'fabric.SwitchControlPolicy',
        'ethernet_network_group': 'fabric.EthNetworkGroupPolicy',
        'vlan': 'fabric.EthNetworkPolicy',
        'vsan': 'fabric.FcNetworkPolicy',
        'fc_qos': 'vnic.FcQosPolicy',
        'fibre_channel_adapter': 'vnic.FcAdapterPolicy',
        'fc_zone': 'fabric.FcZonePolicy',
        'local_user': 'iam.EndPointUserPolicy',
        'ldap': 'iam.LdapPolicy',
        'port': 'fabric.PortPolicy',
        
        # Profiles
        'server': 'server.Profile',
        'chassis': 'chassis.Profile',
        
        # Pools
        'fc': 'fcpool.Pool',
        'ip': 'ippool.Pool',
        'iqn': 'iqnpool.Pool',
        'mac': 'macpool.Pool',
        'resource': 'resourcepool.Pool',
        'uuid': 'uuidpool.Pool'
    }
    
    # Return mapped value or assume it's already in full format
    return type_mapping.get(base_type, base_type)


def get_available_importers(api_client: IntersightAPIClient) -> Dict[str, Any]:
    """
    Get available object importers.
    
    Returns:
        Dictionary mapping object types to their importer instances
    """
    importers = {}
    
    # Initialize Organization importer
    org_importer = Organization(api_client=api_client)
    importers[org_importer.object_type] = org_importer
    
    # Initialize all Policy importers
    policy_classes = [
        AdapterConfigPolicy, BiosPolicy, BootPolicy, MemoryPolicy, PersistentMemoryPolicy,
        AccessPolicy, CertificatePolicy, DeviceConnectorPolicy,
        FirmwarePolicy, IpmiPolicy, IscsiAdapterPolicy, IscsiBootPolicy, IscsiStaticTargetPolicy, KvmPolicy,
        NetworkPolicy, NtpPolicy, PowerPolicy,
        SdCardPolicy, SmtpPolicy, SnmpPolicy,
        SolPolicy, SshPolicy, SyslogPolicy,
        ThermalPolicy, VmediaPolicy, VsanPolicy, VlanPolicy,
        LocalUserPolicy, LdapPolicy, ScrubPolicy, LinkControlPolicy, FlowControlPolicy,
        LinkAggregationPolicy, MulticastPolicy, SystemQosPolicy, PortPolicy, SwitchControlPolicy,
        EthernetNetworkGroupPolicy, EthernetAdapterPolicy, FibreChannelAdapterPolicy, EthernetQosPolicy, FcQosPolicy, FcZonePolicy, DriveSecurityPolicy,
        ServerPoolQualificationPolicy
    ]
    
    for policy_class in policy_classes:
        policy_importer = policy_class(api_client=api_client)
        importers[policy_importer.object_type] = policy_importer
    
    # Initialize Profile importers
    profile_classes = [ChassisProfile, ServerProfile, DomainProfile]
    
    for profile_class in profile_classes:
        profile_importer = profile_class(api_client=api_client)
        importers[profile_importer.object_type] = profile_importer
    
    # Initialize Pool importers
    pool_classes = [FcPool, IpPool, IqnPool, MacPool, ResourcePool, UuidPool]
    
    for pool_class in pool_classes:
        pool_importer = pool_class(api_client=api_client)
        importers[pool_importer.object_type] = pool_importer
    
    return importers


def discover_yaml_files(input_dir: str) -> Dict[str, List[str]]:
    """
    Discover YAML files in the input directory.
    
    Args:
        input_dir: Directory to search for YAML files
        
    Returns:
        Dictionary mapping object types to lists of file paths
    """
    logger = logging.getLogger(__name__)
    
    yaml_files = defaultdict(list)
    
    # Search for YAML files recursively
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.warning(f"Input directory does not exist: {input_dir}")
        return yaml_files
    
    for yaml_file in input_path.rglob("*.yaml"):
        if yaml_file.is_file():
            try:
                # Load the YAML file to determine object type
                with open(yaml_file, 'r') as f:
                    content = yaml.safe_load(f)
                
                if isinstance(content, dict) and 'ObjectType' in content:
                    object_type = content['ObjectType']
                    # Expand simplified ObjectType to full format for processing
                    full_object_type = _expand_object_type(object_type)
                    yaml_files[full_object_type].append(str(yaml_file))
                else:
                    logger.warning(f"YAML file missing ObjectType field: {yaml_file}")
                    
            except Exception as e:
                logger.error(f"Failed to parse YAML file {yaml_file}: {e}")
    
    # Also check for .yml extension
    for yml_file in input_path.rglob("*.yml"):
        if yml_file.is_file():
            try:
                with open(yml_file, 'r') as f:
                    content = yaml.safe_load(f)
                
                if isinstance(content, dict) and 'ObjectType' in content:
                    object_type = content['ObjectType']
                    # Expand simplified ObjectType to full format for processing
                    full_object_type = _expand_object_type(object_type)
                    if str(yml_file) not in yaml_files[full_object_type]:  # Avoid duplicates
                        yaml_files[full_object_type].append(str(yml_file))
                else:
                    logger.warning(f"YAML file missing ObjectType field: {yml_file}")
                    
            except Exception as e:
                logger.error(f"Failed to parse YAML file {yml_file}: {e}")
    
    return dict(yaml_files)


def discover_yaml_files_parallel(input_dir: str) -> Dict[str, List[str]]:
    """
    Discover YAML files in the input directory using parallel processing.
    
    Args:
        input_dir: Directory to search for YAML files
        
    Returns:
        Dictionary mapping object types to lists of file paths
    """
    import concurrent.futures
    import threading
    from collections import defaultdict
    
    logger = logging.getLogger(__name__)
    
    # Search for YAML files recursively
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.warning(f"Input directory does not exist: {input_dir}")
        return {}
    
    # Collect all YAML files
    yaml_file_paths = []
    for yaml_file in input_path.rglob("*.yaml"):
        if yaml_file.is_file():
            yaml_file_paths.append(yaml_file)
    for yml_file in input_path.rglob("*.yml"):
        if yml_file.is_file():
            yaml_file_paths.append(yml_file)
    
    if not yaml_file_paths:
        return {}
    
    yaml_files = defaultdict(list)
    yaml_files_lock = threading.Lock()
    
    def process_yaml_file(file_path: Path) -> tuple:
        """Process a single YAML file and return its object type."""
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
            
            if isinstance(content, dict) and 'ObjectType' in content:
                object_type = content['ObjectType']
                full_object_type = _expand_object_type(object_type)
                return str(file_path), full_object_type, None
            else:
                return str(file_path), None, f"YAML file missing ObjectType field: {file_path}"
                
        except Exception as e:
            return str(file_path), None, f"Failed to parse YAML file {file_path}: {e}"
    
    # Process files in parallel
    max_workers = min(8, len(yaml_file_paths), os.cpu_count() or 1)
    logger.debug(f"Processing {len(yaml_file_paths)} YAML files with {max_workers} threads")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_yaml_file, file_path): file_path
            for file_path in yaml_file_paths
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            file_path, object_type, error = future.result()
            
            if error:
                logger.warning(error)
            elif object_type:
                with yaml_files_lock:
                    if file_path not in yaml_files[object_type]:  # Avoid duplicates
                        yaml_files[object_type].append(file_path)
    
    return dict(yaml_files)


def load_yaml_objects(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Load objects from YAML files.
    
    Args:
        file_paths: List of YAML file paths
        
    Returns:
        List of object dictionaries
    """
    logger = logging.getLogger(__name__)
    objects = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
            
            if isinstance(content, dict):
                # Convert ObjectType from simplified format to full format for import processing
                if 'ObjectType' in content:
                    content['ObjectType'] = _expand_object_type(content['ObjectType'])
                objects.append(content)
            elif isinstance(content, list):
                # Process each object in the list
                for obj in content:
                    if isinstance(obj, dict) and 'ObjectType' in obj:
                        obj['ObjectType'] = _expand_object_type(obj['ObjectType'])
                objects.extend(content)
            else:
                logger.warning(f"Unexpected YAML content in {file_path}")
                
        except Exception as e:
            logger.error(f"Failed to load YAML file {file_path}: {e}")
    
    return objects


def load_yaml_objects_optimized(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Load objects from YAML files with optimized batch processing and memory management.
    
    Args:
        file_paths: List of YAML file paths
        
    Returns:
        List of object dictionaries
    """
    import concurrent.futures
    import threading
    
    logger = logging.getLogger(__name__)
    objects = []
    objects_lock = threading.Lock()
    
    def load_yaml_file(file_path: str) -> tuple:
        """Load a single YAML file and return its contents."""
        try:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f)
            
            file_objects = []
            if isinstance(content, dict):
                # Convert ObjectType from simplified format to full format for import processing
                if 'ObjectType' in content:
                    content['ObjectType'] = _expand_object_type(content['ObjectType'])
                file_objects.append(content)
            elif isinstance(content, list):
                # Process each object in the list
                for obj in content:
                    if isinstance(obj, dict) and 'ObjectType' in obj:
                        obj['ObjectType'] = _expand_object_type(obj['ObjectType'])
                        file_objects.append(obj)
            else:
                return file_path, [], f"Unexpected YAML content in {file_path}"
                
            return file_path, file_objects, None
                
        except Exception as e:
            return file_path, [], f"Failed to load YAML file {file_path}: {e}"
    
    # Process files in smaller batches to manage memory usage
    batch_size = 50  # Process files in batches of 50
    total_files = len(file_paths)
    
    for i in range(0, total_files, batch_size):
        batch_files = file_paths[i:i + batch_size]
        logger.debug(f"Loading batch {i//batch_size + 1}/{(total_files + batch_size - 1)//batch_size}: {len(batch_files)} files")
        
        # Use limited parallelism for file I/O to avoid overwhelming the system
        max_workers = min(8, len(batch_files), os.cpu_count() or 1)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(load_yaml_file, file_path): file_path
                for file_path in batch_files
            }
            
            for future in concurrent.futures.as_completed(future_to_file):
                file_path, file_objects, error = future.result()
                
                if error:
                    logger.error(error)
                else:
                    with objects_lock:
                        objects.extend(file_objects)
    
    logger.debug(f"Loaded {len(objects)} total objects from {total_files} YAML files")
    return objects


def build_dependency_graph(importers: Dict[str, Any]) -> Dict[str, Set[str]]:
    """
    Build a dependency graph for object types.
    
    Args:
        importers: Dictionary of available importers
        
    Returns:
        Dictionary mapping object types to their dependencies
    """
    dependencies = {}
    
    for object_type, importer in importers.items():
        # Get dependency types from the importer
        dep_types = {dep.target_type for dep in importer.get_dependencies()}
        dependencies[object_type] = dep_types
    
    return dependencies


def topological_sort(dependencies: Dict[str, Set[str]], available_types: Set[str]) -> List[str]:
    """
    Perform topological sort on object types based on dependencies.
    
    Args:
        dependencies: Dependency graph
        available_types: Set of object types that are available for import
        
    Returns:
        List of object types in dependency order
    """
    logger = logging.getLogger(__name__)
    
    # Filter dependencies to only include available types
    filtered_deps = {}
    for obj_type in available_types:
        if obj_type in dependencies:
            filtered_deps[obj_type] = dependencies[obj_type] & available_types
        else:
            filtered_deps[obj_type] = set()
    
    # Kahn's algorithm for topological sorting
    in_degree = defaultdict(int)
    for obj_type in available_types:
        in_degree[obj_type] = 0
    
    for obj_type, deps in filtered_deps.items():
        for dep in deps:
            in_degree[obj_type] += 1
    
    queue = deque([obj_type for obj_type in available_types if in_degree[obj_type] == 0])
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Update in-degrees for dependent types
        for obj_type, deps in filtered_deps.items():
            if current in deps:
                in_degree[obj_type] -= 1
                if in_degree[obj_type] == 0:
                    queue.append(obj_type)
    
    # Check for circular dependencies
    if len(result) != len(available_types):
        remaining = available_types - set(result)
        logger.warning(f"Circular dependencies detected for object types: {remaining}")
        # Add remaining types to the end
        result.extend(remaining)
    
    return result


def import_objects(input_dir: str, importers: Dict[str, Any], object_types: List[str] = None, 
                  dry_run: bool = False, safe_mode: bool = None, api_client: Any = None,
                  validate_only: bool = False, show_diff: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """
    Import objects from YAML files with proper operation sequencing.
    
    Operations are performed in three phases:
    1. Creates (in dependency order)
    2. Updates (in dependency order) 
    3. Deletes (in reverse dependency order)
    
    Args:
        input_dir: Directory containing YAML files
        importers: Dictionary of available importers
        object_types: List of specific object types to import (None for all)
        dry_run: If True, don't actually make changes
        safe_mode: If True, prevent destructive operations
        
    Returns:
        Dictionary with overall import results
    """
    import concurrent.futures
    import threading
    
    logger = logging.getLogger(__name__)
    
    # Handle safe mode
    if safe_mode is None:
        safe_mode = os.getenv('SAFE_MODE', 'false').lower() == 'true'
    
    if safe_mode:
        logger.info("SAFE MODE: Destructive operations will be prevented")
    
    # Handle validation mode
    if validate_only:
        logger.info("VALIDATION MODE: Only checking YAML files without applying changes")
        dry_run = True  # Force dry run for validation mode
    
    if show_diff:
        logger.info("DIFF MODE: Showing differences between YAML and current state")
    
    # Initialize organization resolver if API client is available
    if api_client and hasattr(api_client, 'organization_resolver'):
        logger.info("Initializing organization resolver...")
        # Load exported organizations for resolution
        api_client.organization_resolver.load_exported_organizations(input_dir)
        # Preload organizations from API for better performance
        api_client.organization_resolver.preload_organizations_from_api()
    
    # Discover YAML files with parallel processing
    logger.info(f"Discovering YAML files in {input_dir}...")
    yaml_files = discover_yaml_files_parallel(input_dir)
    
    if not yaml_files:
        logger.warning("No YAML files found with valid ObjectType fields")
        return {
            'total_created': 0,
            'total_updated': 0,
            'total_deleted': 0,
            'total_errors': 0,
            'results': {}
        }
    
    # Filter by requested object types
    if object_types:
        yaml_files = {k: v for k, v in yaml_files.items() if k in object_types}
        if not yaml_files:
            logger.warning(f"No YAML files found for requested object types: {object_types}")
            return {
                'total_created': 0,
                'total_updated': 0,
                'total_deleted': 0,
                'total_errors': 0,
                'results': {}
            }
    
    # Filter by available importers
    yaml_files = {k: v for k, v in yaml_files.items() if k in importers}
    
    logger.info(f"Found YAML files for {len(yaml_files)} object types:")
    for obj_type, files in yaml_files.items():
        logger.info(f"  {obj_type}: {len(files)} files")
    
    # For complete GitOps management, we need to process ALL available object types
    # not just those with YAML files, so we can delete orphaned objects
    all_object_types = set(importers.keys())
    yaml_object_types = set(yaml_files.keys())
    missing_object_types = all_object_types - yaml_object_types
    
    if missing_object_types:
        logger.info(f"Object types with no YAML files (will check for deletion): {sorted(missing_object_types)}")
        # Add empty file lists for missing object types so they get processed for deletion
        for obj_type in missing_object_types:
            yaml_files[obj_type] = []
    
    # Build dependency graph and determine import order for ALL object types
    dependencies = build_dependency_graph(importers)
    import_order = topological_sort(dependencies, set(yaml_files.keys()))
    delete_order = list(reversed(import_order))  # Reverse order for deletes
    
    logger.info(f"Import order based on dependencies: {import_order}")
    logger.info(f"Delete order (reverse dependencies): {delete_order}")
    
    overall_results = {
        'total_created': 0,
        'total_updated': 0,
        'total_deleted': 0,
        'total_errors': 0,
        'results': {}
    }
    
    # Thread-safe lock for updating overall results  
    results_lock = threading.Lock()
    
    # Store objects to delete for each type (collected during create/update phase)
    objects_to_delete = {}
    
    def process_creates_updates(object_type: str, file_list: List[str]) -> tuple:
        """Process creates and updates for a single object type."""
        try:
            logger.info(f"Processing creates/updates for {importers[object_type].display_name} ({object_type})...")
            
            # Load YAML objects in batches for better memory efficiency
            yaml_objects = load_yaml_objects_optimized(file_list)
            logger.info(f"Loaded {len(yaml_objects)} objects from YAML files")
            
            if dry_run:
                logger.info(f"DRY RUN: Would process {len(yaml_objects)} {object_type} objects")
                results = {
                    'created_count': 0,
                    'updated_count': 0,
                    'deleted_count': 0,
                    'error_count': 0,
                    'errors': [],
                    'warnings': [],
                    'objects_to_delete': set()
                }
            else:
                # Set safe mode in environment for the importer
                original_safe_mode = os.environ.get('SAFE_MODE')
                os.environ['SAFE_MODE'] = 'true' if safe_mode else 'false'
                
                try:
                    results = importers[object_type].import_objects(yaml_objects)
                finally:
                    # Restore original safe mode setting
                    if original_safe_mode is not None:
                        os.environ['SAFE_MODE'] = original_safe_mode
                    elif 'SAFE_MODE' in os.environ:
                        del os.environ['SAFE_MODE']
            
            # Log results
            if results['error_count'] > 0:
                logger.warning(f"Create/Update of {object_type} completed with {results['error_count']} errors")
                for error in results['errors']:
                    logger.error(f"  {error}")
            
            if results.get('warnings'):
                for warning in results['warnings']:
                    logger.warning(f"  {warning}")
            
            success_msg = f"Create/Update results for {importers[object_type].display_name}: "
            success_msg += f"{results['created_count']} created, {results['updated_count']} updated"
            if 'objects_to_delete' in results:
                success_msg += f", {len(results['objects_to_delete'])} marked for deletion"
            logger.info(success_msg)
            
            return object_type, results, None
            
        except Exception as e:
            logger.error(f"Failed to process creates/updates for {object_type}: {e}")
            error_results = {
                'created_count': 0,
                'updated_count': 0,
                'deleted_count': 0,
                'error_count': 1,
                'errors': [str(e)],
                'warnings': [],
                'objects_to_delete': set()
            }
            return object_type, error_results, e
    
    def process_deletes(object_type: str, to_delete: set) -> tuple:
        """Process deletes for a single object type."""
        try:
            if not to_delete:
                return object_type, {'deleted_count': 0, 'error_count': 0, 'errors': [], 'warnings': []}, None
                
            logger.info(f"Processing deletes for {importers[object_type].display_name} ({object_type})...")
            
            if dry_run:
                logger.info(f"DRY RUN: Would delete {len(to_delete)} {object_type} objects")
                results = {
                    'deleted_count': 0,
                    'error_count': 0,
                    'errors': [],
                    'warnings': []
                }
            else:
                # Set safe mode in environment for the importer
                original_safe_mode = os.environ.get('SAFE_MODE')
                os.environ['SAFE_MODE'] = 'true' if safe_mode else 'false'
                
                try:
                    results = importers[object_type].delete_objects(to_delete)
                finally:
                    # Restore original safe mode setting
                    if original_safe_mode is not None:
                        os.environ['SAFE_MODE'] = original_safe_mode
                    elif 'SAFE_MODE' in os.environ:
                        del os.environ['SAFE_MODE']
            
            # Log results
            if results['error_count'] > 0:
                logger.warning(f"Delete of {object_type} completed with {results['error_count']} errors")
                for error in results['errors']:
                    logger.error(f"  {error}")
            
            if results.get('warnings'):
                for warning in results['warnings']:
                    logger.warning(f"  {warning}")
            
            logger.info(f"Delete results for {importers[object_type].display_name}: {results['deleted_count']} deleted")
            
            return object_type, results, None
            
        except Exception as e:
            logger.error(f"Failed to process deletes for {object_type}: {e}")
            error_results = {
                'deleted_count': 0,
                'error_count': 1,
                'errors': [str(e)],
                'warnings': []
            }
            return object_type, error_results, e
    
    # PHASE 1: Process Creates and Updates (in dependency order)
    logger.info("=" * 60)
    logger.info("PHASE 1: Processing Creates and Updates (dependency order)")
    logger.info("=" * 60)
    
    processed_types = set()
    
    for object_type in import_order:
        if object_type not in yaml_files or object_type in processed_types:
            continue
        
        # Find all types at this dependency level that can be processed in parallel
        current_level_types = []
        remaining_types = [t for t in import_order if t not in processed_types and t in yaml_files]
        
        for remaining_type in remaining_types:
            type_deps = dependencies.get(remaining_type, set())
            # Check if all dependencies are already processed
            if type_deps.issubset(processed_types):
                current_level_types.append(remaining_type)
        
        if not current_level_types:
            current_level_types = [object_type]  # Fallback to single type
        
        logger.info(f"Processing dependency level with {len(current_level_types)} object types in parallel")
        
        # Process current level types in parallel (max 2 threads for import due to API constraints)
        max_workers = min(2, len(current_level_types), os.cpu_count() or 1)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit create/update tasks for current level
            future_to_type = {
                executor.submit(process_creates_updates, obj_type, yaml_files[obj_type]): obj_type
                for obj_type in current_level_types
            }
            
            # Process completed tasks
            for future in concurrent.futures.as_completed(future_to_type):
                object_type, results, error = future.result()
                
                with results_lock:
                    overall_results['results'][object_type] = results
                    overall_results['total_created'] += results['created_count']
                    overall_results['total_updated'] += results['updated_count']
                    overall_results['total_errors'] += results['error_count']
                    processed_types.add(object_type)
                    
                    # Store objects to delete for later processing
                    if 'objects_to_delete' in results:
                        objects_to_delete[object_type] = results['objects_to_delete']
    
    # PHASE 2: Process Deletes (in reverse dependency order)
    logger.info("=" * 60)
    logger.info("PHASE 2: Processing Deletes (reverse dependency order)")
    logger.info("=" * 60)
    
    for object_type in delete_order:
        if object_type not in objects_to_delete:
            continue
            
        to_delete = objects_to_delete[object_type]
        if not to_delete:
            continue
        
        # Process deletes one type at a time to respect reverse dependency order
        object_type, delete_results, error = process_deletes(object_type, to_delete)
        
        with results_lock:
            # Update results with delete counts
            if object_type in overall_results['results']:
                overall_results['results'][object_type]['deleted_count'] = delete_results['deleted_count']
                overall_results['results'][object_type]['errors'].extend(delete_results['errors'])
                overall_results['results'][object_type]['warnings'].extend(delete_results['warnings'])
                overall_results['results'][object_type]['error_count'] += delete_results['error_count']
            else:
                overall_results['results'][object_type] = delete_results
            
            overall_results['total_deleted'] += delete_results['deleted_count']
            overall_results['total_errors'] += delete_results['error_count']
    
    return overall_results


def main():
    """Main import function."""
    parser = argparse.ArgumentParser(
        description='Import YAML files to Intersight for GitOps management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--input-dir', '-i',
        default=os.getenv('FILES_DIR', './files'),
        help='Input directory containing YAML files (default: ./files or FILES_DIR env var)'
    )
    
    parser.add_argument(
        '--object-types', '-t',
        help='Comma-separated list of object types to import (default: all available)'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be imported without actually making changes'
    )
    
    parser.add_argument(
        '--safe-mode', '-s',
        action='store_true',
        help='Enable safe mode to prevent destructive operations (overrides SAFE_MODE env var)'
    )
    
    parser.add_argument(
        '--no-safe-mode',
        action='store_true',
        help='Disable safe mode to allow destructive operations (overrides SAFE_MODE env var)'
    )
    
    parser.add_argument(
        '--log-level', '-l',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO or LOG_LEVEL env var)'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed progress information'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Validation mode: check YAML files without applying changes'
    )
    
    parser.add_argument(
        '--diff',
        action='store_true',
        help='Show differences between YAML files and current Intersight state'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    # Use verbose mode to lower log level for more detailed output
    effective_log_level = args.log_level
    if args.verbose and not args.log_level:
        effective_log_level = 'DEBUG' if args.debug else 'INFO'
    
    setup_logging(effective_log_level, args.debug)
    logger = logging.getLogger(__name__)
    
    if args.verbose:
        logger.info("Verbose mode enabled - showing detailed progress information")
    
    try:
        logger.info("Starting Intersight GitOps import...")
        
        # Parse object types if specified
        object_types = None
        if args.object_types:
            object_types = [t.strip() for t in args.object_types.split(',')]
            logger.info(f"Import limited to object types: {object_types}")
        
        # Determine safe mode setting
        safe_mode = None
        if args.safe_mode:
            safe_mode = True
        elif args.no_safe_mode:
            safe_mode = False
        # Otherwise, let import_objects use the default (environment variable)
        
        # Initialize API client
        logger.info("Initializing Intersight API client...")
        api_client = IntersightAPIClient()
        
        # Get available importers
        logger.info("Loading object importers...")
        importers = get_available_importers(api_client)
        logger.info(f"Loaded {len(importers)} object importers: {list(importers.keys())}")
        
        # Validate input directory
        input_dir = os.path.abspath(args.input_dir)
        if not os.path.exists(input_dir):
            logger.error(f"Input directory does not exist: {input_dir}")
            sys.exit(1)
        
        logger.info(f"Import directory: {input_dir}")
        
        # Import objects
        results = import_objects(input_dir, importers, object_types, args.dry_run, safe_mode, api_client, 
                               args.validate_only, args.diff, args.verbose)
        
        # Print summary
        logger.info("Import completed!")
        logger.info(f"Total objects created: {results['total_created']}")
        logger.info(f"Total objects updated: {results['total_updated']}")
        logger.info(f"Total objects deleted: {results['total_deleted']}")
        logger.info(f"Total errors: {results['total_errors']}")
        
        if args.dry_run:
            logger.info("DRY RUN: No changes were actually made")
        
        # Print per-type results
        for object_type, type_results in results['results'].items():
            logger.info(f"  {object_type}: {type_results['created_count']} created, "
                       f"{type_results['updated_count']} updated, {type_results['deleted_count']} deleted, "
                       f"{type_results['error_count']} errors")
        
        # Exit with error code if there were failures
        sys.exit(1 if results['total_errors'] > 0 else 0)
        
    except KeyboardInterrupt:
        logger.info("Import interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Import failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # Clean up API client
        try:
            api_client.close()
        except:
            pass


if __name__ == '__main__':
    main()