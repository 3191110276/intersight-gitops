#!/usr/bin/env python3
"""
Intersight GitOps Documentation Generator.

This script generates comprehensive documentation for all supported
Intersight object types, including field definitions, examples,
and usage instructions.

Usage:
    python documentation.py [--output-file OUTPUT_FILE] [--format FORMAT]

Environment Variables:
    LOG_LEVEL: Logging level (default: INFO)
    DEBUG: Enable debug mode (default: false)
"""

import os
import sys
import argparse
import logging
from datetime import datetime
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
from objects.wwpn_pool import WwpnPool
from objects.wwnn_pool import WwnnPool

# Import all template types
from objects.vnic_template import VnicTemplate
from objects.vhba_template import VhbaTemplate
from objects.server_template import ServerTemplate
from objects.chassis_template import ChassisTemplate
from objects.domain_template import DomainTemplate

# Import other types
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




def get_available_documenters() -> Dict[str, Any]:
    """
    Get available object documenters.
    
    Returns:
        Dictionary mapping object types to their documenter instances
    """
    # For documentation, we don't need API client connection
    documenters = {}
    
    # Initialize Organization documenter
    org_documenter = Organization()
    documenters[org_documenter.object_type] = org_documenter
    
    # Initialize all Policy documenters
    policy_classes = [
        BiosPolicy, BootPolicy, MemoryPolicy,
        AccessPolicy, AdapterConfigPolicy, CertificatePolicy, DeviceConnectorPolicy,
        DriveSecurityPolicy, EthernetAdapterPolicy, EthernetNetworkControlPolicy,
        EthernetNetworkGroupPolicy, EthernetQosPolicy, FcZonePolicy, FibreChannelAdapterPolicy,
        FibreChannelNetworkPolicy, FirmwarePolicy, FlowControlPolicy, IpmiPolicy, 
        IscsiAdapterPolicy, IscsiBootPolicy, IscsiStaticTargetPolicy, KvmPolicy,
        LanConnectivityPolicy, LdapPolicy, LinkAggregationPolicy, LinkControlPolicy,
        LocalUserPolicy, MacsecPolicy, MulticastPolicy, NetworkPolicy, NtpPolicy, 
        PersistentMemoryPolicy, PortPolicy, PowerPolicy, SanConnectivityPolicy,
        ScrubPolicy, SdCardPolicy, ServerPoolQualificationPolicy, SmtpPolicy, SnmpPolicy,
        SolPolicy, SshPolicy, StoragePolicy, SwitchControlPolicy, SyslogPolicy,
        SystemQosPolicy, ThermalPolicy, VlanPolicy, VmediaPolicy, VsanPolicy
    ]
    
    for policy_class in policy_classes:
        documenter = policy_class()
        documenters[documenter.object_type] = documenter
    
    # Initialize all Profile documenters
    profile_classes = [ChassisProfile, DomainProfile, ServerProfile]
    for profile_class in profile_classes:
        documenter = profile_class()
        documenters[documenter.object_type] = documenter
    
    # Initialize all Pool documenters
    pool_classes = [FcPool, IpPool, IqnPool, MacPool, ResourcePool, UuidPool, WwpnPool, WwnnPool]
    for pool_class in pool_classes:
        documenter = pool_class()
        documenters[documenter.object_type] = documenter
    
    # Initialize all Template documenters
    # TODO: Template classes need to implement abstract methods (export, import_objects, document)
    # template_classes = [VnicTemplate, VhbaTemplate, ServerTemplate, ChassisTemplate, DomainTemplate]
    # for template_class in template_classes:
    #     documenter = template_class()
    #     documenters[documenter.object_type] = documenter
    
    # Initialize other documenters
    # TODO: EmailNotifications class needs to implement abstract methods (export, import_objects)
    # other_classes = [EmailNotifications]
    # for other_class in other_classes:
    #     documenter = other_class()
    #     documenters[documenter.object_type] = documenter
    
    return documenters


