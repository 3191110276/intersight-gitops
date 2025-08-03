#!/usr/bin/env python3
"""
Intersight GitOps Export Script.

This script exports Intersight objects to YAML files for GitOps management.
It connects to Intersight, queries various object types, filters out system
defaults, and saves user-defined objects as YAML files.

Usage:
    python export.py [--output-dir OUTPUT_DIR] [--object-types TYPE1,TYPE2] [--dry-run]

Environment Variables:
    API_KEY: Intersight API Key ID
    API_SECRET: Intersight API Secret Key (file path or key content)
    IS_ENDPOINT: Intersight API endpoint (default: https://intersight.com)
    FILES_DIR: Output directory for exported files (default: ./files)
    LOG_LEVEL: Logging level (default: INFO)
    DEBUG: Enable debug mode (default: false)
"""

import os
import sys
import argparse
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, List

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
from core.error_handler import get_global_error_handler, handle_errors
from core.exceptions import IntersightGitOpsError, CriticalError
from utils.openapi_parser import OpenAPIParser
from core.object_registry import get_global_registry, register_object_type, get_dependency_order
from objects.organization import Organization
from objects.bios_policy import BiosPolicy
from objects.boot_policy import BootPolicy
from objects.memory_policy import MemoryPolicy

# Import all policy types
from objects.access_policy import AccessPolicy
from objects.adapter_config_policy import AdapterConfigPolicy
from objects.certificate_policy import CertificatePolicy
from objects.device_connector_policy import DeviceConnectorPolicy
from objects.drive_security_policy import DriveSecurityPolicy
from objects.ethernet_adapter_policy import EthernetAdapterPolicy
from objects.ethernet_network_control_policy import EthernetNetworkControlPolicy
from objects.ethernet_network_group_policy import EthernetNetworkGroupPolicy
from objects.ethernet_qos_policy import EthernetQosPolicy
from objects.fc_zone_policy import FcZonePolicy
from objects.fibre_channel_adapter_policy import FibreChannelAdapterPolicy
from objects.fibre_channel_network_policy import FibreChannelNetworkPolicy
from objects.firmware_policy import FirmwarePolicy
from objects.flow_control_policy import FlowControlPolicy
from objects.ipmi_policy import IpmiPolicy
from objects.iscsi_adapter_policy import IscsiAdapterPolicy
from objects.iscsi_boot_policy import IscsiBootPolicy
from objects.iscsi_static_target_policy import IscsiStaticTargetPolicy
from objects.kvm_policy import KvmPolicy
from objects.lan_connectivity_policy import LanConnectivityPolicy
from objects.ldap_policy import LdapPolicy
from objects.link_aggregation_policy import LinkAggregationPolicy
from objects.link_control_policy import LinkControlPolicy
from objects.local_user_policy import LocalUserPolicy
from objects.macsec_policy import MacsecPolicy
from objects.multicast_policy import MulticastPolicy
from objects.network_policy import NetworkPolicy
from objects.ntp_policy import NtpPolicy
from objects.persistent_memory_policy import PersistentMemoryPolicy
from objects.port_policy import PortPolicy
from objects.power_policy import PowerPolicy
from objects.san_connectivity_policy import SanConnectivityPolicy
from objects.scrub_policy import ScrubPolicy
from objects.sdcard_policy import SdCardPolicy
from objects.server_pool_qualification_policy import ServerPoolQualificationPolicy
from objects.smtp_policy import SmtpPolicy
from objects.snmp_policy import SnmpPolicy
from objects.sol_policy import SolPolicy
from objects.ssh_policy import SshPolicy
from objects.storage_policy import StoragePolicy
from objects.switch_control_policy import SwitchControlPolicy
from objects.syslog_policy import SyslogPolicy
from objects.system_qos_policy import SystemQosPolicy
from objects.thermal_policy import ThermalPolicy
from objects.vlan_policy import VlanPolicy
from objects.vmedia_policy import VmediaPolicy
from objects.vsan_policy import VsanPolicy

# Import all profile types
from objects.chassis_profile import ChassisProfile
from objects.domain_profile import DomainProfile
from objects.server_profile import ServerProfile

# Import all pool types
from objects.fc_pool import FcPool
from objects.ip_pool import IpPool
from objects.iqn_pool import IqnPool
from objects.mac_pool import MacPool
from objects.resource_pool import ResourcePool
from objects.uuid_pool import UuidPool
from objects.wwnn_pool import WwnnPool
from objects.wwpn_pool import WwpnPool

# Import all template types  
from objects.chassis_template import ChassisTemplate
from objects.domain_template import DomainTemplate
from objects.server_template import ServerTemplate
from objects.vhba_template import VhbaTemplate
from objects.vnic_template import VnicTemplate

