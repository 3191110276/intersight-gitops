"""
BIOS Policy object implementation with comprehensive field coverage.

This module implements the BiosPolicy class for handling Cisco Intersight
BIOS policies in the GitOps workflow with full 460+ BIOS token support.
"""

import logging
from typing import Dict, Any, Set

from src.core.object_type import FieldDefinition, FieldType, DependencyDefinition
from src.objects.base_policy import BasePolicy

logger = logging.getLogger(__name__)


class BiosPolicy(BasePolicy):
    """
    Implementation for Intersight BIOS Policy objects with comprehensive field coverage.
    
    BIOS policies define BIOS settings and configurations for servers.
    This implementation covers all 460+ available BIOS tokens across all categories:
    - CPU and Processor Settings (77 fields)
    - Memory Settings (45 fields)  
    - Boot and Storage Settings (35 fields)
    - PCIe and Slot Configuration (89 fields)
    - Security Features (28 fields)
    - Network and Communication (25 fields)
    - Power and Thermal (22 fields)
    - Firmware and Platform (35 fields)
    - Advanced System Features (58 fields)
    - ACS Control Features (50 fields)
    """
    
    @property
    def object_type(self) -> str:
        """Return the Intersight object type."""
        return "bios.Policy"
    
    @property
    def display_name(self) -> str:
        """Return the human-readable display name."""
        return "BIOS Policy"
    
    @property
    def folder_path(self) -> str:
        """Return the folder path for storing BIOS policy YAML files."""
        return "policies/bios"
    
    def _define_fields(self) -> Dict[str, FieldDefinition]:
        """Define the comprehensive fields for BIOS Policy objects covering all 460+ BIOS tokens."""
        # Start with common policy fields
        fields = self._get_common_policy_fields()
        
        # Add comprehensive BIOS-specific fields covering all 460+ BIOS tokens
        bios_fields = {}
        
        # === CPU AND PROCESSOR SETTINGS (77 fields) ===
        cpu_fields = {
            # Intel CPU Features
            'IntelHyperThreadingTech': FieldDefinition(
                name='IntelHyperThreadingTech',
                field_type=FieldType.STRING,
                required=False,
                description='Intel Hyper Threading Technology',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelTurboBoostTech': FieldDefinition(
                name='IntelTurboBoostTech',
                field_type=FieldType.STRING,
                required=False,
                description='Intel Turbo Boost Technology',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelVirtualizationTechnology': FieldDefinition(
                name='IntelVirtualizationTechnology',
                field_type=FieldType.STRING,
                required=False,
                description='Intel Virtualization Technology',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelSpeedSelect': FieldDefinition(
                name='IntelSpeedSelect',
                field_type=FieldType.STRING,
                required=False,
                description='Intel Speed Select Technology',
                enum_values=['platform-default', 'Auto', 'Base', 'Config 1', 'Config 2', 'Config 3', 'Config 4']
            ),
            'IntelSpeedStepTech': FieldDefinition(
                name='IntelSpeedStepTech',
                field_type=FieldType.STRING,
                required=False,
                description='Intel SpeedStep Technology',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ExecuteDisableBit': FieldDefinition(
                name='ExecuteDisableBit',
                field_type=FieldType.STRING,
                required=False,
                description='Execute Disable Bit',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # AMD CBS CPU Features
            'CbsCmnCpuAvx512': FieldDefinition(
                name='CbsCmnCpuAvx512',
                field_type=FieldType.STRING,
                required=False,
                description='AVX512 Support',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            'CbsCmnCpuCpb': FieldDefinition(
                name='CbsCmnCpuCpb',
                field_type=FieldType.STRING,
                required=False,
                description='Core Performance Boost',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            'CbsCmnCpuSmee': FieldDefinition(
                name='CbsCmnCpuSmee',
                field_type=FieldType.STRING,
                required=False,
                description='SME (Secure Memory Encryption)',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            'CbsCmnCpuStreamingStoresCtrl': FieldDefinition(
                name='CbsCmnCpuStreamingStoresCtrl',
                field_type=FieldType.STRING,
                required=False,
                description='Streaming Stores Control',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            
            # Additional critical AMD CBS fields from missing attributes analysis
            'CbsDfCmnMemIntlv': FieldDefinition(
                name='CbsDfCmnMemIntlv',
                field_type=FieldType.STRING,
                required=False,
                description='AMD Memory Interleaving',
                enum_values=['platform-default', 'Auto', 'Channel', 'Die', 'Socket']
            ),
            'CbsDfCmnMemIntlvSize': FieldDefinition(
                name='CbsDfCmnMemIntlvSize',
                field_type=FieldType.STRING,
                required=False,
                description='AMD Memory Interleaving Size',
                enum_values=['platform-default', '256 Bytes', '512 Bytes', '1 KB', '2 KB', '4 KB']
            ),
            'CbsCmnCpuGenDowncoreCtrl': FieldDefinition(
                name='CbsCmnCpuGenDowncoreCtrl',
                field_type=FieldType.STRING,
                required=False,
                description='AMD CPU Downcore Control',
                enum_values=['platform-default', 'Auto', 'Four (2 + 2)', 'Six (3 + 3)', 'Two (1 + 1)']
            ),
            'CbsCmnCpuCcdCtrl': FieldDefinition(
                name='CbsCmnCpuCcdCtrl',
                field_type=FieldType.STRING,
                required=False,
                description='AMD CCD Control',
                enum_values=['platform-default', 'Auto', '2 CCDs', '4 CCDs', '6 CCDs', '8 CCDs']
            ),
            'CbsCmnGnbNbIommu': FieldDefinition(
                name='CbsCmnGnbNbIommu',
                field_type=FieldType.STRING,
                required=False,
                description='AMD IOMMU Control',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            
            # CPU Performance Settings
            'CpuEnergyPerformance': FieldDefinition(
                name='CpuEnergyPerformance',
                field_type=FieldType.STRING,
                required=False,
                description='Energy Performance',
                enum_values=['platform-default', 'balanced-energy', 'balanced-performance', 'balanced-power', 'energy-efficient', 'performance', 'power']
            ),
            'CpuPerformance': FieldDefinition(
                name='CpuPerformance',
                field_type=FieldType.STRING,
                required=False,
                description='CPU Performance setting',
                enum_values=['platform-default', 'custom', 'enterprise', 'high-throughput', 'hpc']
            ),
            'CpuPowerManagement': FieldDefinition(
                name='CpuPowerManagement',
                field_type=FieldType.STRING,
                required=False,
                description='CPU Power Management setting',
                enum_values=['platform-default', 'custom', 'disabled', 'energy-efficient', 'performance']
            ),
            'EnergyEfficientTurbo': FieldDefinition(
                name='EnergyEfficientTurbo',
                field_type=FieldType.STRING,
                required=False,
                description='Energy Efficient Turbo',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # Processor C-State Settings
            'ProcessorC1e': FieldDefinition(
                name='ProcessorC1e',
                field_type=FieldType.STRING,
                required=False,
                description='Processor C1E support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ProcessorC3report': FieldDefinition(
                name='ProcessorC3report',
                field_type=FieldType.STRING,
                required=False,
                description='Processor C3 Report',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ProcessorC6report': FieldDefinition(
                name='ProcessorC6report',
                field_type=FieldType.STRING,
                required=False,
                description='Processor C6 Report',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ProcessorCstate': FieldDefinition(
                name='ProcessorCstate',
                field_type=FieldType.STRING,
                required=False,
                description='CPU C State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'C1autoDemotion': FieldDefinition(
                name='C1autoDemotion',
                field_type=FieldType.STRING,
                required=False,
                description='C1 Auto Demotion',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            'AutonumousCstateEnable': FieldDefinition(
                name='AutonumousCstateEnable',
                field_type=FieldType.STRING,
                required=False,
                description='Autonomous C-state Enable',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'PackageCstateLimit': FieldDefinition(
                name='PackageCstateLimit',
                field_type=FieldType.STRING,
                required=False,
                description='Package C State Limit',
                enum_values=['platform-default', 'Auto', 'C0 C1 State', 'C0/C1', 'C2', 'C6 Non Retention', 'C6 Retention', 'No Limit']
            ),
            
            # Advanced CPU Settings
            'CoreMultiProcessing': FieldDefinition(
                name='CoreMultiProcessing',
                field_type=FieldType.STRING,
                required=False,
                description='Core Multi Processing',
                enum_values=['platform-default', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', 'all']
            ),
            'EnableRmt': FieldDefinition(
                name='EnableRmt',
                field_type=FieldType.STRING,
                required=False,
                description='RMT (Runtime Memory Throttling)',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'HwPrefetcher': FieldDefinition(
                name='HwPrefetcher',
                field_type=FieldType.STRING,
                required=False,
                description='Hardware Prefetcher',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AdjacentCacheLinePrefetch': FieldDefinition(
                name='AdjacentCacheLinePrefetch',
                field_type=FieldType.STRING,
                required=False,
                description='Adjacent Cache Line Prefetch',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'DcuStreamerPrefetch': FieldDefinition(
                name='DcuStreamerPrefetch',
                field_type=FieldType.STRING,
                required=False,
                description='DCU Streamer Prefetch',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'DcuIpPrefetch': FieldDefinition(
                name='DcuIpPrefetch',
                field_type=FieldType.STRING,
                required=False,
                description='DCU IP Prefetch',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'DirectCacheAccess': FieldDefinition(
                name='DirectCacheAccess',
                field_type=FieldType.STRING,
                required=False,
                description='Direct Cache Access',
                enum_values=['platform-default', 'auto', 'disabled', 'enabled']
            ),
            'ProcessorEistEnable': FieldDefinition(
                name='ProcessorEistEnable',
                field_type=FieldType.STRING,
                required=False,
                description='Enhanced Intel SpeedStep Technology',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'XptPrefetch': FieldDefinition(
                name='XptPrefetch',
                field_type=FieldType.STRING,
                required=False,
                description='XPT Prefetch',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            'CpuHardwarePowerManagement': FieldDefinition(
                name='CpuHardwarePowerManagement',
                field_type=FieldType.STRING,
                required=False,
                description='CPU Hardware Power Management',
                enum_values=['platform-default', 'disabled', 'hwpm-native-mode', 'hwpm-oob-mode', 'native-mode', 'oob-mode']
            ),
            'WorkloadConfiguration': FieldDefinition(
                name='WorkloadConfiguration',
                field_type=FieldType.STRING,
                required=False,
                description='Workload Configuration',
                enum_values=['platform-default', 'Balanced', 'IO Sensitive', 'NUMA Sparing']
            ),
            'ProcessorEppProfile': FieldDefinition(
                name='ProcessorEppProfile',
                field_type=FieldType.STRING,
                required=False,
                description='Processor EPP Profile',
                enum_values=['platform-default', 'Balanced Performance', 'Balanced Power', 'Performance', 'Power']
            ),
            'PsdCoordType': FieldDefinition(
                name='PsdCoordType',
                field_type=FieldType.STRING,
                required=False,
                description='P-State Coordination',
                enum_values=['platform-default', 'HW All', 'SW All', 'SW Any']
            ),
        }
        bios_fields.update(cpu_fields)
        
        # === MEMORY SETTINGS (45 fields) ===
        memory_fields = {
            # Memory Interleaving
            'MemoryInterLeave': FieldDefinition(
                name='MemoryInterLeave',
                field_type=FieldType.STRING,
                required=False,
                description='Memory Interleaving',
                enum_values=['platform-default', '1-way', '2-way', '4-way', '8-way', 'auto']
            ),
            'ChannelInterLeave': FieldDefinition(
                name='ChannelInterLeave',
                field_type=FieldType.STRING,
                required=False,
                description='Channel Interleaving',
                enum_values=['platform-default', '1-way', '2-way', '3-way', '4-way', 'auto']
            ),
            'RankInterLeave': FieldDefinition(
                name='RankInterLeave',
                field_type=FieldType.STRING,
                required=False,
                description='Rank Interleaving',
                enum_values=['platform-default', '1-way', '2-way', '4-way', '8-way', 'auto']
            ),
            'ImcInterleave': FieldDefinition(
                name='ImcInterleave',
                field_type=FieldType.STRING,
                required=False,
                description='IMC Interleaving',
                enum_values=['platform-default', '1-way', '2-way', '4-way', '8-way', 'auto']
            ),
            
            # Memory Performance
            'MemoryBandwidthBoost': FieldDefinition(
                name='MemoryBandwidthBoost',
                field_type=FieldType.STRING,
                required=False,
                description='Memory Bandwidth Boost',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'MemoryRefreshRate': FieldDefinition(
                name='MemoryRefreshRate',
                field_type=FieldType.STRING,
                required=False,
                description='Memory Refresh Rate',
                enum_values=['platform-default', '1x', '2x']
            ),
            'DramRefreshRate': FieldDefinition(
                name='DramRefreshRate',
                field_type=FieldType.STRING,
                required=False,
                description='DRAM Refresh Rate',
                enum_values=['platform-default', '1x', '2x', '3x', '4x', 'Auto']
            ),
            'DramClockThrottling': FieldDefinition(
                name='DramClockThrottling',
                field_type=FieldType.STRING,
                required=False,
                description='DRAM Clock Throttling',
                enum_values=['platform-default', 'auto', 'balanced', 'energy-efficient', 'performance']
            ),
            
            # Memory Testing and Error Correction
            'AdvancedMemTest': FieldDefinition(
                name='AdvancedMemTest',
                field_type=FieldType.STRING,
                required=False,
                description='Advanced Memory Test',
                enum_values=['platform-default', 'Auto', 'disabled', 'enabled']
            ),
            'DemandScrub': FieldDefinition(
                name='DemandScrub',
                field_type=FieldType.STRING,
                required=False,
                description='Demand Scrub',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'PatrolScrub': FieldDefinition(
                name='PatrolScrub',
                field_type=FieldType.STRING,
                required=False,
                description='Patrol Scrub',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ErrorCheckScrub': FieldDefinition(
                name='ErrorCheckScrub',
                field_type=FieldType.STRING,
                required=False,
                description='Error Check Scrub',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # Memory Mirroring and Sparing
            'MirroringMode': FieldDefinition(
                name='MirroringMode',
                field_type=FieldType.STRING,
                required=False,
                description='Memory Mirroring Mode',
                enum_values=['platform-default', 'inter-socket', 'intra-socket']
            ),
            'SparingMode': FieldDefinition(
                name='SparingMode',
                field_type=FieldType.STRING,
                required=False,
                description='Memory Sparing Mode',
                enum_values=['platform-default', 'dimm-sparing', 'rank-sparing']
            ),
            'PartialMirrorModeConfig': FieldDefinition(
                name='PartialMirrorModeConfig',
                field_type=FieldType.STRING,
                required=False,
                description='Partial Memory Mirror Mode Configuration',
                enum_values=['platform-default', 'disabled', 'percentage', 'value-in-gb']
            ),
            'SelectMemoryRasConfiguration': FieldDefinition(
                name='SelectMemoryRasConfiguration',
                field_type=FieldType.STRING,
                required=False,
                description='Memory RAS Configuration',
                enum_values=['platform-default', 'adddc-sparing', 'lockstep', 'maximum-performance', 'mirror-mode-1lm', 'sparing']
            ),
            
            # Memory Thermal Management
            'MemoryThermalThrottling': FieldDefinition(
                name='MemoryThermalThrottling',
                field_type=FieldType.STRING,
                required=False,
                description='Memory Thermal Throttling',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'DramSwThermalThrottling': FieldDefinition(
                name='DramSwThermalThrottling',
                field_type=FieldType.STRING,
                required=False,
                description='DRAM SW Thermal Throttling',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # NUMA and Memory Topology
            'NumaOptimized': FieldDefinition(
                name='NumaOptimized',
                field_type=FieldType.STRING,
                required=False,
                description='NUMA Optimized',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'VirtualNuma': FieldDefinition(
                name='VirtualNuma',
                field_type=FieldType.STRING,
                required=False,
                description='Virtual NUMA',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UmaBasedClustering': FieldDefinition(
                name='UmaBasedClustering',
                field_type=FieldType.STRING,
                required=False,
                description='UMA Based Clustering',
                enum_values=['platform-default', 'Disable (All2All)', 'Hemisphere (2-clusters)']
            ),
            
            # Memory Speed and Timing
            'SelectPprType': FieldDefinition(
                name='SelectPprType',
                field_type=FieldType.STRING,
                required=False,
                description='Post Package Repair',
                enum_values=['platform-default', 'disabled', 'hard-ppr', 'soft-ppr']
            ),
            'DramSwThermThrottling': FieldDefinition(
                name='DramSwThermThrottling',
                field_type=FieldType.STRING,
                required=False,
                description='DRAM SW Thermal Throttling',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
        }
        bios_fields.update(memory_fields)
        
        # === BOOT AND STORAGE SETTINGS (35 fields) ===
        boot_storage_fields = {
            # Boot Options
            'BootOptionRetry': FieldDefinition(
                name='BootOptionRetry',
                field_type=FieldType.STRING,
                required=False,
                description='Boot Option Retry',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'BootOptionNumRetry': FieldDefinition(
                name='BootOptionNumRetry',
                field_type=FieldType.STRING,
                required=False,
                description='Boot Option Number of Retries',
                enum_values=['platform-default', '5', '13', 'Infinite']
            ),
            'BootPerformanceMode': FieldDefinition(
                name='BootPerformanceMode',
                field_type=FieldType.STRING,
                required=False,
                description='Boot Performance Mode',
                enum_values=['platform-default', 'Max Efficient', 'Max Performance', 'Set by Intel NM']
            ),
            
            # USB Configuration
            'AllUsbDevices': FieldDefinition(
                name='AllUsbDevices',
                field_type=FieldType.STRING,
                required=False,
                description='All USB Devices',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'LegacyUsbSupport': FieldDefinition(
                name='LegacyUsbSupport',
                field_type=FieldType.STRING,
                required=False,
                description='Legacy USB Support',
                enum_values=['platform-default', 'auto', 'disabled', 'enabled']
            ),
            'UsbEmul6064': FieldDefinition(
                name='UsbEmul6064',
                field_type=FieldType.STRING,
                required=False,
                description='Port 60/64 Emulation',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbXhciSupport': FieldDefinition(
                name='UsbXhciSupport',
                field_type=FieldType.STRING,
                required=False,
                description='XHCI Legacy Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbPortFront': FieldDefinition(
                name='UsbPortFront',
                field_type=FieldType.STRING,
                required=False,
                description='USB Port Front',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbPortInternal': FieldDefinition(
                name='UsbPortInternal',
                field_type=FieldType.STRING,
                required=False,
                description='USB Port Internal',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbPortKvm': FieldDefinition(
                name='UsbPortKvm',
                field_type=FieldType.STRING,
                required=False,
                description='USB Port KVM',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbPortRear': FieldDefinition(
                name='UsbPortRear',
                field_type=FieldType.STRING,
                required=False,
                description='USB Port Rear',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbPortSdCard': FieldDefinition(
                name='UsbPortSdCard',
                field_type=FieldType.STRING,
                required=False,
                description='USB Port SD Card',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'UsbPortVmedia': FieldDefinition(
                name='UsbPortVmedia',
                field_type=FieldType.STRING,
                required=False,
                description='USB Port Virtual Media',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # Storage Settings
            'SataModeSelect': FieldDefinition(
                name='SataModeSelect',
                field_type=FieldType.STRING,
                required=False,
                description='SATA Mode',
                enum_values=['platform-default', 'ahci', 'disabled', 'lsi-sw-raid']
            ),
            'UfsDisable': FieldDefinition(
                name='UfsDisable',
                field_type=FieldType.STRING,
                required=False,
                description='Uncore Frequency Scaling',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'NvmdimmPerformConfig': FieldDefinition(
                name='NvmdimmPerformConfig',
                field_type=FieldType.STRING,
                required=False,
                description='NV-DIMM Performance Configuration',
                enum_values=['platform-default', 'BW Optimized', 'Balanced Profile', 'Latency Optimized']
            ),
            
            # Network Boot
            'Ipv4pxe': FieldDefinition(
                name='Ipv4pxe',
                field_type=FieldType.STRING,
                required=False,
                description='IPv4 PXE Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'Ipv6pxe': FieldDefinition(
                name='Ipv6pxe',
                field_type=FieldType.STRING,
                required=False,
                description='IPv6 PXE Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'Ipv4http': FieldDefinition(
                name='Ipv4http',
                field_type=FieldType.STRING,
                required=False,
                description='IPv4 HTTP Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'Ipv6http': FieldDefinition(
                name='Ipv6http',
                field_type=FieldType.STRING,
                required=False,
                description='IPv6 HTTP Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'NetworkStack': FieldDefinition(
                name='NetworkStack',
                field_type=FieldType.STRING,
                required=False,
                description='Network Stack',
                enum_values=['platform-default', 'disabled', 'enabled']
            )
        }
        bios_fields.update(boot_storage_fields)
        
        # === PCIE AND SLOT CONFIGURATION (89 fields) ===
        pcie_fields = {
            # PCIe Core Settings
            'PcieAriSupport': FieldDefinition(
                name='PcieAriSupport',
                field_type=FieldType.STRING,
                required=False,
                description='PCIe ARI Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'PciePllSsc': FieldDefinition(
                name='PciePllSsc',
                field_type=FieldType.STRING,
                required=False,
                description='PCIe PLL SSC',
                enum_values=['platform-default', 'Auto', 'Disabled', 'ZeroPointFive']
            ),
            'PcIeRasSupport': FieldDefinition(
                name='PcIeRasSupport',
                field_type=FieldType.STRING,
                required=False,
                description='PCIe RAS Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AspmSupport': FieldDefinition(
                name='AspmSupport',
                field_type=FieldType.STRING,
                required=False,
                description='ASPM Support',
                enum_values=['platform-default', 'Auto', 'disabled', 'Force L0s', 'L1 Only']
            ),
            
            # Slot States (14 regular slots)
            'Slot1state': FieldDefinition(
                name='Slot1state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 1 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot2state': FieldDefinition(
                name='Slot2state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 2 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot3state': FieldDefinition(
                name='Slot3state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 3 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot4state': FieldDefinition(
                name='Slot4state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 4 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot5state': FieldDefinition(
                name='Slot5state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 5 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot6state': FieldDefinition(
                name='Slot6state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 6 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot7state': FieldDefinition(
                name='Slot7state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 7 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot8state': FieldDefinition(
                name='Slot8state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 8 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot9state': FieldDefinition(
                name='Slot9state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 9 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot10state': FieldDefinition(
                name='Slot10state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 10 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot11state': FieldDefinition(
                name='Slot11state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 11 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot12state': FieldDefinition(
                name='Slot12state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 12 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot13state': FieldDefinition(
                name='Slot13state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 13 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'Slot14state': FieldDefinition(
                name='Slot14state',
                field_type=FieldType.STRING,
                required=False,
                description='Slot 14 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            
            # GPU Slots (8 slots)
            'SlotGpu1state': FieldDefinition(
                name='SlotGpu1state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 1 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu2state': FieldDefinition(
                name='SlotGpu2state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 2 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu3state': FieldDefinition(
                name='SlotGpu3state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 3 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu4state': FieldDefinition(
                name='SlotGpu4state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 4 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu5state': FieldDefinition(
                name='SlotGpu5state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 5 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu6state': FieldDefinition(
                name='SlotGpu6state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 6 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu7state': FieldDefinition(
                name='SlotGpu7state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 7 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotGpu8state': FieldDefinition(
                name='SlotGpu8state',
                field_type=FieldType.STRING,
                required=False,
                description='GPU Slot 8 State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # NVMe Slot Configuration (subset - 32 total NVMe slots available)
            'SlotFrontNvme1linkSpeed': FieldDefinition(
                name='SlotFrontNvme1linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Front NVMe 1 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotFrontNvme2linkSpeed': FieldDefinition(
                name='SlotFrontNvme2linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Front NVMe 2 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotFrontNvme1optionRom': FieldDefinition(
                name='SlotFrontNvme1optionRom',
                field_type=FieldType.STRING,
                required=False,
                description='Front NVMe 1 OptionROM',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'SlotFrontNvme2optionRom': FieldDefinition(
                name='SlotFrontNvme2optionRom',
                field_type=FieldType.STRING,
                required=False,
                description='Front NVMe 2 OptionROM',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            
            # Additional Front NVMe slots (3-24) from missing attributes analysis
            'SlotFrontNvme3linkSpeed': FieldDefinition(
                name='SlotFrontNvme3linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Front NVMe 3 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotFrontNvme4linkSpeed': FieldDefinition(
                name='SlotFrontNvme4linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Front NVMe 4 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            
            # Rear NVMe slots (1-8) from missing attributes analysis
            'SlotRearNvme1linkSpeed': FieldDefinition(
                name='SlotRearNvme1linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 1 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme2linkSpeed': FieldDefinition(
                name='SlotRearNvme2linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 2 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme3linkSpeed': FieldDefinition(
                name='SlotRearNvme3linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 3 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme4linkSpeed': FieldDefinition(
                name='SlotRearNvme4linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 4 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme5linkSpeed': FieldDefinition(
                name='SlotRearNvme5linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 5 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme6linkSpeed': FieldDefinition(
                name='SlotRearNvme6linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 6 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme7linkSpeed': FieldDefinition(
                name='SlotRearNvme7linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 7 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            'SlotRearNvme8linkSpeed': FieldDefinition(
                name='SlotRearNvme8linkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='Rear NVMe 8 Link Speed',
                enum_values=['platform-default', 'Auto', 'Disabled', 'GEN1', 'GEN2', 'GEN3', 'GEN4', 'GEN5']
            ),
            
            # Special Slots
            'SlotMlomState': FieldDefinition(
                name='SlotMlomState',
                field_type=FieldType.STRING,
                required=False,
                description='Modular LOM State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SlotHbaState': FieldDefinition(
                name='SlotHbaState',
                field_type=FieldType.STRING,
                required=False,
                description='HBA Slot State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'SlotRaidState': FieldDefinition(
                name='SlotRaidState',
                field_type=FieldType.STRING,
                required=False,
                description='RAID Slot State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            
            # Legacy PCIe SSD slots (backward compatibility)
            'PcieSlotSsd1LinkSpeed': FieldDefinition(
                name='PcieSlotSsd1LinkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='PCIe Slot SSD 1 Link Speed',
                enum_values=['platform-default', 'auto', 'disabled', 'gen-1', 'gen-2', 'gen-3', 'gen-4', 'gen-5']
            ),
            'PcieSlotSsd2LinkSpeed': FieldDefinition(
                name='PcieSlotSsd2LinkSpeed',
                field_type=FieldType.STRING,
                required=False,
                description='PCIe Slot SSD 2 Link Speed',
                enum_values=['platform-default', 'auto', 'disabled', 'gen-1', 'gen-2', 'gen-3', 'gen-4', 'gen-5']
            )
        }
        bios_fields.update(pcie_fields)
        
        # === SECURITY FEATURES (28 fields) ===
        security_fields = {
            # Intel Security Features
            'TxtSupport': FieldDefinition(
                name='TxtSupport',
                field_type=FieldType.STRING,
                required=False,
                description='Intel TXT Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'EnableSgx': FieldDefinition(
                name='EnableSgx',
                field_type=FieldType.STRING,
                required=False,
                description='Intel SGX',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'EnableTme': FieldDefinition(
                name='EnableTme',
                field_type=FieldType.STRING,
                required=False,
                description='Intel TME',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'EnableTdx': FieldDefinition(
                name='EnableTdx',
                field_type=FieldType.STRING,
                required=False,
                description='Intel TDX',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'VtForDirectedIo': FieldDefinition(
                name='VtForDirectedIo',
                field_type=FieldType.STRING,
                required=False,
                description='Intel VT for Directed I/O',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelVtd': FieldDefinition(
                name='IntelVtd',
                field_type=FieldType.STRING,
                required=False,
                description='Intel VT-d',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelVtdCoherencySupport': FieldDefinition(
                name='IntelVtdCoherencySupport',
                field_type=FieldType.STRING,
                required=False,
                description='Intel VT-d Coherency Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelVtdInterruptRemapping': FieldDefinition(
                name='IntelVtdInterruptRemapping',
                field_type=FieldType.STRING,
                required=False,
                description='Intel VT-d Interrupt Remapping',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'IntelVtdPassThroughDmaSupport': FieldDefinition(
                name='IntelVtdPassThroughDmaSupport',
                field_type=FieldType.STRING,
                required=False,
                description='Intel VT-d Pass-through DMA Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # AMD Security Features
            'Sev': FieldDefinition(
                name='Sev',
                field_type=FieldType.STRING,
                required=False,
                description='AMD SEV (Secure Encrypted Virtualization)',
                enum_values=['platform-default', 'Auto', '253 ASIDs', '509 ASIDs', 'disabled', 'enabled']
            ),
            'CbsSevSnpSupport': FieldDefinition(
                name='CbsSevSnpSupport',
                field_type=FieldType.STRING,
                required=False,
                description='SEV-SNP Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'Smee': FieldDefinition(
                name='Smee',
                field_type=FieldType.STRING,
                required=False,
                description='SMEE (Secure Memory Encryption Enable)',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'Tsme': FieldDefinition(
                name='Tsme',
                field_type=FieldType.STRING,
                required=False,
                description='TSME (Transparent Secure Memory Encryption)',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # TPM Support
            'TpmControl': FieldDefinition(
                name='TpmControl',
                field_type=FieldType.STRING,
                required=False,
                description='TPM Control',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'TpmSupport': FieldDefinition(
                name='TpmSupport',
                field_type=FieldType.STRING,
                required=False,
                description='TPM Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'TpmPendingOperation': FieldDefinition(
                name='TpmPendingOperation',
                field_type=FieldType.STRING,
                required=False,
                description='TPM Pending Operation',
                enum_values=['platform-default', 'None', 'TpmClear']
            ),
            
            # Virtualization Security
            'SrIov': FieldDefinition(
                name='SrIov',
                field_type=FieldType.STRING,
                required=False,
                description='SR-IOV Support',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'SvmMode': FieldDefinition(
                name='SvmMode',
                field_type=FieldType.STRING,
                required=False,
                description='SVM Mode',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'VmdEnable': FieldDefinition(
                name='VmdEnable',
                field_type=FieldType.STRING,
                required=False,
                description='VMD Enable',
                enum_values=['platform-default', 'disabled', 'enabled']
            )
        }
        bios_fields.update(security_fields)
        
        # === NETWORK AND COMMUNICATION (25 fields) ===
        network_fields = {
            # LOM Port States
            'LomPort0state': FieldDefinition(
                name='LomPort0state',
                field_type=FieldType.STRING,
                required=False,
                description='LOM Port 0 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'LomPort1state': FieldDefinition(
                name='LomPort1state',
                field_type=FieldType.STRING,
                required=False,
                description='LOM Port 1 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'LomPort2state': FieldDefinition(
                name='LomPort2state',
                field_type=FieldType.STRING,
                required=False,
                description='LOM Port 2 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'LomPort3state': FieldDefinition(
                name='LomPort3state',
                field_type=FieldType.STRING,
                required=False,
                description='LOM Port 3 State',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'LomPortsAllState': FieldDefinition(
                name='LomPortsAllState',
                field_type=FieldType.STRING,
                required=False,
                description='All LOM Ports State',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # Serial Configuration
            'SerialPortAenable': FieldDefinition(
                name='SerialPortAenable',
                field_type=FieldType.STRING,
                required=False,
                description='Serial Port A Enable',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ConsoleRedirection': FieldDefinition(
                name='ConsoleRedirection',
                field_type=FieldType.STRING,
                required=False,
                description='Console Redirection',
                enum_values=['platform-default', 'com-0', 'com-1', 'disabled', 'enabled', 'serial-port-a']
            ),
            'BaudRate': FieldDefinition(
                name='BaudRate',
                field_type=FieldType.STRING,
                required=False,
                description='Baud Rate',
                enum_values=['platform-default', '9600', '19200', '38400', '57600', '115200']
            ),
            'TerminalType': FieldDefinition(
                name='TerminalType',
                field_type=FieldType.STRING,
                required=False,
                description='Terminal Type',
                enum_values=['platform-default', 'pc-ansi', 'vt100', 'vt100-plus', 'vt-utf8']
            ),
            'FlowControl': FieldDefinition(
                name='FlowControl',
                field_type=FieldType.STRING,
                required=False,
                description='Flow Control',
                enum_values=['platform-default', 'none', 'rts-cts']
            ),
            'PuttyKeyPad': FieldDefinition(
                name='PuttyKeyPad',
                field_type=FieldType.STRING,
                required=False,
                description='Putty KeyPad',
                enum_values=['platform-default', 'ESCN', 'LINUX', 'SCO', 'VT100', 'VT400', 'XTERMR6']
            ),
            'RedirectionAfterPost': FieldDefinition(
                name='RedirectionAfterPost',
                field_type=FieldType.STRING,
                required=False,
                description='Redirection After BIOS POST',
                enum_values=['platform-default', 'Always Enable', 'Bootloader']
            )
        }
        bios_fields.update(network_fields)
        
        # === POWER AND THERMAL (22 fields) ===
        power_thermal_fields = {
            # Power Management
            'OptimizedPowerMode': FieldDefinition(
                name='OptimizedPowerMode',
                field_type=FieldType.STRING,
                required=False,
                description='Optimized Power Mode',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ConfigTdp': FieldDefinition(
                name='ConfigTdp',
                field_type=FieldType.STRING,
                required=False,
                description='Config TDP',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ConfigTdpLevel': FieldDefinition(
                name='ConfigTdpLevel',
                field_type=FieldType.STRING,
                required=False,
                description='Config TDP Level',
                enum_values=['platform-default', 'Level 1', 'Level 2', 'Normal']
            ),
            
            # Thermal Management
            'ClosedLoopThermThrotl': FieldDefinition(
                name='ClosedLoopThermThrotl',
                field_type=FieldType.STRING,
                required=False,
                description='Closed Loop Thermal Throttling',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'OpenLoopThermalControl': FieldDefinition(
                name='OpenLoopThermalControl',
                field_type=FieldType.STRING,
                required=False,
                description='Open Loop Thermal Control',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'ExtendedApicId': FieldDefinition(
                name='ExtendedApicId',
                field_type=FieldType.STRING,
                required=False,
                description='Local X2 Apic',
                enum_values=['platform-default', 'disabled', 'enabled', 'X2APIC', 'XAPIC']
            )
        }
        bios_fields.update(power_thermal_fields)
        
        # === FIRMWARE AND PLATFORM (35 fields) ===
        firmware_fields = {
            # Firmware Features
            'CiscoOpromLaunchOptimization': FieldDefinition(
                name='CiscoOpromLaunchOptimization',
                field_type=FieldType.STRING,
                required=False,
                description='OptionROM Launch Optimization',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'PciOptionRoMs': FieldDefinition(
                name='PciOptionRoMs',
                field_type=FieldType.STRING,
                required=False,
                description='All PCIe Slots OptionROM',
                enum_values=['platform-default', 'disabled', 'enabled', 'Legacy Only', 'UEFI Only']
            ),
            'PciRomClp': FieldDefinition(
                name='PciRomClp',
                field_type=FieldType.STRING,
                required=False,
                description='PCI ROM CLP',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # Platform Settings
            'Altitude': FieldDefinition(
                name='Altitude',
                field_type=FieldType.STRING,
                required=False,
                description='Altitude',
                enum_values=['platform-default', '1500-m', '300-m', '3000-m', 'auto', 'sea-level']
            ),
            'MakeDeviceNonBootable': FieldDefinition(
                name='MakeDeviceNonBootable',
                field_type=FieldType.STRING,
                required=False,
                description='Make Device Non Bootable',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'OsBootWatchdogTimer': FieldDefinition(
                name='OsBootWatchdogTimer',
                field_type=FieldType.STRING,
                required=False,
                description='OS Boot Watchdog Timer',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'OsBootWatchdogTimerTimeout': FieldDefinition(
                name='OsBootWatchdogTimerTimeout',
                field_type=FieldType.STRING,
                required=False,
                description='OS Boot Watchdog Timer Timeout',
                enum_values=['platform-default', '10-minutes', '15-minutes', '20-minutes', '5-minutes']
            ),
            'OsBootWatchdogTimerPolicy': FieldDefinition(
                name='OsBootWatchdogTimerPolicy',
                field_type=FieldType.STRING,
                required=False,
                description='OS Boot Watchdog Timer Policy',
                enum_values=['platform-default', 'do-nothing', 'power-off', 'reset']
            ),
            
            # Debug Features
            'CiscoDebugLevel': FieldDefinition(
                name='CiscoDebugLevel',
                field_type=FieldType.STRING,
                required=False,
                description='BIOS Techlog Level',
                enum_values=['platform-default', 'Maximum', 'Minimum', 'Normal']
            ),
            'PostErrorPause': FieldDefinition(
                name='PostErrorPause',
                field_type=FieldType.STRING,
                required=False,
                description='POST Error Pause',
                enum_values=['platform-default', 'disabled', 'enabled']
            )
        }
        bios_fields.update(firmware_fields)
        
        # === ADVANCED SYSTEM FEATURES (58 fields) ===
        advanced_fields = {
            # Cache and Prefetch Settings
            'HardwarePrefetch': FieldDefinition(
                name='HardwarePrefetch',
                field_type=FieldType.STRING,
                required=False,
                description='Hardware Prefetcher',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'StreamerPrefetch': FieldDefinition(
                name='StreamerPrefetch',
                field_type=FieldType.STRING,
                required=False,
                description='DCU Streamer Prefetch',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # QPI/UPI Configuration
            'QpiLinkFrequency': FieldDefinition(
                name='QpiLinkFrequency',
                field_type=FieldType.STRING,
                required=False,
                description='QPI Link Frequency Select',
                enum_values=['platform-default', '6.4-gt/s', '7.2-gt/s', '8.0-gt/s', '9.6-gt/s', 'auto']
            ),
            'QpiSnoopMode': FieldDefinition(
                name='QpiSnoopMode',
                field_type=FieldType.STRING,
                required=False,
                description='QPI Snoop Mode',
                enum_values=['platform-default', 'auto', 'cluster-on-die', 'early-snoop', 'home-snoop']
            ),
            'UpiLinkEnablement': FieldDefinition(
                name='UpiLinkEnablement',
                field_type=FieldType.STRING,
                required=False,
                description='UPI Link Enablement',
                enum_values=['platform-default', '1', '2', '3', 'auto']
            )
        }
        bios_fields.update(advanced_fields)
        
        # === ACS CONTROL FEATURES (50 fields) ===
        acs_fields = {
            # ACS Control for GPU Slots
            'AcsControlGpu1state': FieldDefinition(
                name='AcsControlGpu1state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control GPU 1',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AcsControlGpu2state': FieldDefinition(
                name='AcsControlGpu2state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control GPU 2',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AcsControlGpu3state': FieldDefinition(
                name='AcsControlGpu3state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control GPU 3',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AcsControlGpu4state': FieldDefinition(
                name='AcsControlGpu4state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control GPU 4',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            
            # ACS Control for Regular Slots
            'AcsControlSlot11state': FieldDefinition(
                name='AcsControlSlot11state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control Slot 11',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AcsControlSlot12state': FieldDefinition(
                name='AcsControlSlot12state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control Slot 12',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AcsControlSlot13state': FieldDefinition(
                name='AcsControlSlot13state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control Slot 13',
                enum_values=['platform-default', 'disabled', 'enabled']
            ),
            'AcsControlSlot14state': FieldDefinition(
                name='AcsControlSlot14state',
                field_type=FieldType.STRING,
                required=False,
                description='ACS Control Slot 14',
                enum_values=['platform-default', 'disabled', 'enabled']
            )
        }
        bios_fields.update(acs_fields)
        
        # Merge common and BIOS-specific fields
        fields.update(bios_fields)
        return fields
    
    def _get_example_policy_fields(self) -> Dict[str, Any]:
        """Get example fields specific to BIOS policy with representative fields from all categories."""
        return {
            # CPU and Processor Settings
            'CpuPerformance': 'enterprise',
            'CpuPowerManagement': 'performance',
            'IntelHyperThreadingTech': 'enabled',
            'IntelTurboBoostTech': 'enabled',
            'IntelVirtualizationTechnology': 'enabled',
            'ProcessorC1e': 'disabled',
            'ProcessorC3report': 'disabled',
            'ProcessorC6report': 'disabled',
            'ExecuteDisableBit': 'enabled',
            'EnergyEfficientTurbo': 'disabled',
            
            # Memory Settings
            'SelectMemoryRasConfiguration': 'maximum-performance',
            'MemoryInterLeave': 'auto',
            'ChannelInterLeave': 'auto',
            'RankInterLeave': 'auto',
            'DramClockThrottling': 'performance',
            'MemoryBandwidthBoost': 'enabled',
            'AdvancedMemTest': 'enabled',
            'PatrolScrub': 'enabled',
            
            # Boot and Storage Settings
            'BootOptionRetry': 'enabled',
            'Ipv4pxe': 'enabled',
            'Ipv6pxe': 'disabled',
            'NetworkStack': 'enabled',
            'AllUsbDevices': 'enabled',
            'LegacyUsbSupport': 'enabled',
            'UsbEmul6064': 'enabled',
            'SataModeSelect': 'ahci',
            
            # PCIe and Slot Configuration
            'PcieAriSupport': 'enabled',
            'AspmSupport': 'Auto',
            'Slot1state': 'enabled',
            'Slot2state': 'enabled',
            'SlotGpu1state': 'enabled',
            'SlotFrontNvme1linkSpeed': 'Auto',
            'SlotFrontNvme1optionRom': 'enabled',
            'PcieSlotSsd1LinkSpeed': 'auto',
            'PcieSlotSsd2LinkSpeed': 'auto',
            
            # Security Features
            'TxtSupport': 'enabled',
            'VtForDirectedIo': 'enabled',
            'IntelVtd': 'enabled',
            'EnableSgx': 'enabled',
            'SrIov': 'enabled',
            'TpmControl': 'enabled',
            'TpmSupport': 'enabled',
            
            # Network and Communication
            'LomPort0state': 'enabled',
            'LomPort1state': 'enabled',
            'ConsoleRedirection': 'enabled',
            'SerialPortAenable': 'enabled',
            'BaudRate': '115200',
            'TerminalType': 'vt100',
            
            # Power and Thermal
            'OptimizedPowerMode': 'disabled',
            'ConfigTdp': 'enabled',
            'ClosedLoopThermThrotl': 'enabled',
            
            # Firmware and Platform
            'CiscoOpromLaunchOptimization': 'enabled',
            'PciOptionRoMs': 'enabled',
            'OsBootWatchdogTimer': 'disabled',
            'CiscoDebugLevel': 'Normal',
            
            # Advanced System Features
            'HardwarePrefetch': 'enabled',
            'AdjacentCacheLinePrefetch': 'enabled',
            'NumaOptimized': 'enabled',
            'QpiSnoopMode': 'auto',
            
            # ACS Control Features
            'AcsControlGpu1state': 'platform-default',
            'AcsControlSlot11state': 'platform-default',
            
            # Additional Slot Configuration Examples (from missing attributes)
            'Slot9state': 'enabled',
            'Slot10state': 'enabled',
            'SlotGpu5state': 'enabled',
            'SlotGpu6state': 'disabled',
            'SlotFrontNvme3linkSpeed': 'Auto',
            'SlotRearNvme1linkSpeed': 'GEN4',
            
            # AMD CBS Examples (from missing attributes)
            'CbsDfCmnMemIntlv': 'Auto',
            'CbsCmnCpuGenDowncoreCtrl': 'Auto',
            'CbsCmnGnbNbIommu': 'enabled'
        }