def generate_markdown_documentation(documenters: Dict[str, Any]) -> str:
    """
    Generate comprehensive markdown documentation.
    
    Args:
        documenters: Dictionary of available documenters
        
    Returns:
        Markdown documentation as string
    """
    logger = logging.getLogger(__name__)
    
    doc_lines = []
    
    # Header
    doc_lines.extend([
        "# Intersight GitOps Tool - Object Reference",
        "",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This document provides comprehensive reference information for all Intersight object types",
        "supported by the GitOps tool. Each object type includes field definitions, constraints,",
        "examples, and usage instructions.",
        "",
        "## Table of Contents",
        ""
    ])
    
    # Generate table of contents
    for object_type, documenter in sorted(documenters.items()):
        anchor = documenter.display_name.lower().replace(' ', '-')
        doc_lines.append(f"- [{documenter.display_name}](#{anchor})")
    
    doc_lines.extend([
        "",
        "## General Information",
        "",
        "### Organization References",
        "",
        "Objects that belong to an organization reference it using a simple name format:",
        "",
        "```yaml",
        "ObjectType: policies/bios",
        "Name: my-policy",
        "Organization: default",
        "```",
        "",
        "## Object Types",
        ""
    ])
    
    # Generate documentation for each object type
    for object_type, documenter in sorted(documenters.items()):
        try:
            logger.info(f"Generating documentation for {documenter.display_name}...")
            
            # Generate documentation
            doc_info = documenter.document()
            
            if 'error' in doc_info:
                logger.error(f"Failed to document {object_type}: {doc_info['error']}")
                continue
            
            # Object type header
            doc_lines.extend([
                f"### {doc_info['display_name']}",
                "",
                f"**Object Type:** `{doc_info['object_type']}`",
                f"**Folder Path:** `{doc_info['folder_path']}/`",
                ""
            ])
            
            # Description
            if doc_info.get('description'):
                doc_lines.extend([
                    "**Description:**",
                    "",
                    doc_info['description'],
                    ""
                ])
            
            # Dependencies
            if doc_info.get('dependencies'):
                doc_lines.extend([
                    "**Dependencies:**",
                    ""
                ])
                for dep in doc_info['dependencies']:
                    doc_lines.append(f"- `{dep}`")
                doc_lines.append("")
            
            # Fields
            fields = doc_info.get('fields', {})
            if fields:
                doc_lines.extend([
                    "**Fields:**",
                    "",
                    "| Field | Type | Required | Description | Constraints |",
                    "|-------|------|----------|-------------|-------------|"
                ])
                
                # Create custom field order with ObjectType and Name first
                field_order = []
                remaining_fields = []
                
                for field_name in fields.keys():
                    if field_name == 'ObjectType':
                        field_order.insert(0, field_name)  # ObjectType first
                    elif field_name == 'Name':
                        if 'ObjectType' in field_order:
                            field_order.insert(1, field_name)  # Name second
                        else:
                            field_order.insert(0, field_name)  # Name first if no ObjectType
                    else:
                        remaining_fields.append(field_name)
                
                # Add remaining fields in alphabetical order
                field_order.extend(sorted(remaining_fields))
                
                for field_name in field_order:
                    field_info = fields[field_name]
                    field_type = field_info.get('type', 'unknown')
                    
                    # Fix Organization field type to match current implementation
                    if field_name == 'Organization' and field_type == 'reference':
                        field_type = 'string'
                        field_info = field_info.copy()
                        field_info['description'] = 'Name of the organization'
                    
                    required = 'Yes' if field_info.get('required', False) else 'No'
                    description = field_info.get('description', 'No description').replace('|', '\\|')
                    
                    # Format constraints
                    constraints = field_info.get('constraints', {})
                    constraint_parts = []
                    
                    if 'pattern' in constraints:
                        constraint_parts.append(f"Pattern: `{constraints['pattern']}`")
                    if 'min_length' in constraints:
                        constraint_parts.append(f"Min length: {constraints['min_length']}")
                    if 'max_length' in constraints:
                        constraint_parts.append(f"Max length: {constraints['max_length']}")
                    if 'allowed_values' in constraints:
                        values = ', '.join(f"`{v}`" for v in constraints['allowed_values'])
                        constraint_parts.append(f"Values: {values}")
                    
                    # Add user-friendly ObjectType format as constraint for ObjectType field
                    if field_name == 'ObjectType':
                        # Get user-friendly format from documenter
                        user_friendly_type = doc_info.get('example', {}).get('ObjectType', '')
                        if user_friendly_type:
                            constraint_parts.append(f"Format: `{user_friendly_type}`")
                    
                    constraint_text = '<br>'.join(constraint_parts) if constraint_parts else '-'
                    
                    doc_lines.append(f"| {field_name} | {field_type} | {required} | {description} | {constraint_text} |")
                
                doc_lines.append("")
            
            # Example
            example = doc_info.get('example', {})
            if example:
                doc_lines.extend([
                    "**Example:**",
                    "",
                    "```yaml"
                ])
                
                # Format the example as YAML
                import yaml
                example_yaml = yaml.dump(example, default_flow_style=False, sort_keys=False, indent=2)
                doc_lines.extend(example_yaml.strip().split('\n'))
                
                doc_lines.extend([
                    "```",
                    ""
                ])
            
            doc_lines.append("---")
            doc_lines.append("")
            
        except Exception as e:
            logger.error(f"Failed to generate documentation for {object_type}: {e}")
            doc_lines.extend([
                f"### {object_type}",
                "",
                f"**Error:** Failed to generate documentation - {e}",
                "",
                "---",
                ""
            ])
    
    # Footer
    doc_lines.extend([
        "## Usage Examples",
        "",
        "### Export Objects",
        "",
        "Export all supported object types:",
        "```bash",
        "python export.py",
        "```",
        "",
        "Export specific object types:",
        "```bash",
        "python export.py --object-types organization.Organization,bios.Policy",
        "```",
        "",
        "### Import Objects",
        "",
        "Import all YAML files:",
        "```bash",
        "python import.py",
        "```",
        "",
        "Import in safe mode (prevents deletions):",
        "```bash",
        "python import.py --safe-mode",
        "```",
        "",
        "Dry run to see what would be changed:",
        "```bash",
        "python import.py --dry-run",
        "```",
        "",
        "### Environment Configuration",
        "",
        "Create a `.env` file with your Intersight credentials:",
        "",
        "```bash",
        "# Copy the example configuration",
        "cp .env.example .env",
        "",
        "# Edit with your credentials",
        "vi .env",
        "```",
        "",
        "Required environment variables:",
        "",
        "- `API_KEY`: Your Intersight API Key ID",
        "- `API_SECRET`: Your Intersight API Secret Key (file path or key content)",
        "- `IS_ENDPOINT`: Intersight API endpoint (default: https://intersight.com)",
        "",
        "Optional environment variables:",
        "",
        "- `FILES_DIR`: Directory for YAML files (default: ./files)",
        "- `SAFE_MODE`: Prevent destructive operations (default: true)",
        "- `LOG_LEVEL`: Logging level (default: INFO)",
        "- `DEBUG`: Enable debug logging (default: false)",
        "",
        "## Troubleshooting",
        "",
        "### Common Issues",
        "",
        "**Authentication Errors:**",
        "- Verify API_KEY and API_SECRET are correct",
        "- Ensure the private key file is readable",
        "- Check that the API key has sufficient permissions",
        "",
        "**Validation Errors:**",
        "- Check YAML syntax with `yamllint`",
        "- Ensure required fields are present",
        "- Verify field values match constraints",
        "",
        "**Import Failures:**",
        "- Check object dependencies are satisfied",
        "- Verify referenced objects exist",
        "- Review logs for detailed error messages",
        "",
        "### Debug Mode",
        "",
        "Enable debug logging for detailed troubleshooting:",
        "",
        "```bash",
        "python export.py --debug",
        "python import.py --debug",
        "```",
        "",
        "---",
        "",
        f"*Documentation generated by Intersight GitOps Tool on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    ])
    
    return '\n'.join(doc_lines)


def generate_json_documentation(documenters: Dict[str, Any]) -> str:
    """
    Generate documentation in JSON format.
    
    Args:
        documenters: Dictionary of available documenters
        
    Returns:
        JSON documentation as string
    """
    import json
    
    logger = logging.getLogger(__name__)
    
    doc_data = {
        'generated_at': datetime.now().isoformat(),
        'version': '1.0.0',
        'object_types': {}
    }
    
    for object_type, documenter in documenters.items():
        try:
            logger.info(f"Generating JSON documentation for {documenter.display_name}...")
            
            # Generate documentation
            doc_info = documenter.document()
            
            if 'error' not in doc_info:
                doc_data['object_types'][object_type] = doc_info
            else:
                logger.error(f"Failed to document {object_type}: {doc_info['error']}")
                
        except Exception as e:
            logger.error(f"Failed to generate JSON documentation for {object_type}: {e}")
    
    return json.dumps(doc_data, indent=2, sort_keys=True)


def main():
    """Main documentation function."""
    parser = argparse.ArgumentParser(
        description='Generate documentation for Intersight GitOps object types',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--output-file', '-o',
        default='OBJECT_REFERENCE.md',
        help='Output file for generated documentation (default: OBJECT_REFERENCE.md)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
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
        logger.info("Starting Intersight GitOps documentation generation...")
        
        # Get available documenters
        logger.info("Loading object documenters...")
        documenters = get_available_documenters()
        logger.info(f"Loaded {len(documenters)} object documenters: {list(documenters.keys())}")
        
        # Generate documentation
        logger.info(f"Generating {args.format} documentation...")
        
        if args.format == 'json':
            documentation = generate_json_documentation(documenters)
        else:
            documentation = generate_markdown_documentation(documenters)
        
        # Write to file
        output_file = os.path.abspath(args.output_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(documentation)
        
        logger.info(f"Documentation generated successfully: {output_file}")
        logger.info(f"Documentation contains {len(documenters)} object types")
        
    except KeyboardInterrupt:
        logger.info("Documentation generation interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Documentation generation failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()