# Import email notifications
from objects.email_notifications import EmailNotifications


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


def get_full_object_type(simplified_type: str) -> str:
    """
    Convert simplified object type to full object type.
    
    Args:
        simplified_type: Simplified object type (e.g., "power" or "policies/power")
        
    Returns:
        Full object type (e.g., "power.Policy")
    """
    # Extract base type from folder/type format if present
    if '/' in simplified_type:
        _, base_type = simplified_type.split('/', 1)
    else:
        base_type = simplified_type
    
    type_mapping = {
        # Organizations
        'organization': 'organization.Organization',
        
        # Policies
        'bios': 'bios.Policy',
        'boot': 'boot.PrecisionPolicy',
        'memory': 'memory.Policy',
        'access': 'access.Policy',
        'certificate': 'certificatemanagement.Policy',
        'deviceconnector': 'deviceconnector.Policy',
        'firmware': 'firmware.Policy',
        'ipmi': 'ipmioverlan.Policy',
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
        
        # Profiles
        'server': 'server.Profile',
        'chassis': 'chassis.Profile',
        
        # Pools
        'fcpool': 'fcpool.Pool',
        'ippool': 'ippool.Pool',
        'iqnpool': 'iqnpool.Pool',
        'macpool': 'macpool.Pool',
        'resourcepool': 'resourcepool.Pool',
        'uuidpool': 'uuidpool.Pool'
    }
    
    return type_mapping.get(base_type, simplified_type)


def load_openapi_schema() -> OpenAPIParser:
    """Load and parse the OpenAPI schema."""
    openapi_file = os.path.join(os.path.dirname(__file__), 'openapi.json')
    if not os.path.exists(openapi_file):
        raise FileNotFoundError(f"OpenAPI schema file not found: {openapi_file}")
    
    return OpenAPIParser(openapi_file)


def setup_object_registry(api_client: IntersightAPIClient, openapi_parser: OpenAPIParser):
    """
    Set up the object registry with all available object types.
    
    Args:
        api_client: The Intersight API client
        openapi_parser: The OpenAPI schema parser
    """
    # Clear the global registry
    registry = get_global_registry()
    registry.clear()
    
    # Register Organization
    register_object_type(Organization)
    
    # Register all Policy types
    policy_classes = [
        BiosPolicy, BootPolicy, MemoryPolicy,
        AccessPolicy, AdapterConfigPolicy, CertificatePolicy, DeviceConnectorPolicy,
        DriveSecurityPolicy, EthernetAdapterPolicy, EthernetNetworkControlPolicy,
        EthernetNetworkGroupPolicy, EthernetQosPolicy, FcZonePolicy,
        FibreChannelAdapterPolicy, FibreChannelNetworkPolicy, FirmwarePolicy,
        FlowControlPolicy, IpmiPolicy, IscsiAdapterPolicy, IscsiBootPolicy,
        IscsiStaticTargetPolicy, KvmPolicy, LanConnectivityPolicy, LdapPolicy,
        LinkAggregationPolicy, LinkControlPolicy, LocalUserPolicy, MacsecPolicy,
        MulticastPolicy, NetworkPolicy, NtpPolicy, PersistentMemoryPolicy,
        PortPolicy, PowerPolicy, SanConnectivityPolicy, ScrubPolicy,
        SdCardPolicy, ServerPoolQualificationPolicy, SmtpPolicy, SnmpPolicy, 
        SolPolicy, SshPolicy, StoragePolicy, SwitchControlPolicy, SyslogPolicy,
        SystemQosPolicy, ThermalPolicy, VlanPolicy, VmediaPolicy, VsanPolicy
    ]
    
    for policy_class in policy_classes:
        register_object_type(policy_class)
    
    # Register Profile types
    profile_classes = [ChassisProfile, DomainProfile, ServerProfile]
    
    for profile_class in profile_classes:
        register_object_type(profile_class)
    
    # Register Pool types
    pool_classes = [FcPool, IpPool, IqnPool, MacPool, ResourcePool, UuidPool, WwnnPool, WwpnPool]
    
    for pool_class in pool_classes:
        register_object_type(pool_class)
    
    # Register Template types (skip abstract template classes for now)
    # template_classes = [ChassisTemplate, DomainTemplate, ServerTemplate, VhbaTemplate, VnicTemplate]
    # 
    # for template_class in template_classes:
    #     register_object_type(template_class)
        
    # Register Email Notifications (skip abstract class for now)
    # register_object_type(EmailNotifications)
    
    # Create instances with API client and schema
    for object_type_id in registry.get_registered_types().keys():
        registry.create_instance(
            object_type_id,
            api_client=api_client, 
            openapi_schema=openapi_parser.schema
        )


def get_available_exporters() -> Dict[str, Any]:
    """
    Get available object exporters from the registry.
    
    Returns:
        Dictionary mapping object types to their exporter instances
    """
    registry = get_global_registry()
    exporters = {}
    
    for object_type_id, object_type_class in registry.get_registered_types().items():
        instance = registry.get_instance(object_type_id)
        if instance:
            exporters[object_type_id] = instance
    
    return exporters


def clean_export_directory(output_dir: str, dry_run: bool = False) -> None:
    """
    Clean the export directory before exporting to ensure a fresh state.
    
    This removes all existing files and subdirectories in the output directory
    to prevent leftover files from previous exports.
    
    Args:
        output_dir: Directory to clean
        dry_run: If True, log what would be cleaned but don't actually delete
    """
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(output_dir):
        logger.info(f"Export directory doesn't exist, will be created: {output_dir}")
        return
    
    if dry_run:
        logger.info(f"DRY RUN: Would clean export directory: {output_dir}")
        # List what would be deleted
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                logger.info(f"DRY RUN: Would delete file: {file_path}")
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                logger.info(f"DRY RUN: Would delete directory: {dir_path}")
        return
    
    logger.info(f"Cleaning export directory: {output_dir}")
    
    try:
        # Remove all contents of the directory but keep the directory itself
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logger.debug(f"Removed directory: {item_path}")
            else:
                os.remove(item_path)
                logger.debug(f"Removed file: {item_path}")
        
        logger.info(f"Successfully cleaned export directory: {output_dir}")
        
    except Exception as e:
        logger.error(f"Failed to clean export directory {output_dir}: {e}")
        raise


def export_objects(output_dir: str, exporters: Dict[str, Any], object_types: List[str] = None, dry_run: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """
    Export objects using the specified exporters with parallel processing support.
    
    Args:
        output_dir: Directory to save exported files
        exporters: Dictionary of available exporters
        object_types: List of specific object types to export (None for all)
        dry_run: If True, don't actually save files
        
    Returns:
        Dictionary with overall export results
    """
    import concurrent.futures
    import threading
    from functools import partial
    
    logger = logging.getLogger(__name__)
    
    # Clean the export directory before starting export
    clean_export_directory(output_dir, dry_run)
    
    # Filter exporters if specific object types requested
    if object_types:
        # Convert simplified object types to full object types using the mapping
        full_object_types = []
        for obj_type in object_types:
            full_type = get_full_object_type(obj_type)
            full_object_types.append(full_type)
            logger.debug(f"Mapped object type '{obj_type}' to '{full_type}'")
        
        filtered_exporters = {k: v for k, v in exporters.items() if k in full_object_types}
        if not filtered_exporters:
            logger.warning(f"No exporters found for requested object types: {object_types} (mapped to: {full_object_types})")
            logger.warning(f"Available exporters: {list(exporters.keys())}")
            return {'total_objects': 0, 'total_errors': 0, 'results': {}}
    else:
        filtered_exporters = exporters
    
    logger.info(f"Starting parallel export for {len(filtered_exporters)} object types to {output_dir}")
    
    overall_results = {
        'total_objects': 0,
        'total_errors': 0,
        'results': {}
    }
    
    # Thread-safe lock for updating overall results
    results_lock = threading.Lock()
    
    def export_object_type(object_type: str, exporter: Any) -> tuple:
        """Export a single object type and return results."""
        try:
            if verbose:
                logger.info(f"Starting export of {exporter.display_name} ({object_type})...")
            else:
                logger.info(f"Exporting {exporter.display_name} ({object_type})...")
            
            if dry_run:
                logger.info(f"DRY RUN: Would export {object_type}")
                results = {
                    'success_count': 0,
                    'error_count': 0,
                    'errors': [],
                    'exported_files': []
                }
            else:
                results = exporter.export(output_dir)
            
            if results['error_count'] > 0:
                logger.warning(f"Export of {object_type} completed with {results['error_count']} errors")
                for error in results['errors']:
                    logger.error(f"  {error}")
            else:
                success_msg = f"Successfully exported {results['success_count']} {exporter.display_name} objects"
                if verbose and results.get('exported_files'):
                    success_msg += f" to {len(results['exported_files'])} files"
                logger.info(success_msg)
                
                if verbose and results.get('exported_files'):
                    for file_path in results['exported_files'][:5]:  # Show first 5 files
                        logger.debug(f"  Created: {file_path}")
                    if len(results['exported_files']) > 5:
                        logger.debug(f"  ... and {len(results['exported_files']) - 5} more files")
                
            return object_type, results, None
            
        except Exception as e:
            logger.error(f"Failed to export {object_type}: {e}")
            error_results = {
                'success_count': 0,
                'error_count': 1,
                'errors': [str(e)],
                'exported_files': []
            }
            return object_type, error_results, e
    
    # Determine optimal number of threads (max 4, or number of exporters if fewer)
    max_workers = min(4, len(filtered_exporters), os.cpu_count() or 1)
    logger.info(f"Using {max_workers} threads for parallel export")
    
    # Execute exports in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all export tasks
        future_to_type = {
            executor.submit(export_object_type, object_type, exporter): object_type
            for object_type, exporter in filtered_exporters.items()
        }
        
        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_type):
            object_type, results, error = future.result()
            
            with results_lock:
                overall_results['results'][object_type] = results
                overall_results['total_objects'] += results['success_count']
                overall_results['total_errors'] += results['error_count']
    
    return overall_results


def main():
    """Main export function."""
    parser = argparse.ArgumentParser(
        description='Export Intersight objects to YAML files for GitOps management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default=os.getenv('FILES_DIR', './files'),
        help='Output directory for exported YAML files (default: ./files or FILES_DIR env var)'
    )
    
    parser.add_argument(
        '--object-types', '-t',
        help='Comma-separated list of object types to export (default: all available)'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be exported without actually saving files'
    )
    
    parser.add_argument(
        '--streaming',
        action='store_true',
        help='Use streaming export for large datasets (more memory efficient)'
    )
    
    parser.add_argument(
        '--progress',
        action='store_true',
        help='Show progress information during export'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=1000,
        help='Batch size for processing objects (default: 1000)'
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
        logger.info("Starting Intersight GitOps export...")
        
        # Parse object types if specified
        object_types = None
        if args.object_types:
            object_types = [t.strip() for t in args.object_types.split(',')]
            logger.info(f"Export limited to object types: {object_types}")
        
        # Load OpenAPI schema
        logger.info("Loading OpenAPI schema...")
        openapi_parser = load_openapi_schema()
        
        # Initialize API client
        logger.info("Initializing Intersight API client...")
        api_client = IntersightAPIClient()
        
        # Set up object registry
        logger.info("Setting up object registry...")
        setup_object_registry(api_client, openapi_parser)
        
        # Get available exporters
        logger.info("Loading object exporters...")
        exporters = get_available_exporters()
        logger.info(f"Loaded {len(exporters)} object exporters: {list(exporters.keys())}")
        
        # Create output directory
        output_dir = os.path.abspath(args.output_dir)
        if not args.dry_run:
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Export directory: {output_dir}")
        
        # Export objects
        results = export_objects(output_dir, exporters, object_types, args.dry_run, args.verbose)
        
        # Print summary
        logger.info("Export completed!")
        logger.info(f"Total objects exported: {results['total_objects']}")
        logger.info(f"Total errors: {results['total_errors']}")
        
        if args.dry_run:
            logger.info("DRY RUN: No files were actually created")
        
        # Print per-type results
        for object_type, type_results in results['results'].items():
            if type_results['success_count'] > 0 or type_results['error_count'] > 0:
                logger.info(f"  {object_type}: {type_results['success_count']} exported, {type_results['error_count']} errors")
        
        # Print error summary if there were errors
        error_handler = get_global_error_handler()
        error_summary = error_handler.get_error_summary()
        if error_summary['total_errors'] > 0:
            logger.error(f"Error summary: {error_summary['total_errors']} total errors")
            for error_code, count in error_summary['error_counts'].items():
                logger.error(f"  {error_code}: {count} occurrences")
            
            # Export detailed error report if debug mode
            if args.debug:
                error_report_path = os.path.join(output_dir, 'export_error_report.json')
                error_handler.export_error_report(error_report_path)
        
        # Exit with error code if there were failures
        sys.exit(1 if results['total_errors'] > 0 else 0)
        
    except KeyboardInterrupt:
        logger.info("Export interrupted by user")
        sys.exit(130)
    except IntersightGitOpsError as e:
        logger.error(f"Export failed: {e.message}")
        logger.error(f"Error code: {e.error_code}")
        if e.context:
            logger.error(f"Context: {e.context}")
        
        if args.debug:
            import traceback
            traceback.print_exc()
        
        # Handle critical errors
        if e.error_code == 'CRITICAL_ERROR':
            suggestions = e.context.get('recovery_suggestions', [])
            if suggestions:
                logger.error("Recovery suggestions:")
                for suggestion in suggestions:
                    logger.error(f"  - {suggestion}")
        
        sys.exit(1)
    except Exception as e:
        # Handle unexpected errors
        error_handler = get_global_error_handler()
        error_handler.handle_error(e, {
            'script': 'export.py',
            'operation': 'main_export'
        })
        
        logger.error(f"Unexpected export failure: {e}")
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