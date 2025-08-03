# Intersight GitOps Tool - Object Reference

Generated on: 2025-08-03 21:19:55

This document provides comprehensive reference information for all Intersight object types
supported by the GitOps tool. Each object type includes field definitions, constraints,
examples, and usage instructions.

## Table of Contents

- [Access Policy](#access-policy)
- [Adapter Configuration Policy](#adapter-configuration-policy)
- [BIOS Policy](#bios-policy)
- [Boot Order Policy](#boot-order-policy)
- [Certificate Management Policy](#certificate-management-policy)
- [Chassis Profile](#chassis-profile)
- [Scrub Policy](#scrub-policy)
- [Device Connector Policy](#device-connector-policy)
- [Ethernet Network Control Policy](#ethernet-network-control-policy)
- [Ethernet Network Group Policy](#ethernet-network-group-policy)
- [VLAN Policy](#vlan-policy)
- [VSAN Policy](#vsan-policy)
- [FC Zone Policy](#fc-zone-policy)
- [Flow Control Policy](#flow-control-policy)
- [Link Aggregation Policy](#link-aggregation-policy)
- [Link Control Policy](#link-control-policy)
- [Multicast Policy](#multicast-policy)
- [Port Policy](#port-policy)
- [Switch Control Policy](#switch-control-policy)
- [Domain Profile](#domain-profile)
- [System QoS Policy](#system-qos-policy)
- [WWNN Pool](#wwnn-pool)
- [Firmware Policy](#firmware-policy)
- [Local User Policy](#local-user-policy)
- [LDAP Policy](#ldap-policy)
- [IPMI Over LAN Policy](#ipmi-over-lan-policy)
- [IP Pool](#ip-pool)
- [IQN Pool](#iqn-pool)
- [Virtual KVM Policy](#virtual-kvm-policy)
- [MAC Pool](#mac-pool)
- [Persistent Memory Policy](#persistent-memory-policy)
- [Memory Policy](#memory-policy)
- [Network Configuration Policy](#network-configuration-policy)
- [NTP Policy](#ntp-policy)
- [Organization](#organization)
- [Power Policy](#power-policy)
- [Resource Pool](#resource-pool)
- [Server Pool Qualification Policy](#server-pool-qualification-policy)
- [SD Card Policy](#sd-card-policy)
- [Server Profile](#server-profile)
- [SMTP Policy](#smtp-policy)
- [SNMP Policy](#snmp-policy)
- [Serial Over LAN Policy](#serial-over-lan-policy)
- [SSH Policy](#ssh-policy)
- [Drive Security Policy](#drive-security-policy)
- [Storage Policy](#storage-policy)
- [Syslog Policy](#syslog-policy)
- [Thermal Policy](#thermal-policy)
- [UUID Pool](#uuid-pool)
- [Virtual Media Policy](#virtual-media-policy)
- [Ethernet Adapter Policy](#ethernet-adapter-policy)
- [Ethernet QoS Policy](#ethernet-qos-policy)
- [Fibre Channel Adapter Policy](#fibre-channel-adapter-policy)
- [Fibre Channel Network Policy](#fibre-channel-network-policy)
- [iSCSI Adapter Policy](#iscsi-adapter-policy)
- [iSCSI Boot Policy](#iscsi-boot-policy)
- [iSCSI Static Target Policy](#iscsi-static-target-policy)
- [LAN Connectivity Policy](#lan-connectivity-policy)
- [SAN Connectivity Policy](#san-connectivity-policy)

## General Information

### Organization References

Objects that belong to an organization reference it using a simple name format:

```yaml
ObjectType: policies/bios
Name: my-policy
Organization: default
```

## Object Types

### Access Policy

**Object Type:** `access.Policy`
**Folder Path:** `policies/access/`

**Description:**

Access Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/access` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/access
Name: example-access-policy
Description: Example Access Policy policy for development environment
Organization: default
```

---

### Adapter Configuration Policy

**Object Type:** `adapter.ConfigPolicy`
**Folder Path:** `policies/adapter_config/`

**Description:**

Adapter Configuration Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/adapter_config` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Settings | array | No | Configuration for all the adapters available in the server | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/adapter_config
Name: example-adapter-configuration-policy
Description: Example Adapter Configuration Policy policy for development environment
Organization: default
Settings:
- SlotId: MLOM
  EthSettings:
    LldpEnabled: true
  FcSettings:
    FipEnabled: false
```

---

### BIOS Policy

**Object Type:** `bios.Policy`
**Folder Path:** `policies/bios/`

**Description:**

BIOS Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/bios` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AcsControlGpu1state | string | No | ACS Control GPU 1 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlGpu2state | string | No | ACS Control GPU 2 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlGpu3state | string | No | ACS Control GPU 3 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlGpu4state | string | No | ACS Control GPU 4 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlSlot11state | string | No | ACS Control Slot 11 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlSlot12state | string | No | ACS Control Slot 12 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlSlot13state | string | No | ACS Control Slot 13 | Values: `platform-default`, `disabled`, `enabled` |
| AcsControlSlot14state | string | No | ACS Control Slot 14 | Values: `platform-default`, `disabled`, `enabled` |
| AdjacentCacheLinePrefetch | string | No | Adjacent Cache Line Prefetch | Values: `platform-default`, `disabled`, `enabled` |
| AdvancedMemTest | string | No | Advanced Memory Test | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| AllUsbDevices | string | No | All USB Devices | Values: `platform-default`, `disabled`, `enabled` |
| Altitude | string | No | Altitude | Values: `platform-default`, `1500-m`, `300-m`, `3000-m`, `auto`, `sea-level` |
| AspmSupport | string | No | ASPM Support | Values: `platform-default`, `Auto`, `disabled`, `Force L0s`, `L1 Only` |
| AutonumousCstateEnable | string | No | Autonomous C-state Enable | Values: `platform-default`, `disabled`, `enabled` |
| BaudRate | string | No | Baud Rate | Values: `platform-default`, `9600`, `19200`, `38400`, `57600`, `115200` |
| BootOptionNumRetry | string | No | Boot Option Number of Retries | Values: `platform-default`, `5`, `13`, `Infinite` |
| BootOptionRetry | string | No | Boot Option Retry | Values: `platform-default`, `disabled`, `enabled` |
| BootPerformanceMode | string | No | Boot Performance Mode | Values: `platform-default`, `Max Efficient`, `Max Performance`, `Set by Intel NM` |
| C1autoDemotion | string | No | C1 Auto Demotion | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| CbsCmnCpuAvx512 | string | No | AVX512 Support | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| CbsCmnCpuCcdCtrl | string | No | AMD CCD Control | Values: `platform-default`, `Auto`, `2 CCDs`, `4 CCDs`, `6 CCDs`, `8 CCDs` |
| CbsCmnCpuCpb | string | No | Core Performance Boost | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| CbsCmnCpuGenDowncoreCtrl | string | No | AMD CPU Downcore Control | Values: `platform-default`, `Auto`, `Four (2 + 2)`, `Six (3 + 3)`, `Two (1 + 1)` |
| CbsCmnCpuSmee | string | No | SME (Secure Memory Encryption) | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| CbsCmnCpuStreamingStoresCtrl | string | No | Streaming Stores Control | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| CbsCmnGnbNbIommu | string | No | AMD IOMMU Control | Values: `platform-default`, `Auto`, `disabled`, `enabled` |
| CbsDfCmnMemIntlv | string | No | AMD Memory Interleaving | Values: `platform-default`, `Auto`, `Channel`, `Die`, `Socket` |
| CbsDfCmnMemIntlvSize | string | No | AMD Memory Interleaving Size | Values: `platform-default`, `256 Bytes`, `512 Bytes`, `1 KB`, `2 KB`, `4 KB` |
| CbsSevSnpSupport | string | No | SEV-SNP Support | Values: `platform-default`, `disabled`, `enabled` |
| ChannelInterLeave | string | No | Channel Interleaving | Values: `platform-default`, `1-way`, `2-way`, `3-way`, `4-way`, `auto` |
| CiscoDebugLevel | string | No | BIOS Techlog Level | Values: `platform-default`, `Maximum`, `Minimum`, `Normal` |
| CiscoOpromLaunchOptimization | string | No | OptionROM Launch Optimization | Values: `platform-default`, `disabled`, `enabled` |
| ClosedLoopThermThrotl | string | No | Closed Loop Thermal Throttling | Values: `platform-default`, `disabled`, `enabled` |
| ConfigTdp | string | No | Config TDP | Values: `platform-default`, `disabled`, `enabled` |
| ConfigTdpLevel | string | No | Config TDP Level | Values: `platform-default`, `Level 1`, `Level 2`, `Normal` |
| ConsoleRedirection | string | No | Console Redirection | Values: `platform-default`, `com-0`, `com-1`, `disabled`, `enabled`, `serial-port-a` |
| CoreMultiProcessing | string | No | Core Multi Processing | Values: `platform-default`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `all` |
| CpuEnergyPerformance | string | No | Energy Performance | Values: `platform-default`, `balanced-energy`, `balanced-performance`, `balanced-power`, `energy-efficient`, `performance`, `power` |
| CpuHardwarePowerManagement | string | No | CPU Hardware Power Management | Values: `platform-default`, `disabled`, `hwpm-native-mode`, `hwpm-oob-mode`, `native-mode`, `oob-mode` |
| CpuPerformance | string | No | CPU Performance setting | Values: `platform-default`, `custom`, `enterprise`, `high-throughput`, `hpc` |
| CpuPowerManagement | string | No | CPU Power Management setting | Values: `platform-default`, `custom`, `disabled`, `energy-efficient`, `performance` |
| DcuIpPrefetch | string | No | DCU IP Prefetch | Values: `platform-default`, `disabled`, `enabled` |
| DcuStreamerPrefetch | string | No | DCU Streamer Prefetch | Values: `platform-default`, `disabled`, `enabled` |
| DemandScrub | string | No | Demand Scrub | Values: `platform-default`, `disabled`, `enabled` |
| Description | string | No | Description of the policy | - |
| DirectCacheAccess | string | No | Direct Cache Access | Values: `platform-default`, `auto`, `disabled`, `enabled` |
| DramClockThrottling | string | No | DRAM Clock Throttling | Values: `platform-default`, `auto`, `balanced`, `energy-efficient`, `performance` |
| DramRefreshRate | string | No | DRAM Refresh Rate | Values: `platform-default`, `1x`, `2x`, `3x`, `4x`, `Auto` |
| DramSwThermThrottling | string | No | DRAM SW Thermal Throttling | Values: `platform-default`, `disabled`, `enabled` |
| DramSwThermalThrottling | string | No | DRAM SW Thermal Throttling | Values: `platform-default`, `disabled`, `enabled` |
| EnableRmt | string | No | RMT (Runtime Memory Throttling) | Values: `platform-default`, `disabled`, `enabled` |
| EnableSgx | string | No | Intel SGX | Values: `platform-default`, `disabled`, `enabled` |
| EnableTdx | string | No | Intel TDX | Values: `platform-default`, `disabled`, `enabled` |
| EnableTme | string | No | Intel TME | Values: `platform-default`, `disabled`, `enabled` |
| EnergyEfficientTurbo | string | No | Energy Efficient Turbo | Values: `platform-default`, `disabled`, `enabled` |
| ErrorCheckScrub | string | No | Error Check Scrub | Values: `platform-default`, `disabled`, `enabled` |
| ExecuteDisableBit | string | No | Execute Disable Bit | Values: `platform-default`, `disabled`, `enabled` |
| ExtendedApicId | string | No | Local X2 Apic | Values: `platform-default`, `disabled`, `enabled`, `X2APIC`, `XAPIC` |
| FlowControl | string | No | Flow Control | Values: `platform-default`, `none`, `rts-cts` |
| HardwarePrefetch | string | No | Hardware Prefetcher | Values: `platform-default`, `disabled`, `enabled` |
| HwPrefetcher | string | No | Hardware Prefetcher | Values: `platform-default`, `disabled`, `enabled` |
| ImcInterleave | string | No | IMC Interleaving | Values: `platform-default`, `1-way`, `2-way`, `4-way`, `8-way`, `auto` |
| IntelHyperThreadingTech | string | No | Intel Hyper Threading Technology | Values: `platform-default`, `disabled`, `enabled` |
| IntelSpeedSelect | string | No | Intel Speed Select Technology | Values: `platform-default`, `Auto`, `Base`, `Config 1`, `Config 2`, `Config 3`, `Config 4` |
| IntelSpeedStepTech | string | No | Intel SpeedStep Technology | Values: `platform-default`, `disabled`, `enabled` |
| IntelTurboBoostTech | string | No | Intel Turbo Boost Technology | Values: `platform-default`, `disabled`, `enabled` |
| IntelVirtualizationTechnology | string | No | Intel Virtualization Technology | Values: `platform-default`, `disabled`, `enabled` |
| IntelVtd | string | No | Intel VT-d | Values: `platform-default`, `disabled`, `enabled` |
| IntelVtdCoherencySupport | string | No | Intel VT-d Coherency Support | Values: `platform-default`, `disabled`, `enabled` |
| IntelVtdInterruptRemapping | string | No | Intel VT-d Interrupt Remapping | Values: `platform-default`, `disabled`, `enabled` |
| IntelVtdPassThroughDmaSupport | string | No | Intel VT-d Pass-through DMA Support | Values: `platform-default`, `disabled`, `enabled` |
| Ipv4http | string | No | IPv4 HTTP Support | Values: `platform-default`, `disabled`, `enabled` |
| Ipv4pxe | string | No | IPv4 PXE Support | Values: `platform-default`, `disabled`, `enabled` |
| Ipv6http | string | No | IPv6 HTTP Support | Values: `platform-default`, `disabled`, `enabled` |
| Ipv6pxe | string | No | IPv6 PXE Support | Values: `platform-default`, `disabled`, `enabled` |
| LegacyUsbSupport | string | No | Legacy USB Support | Values: `platform-default`, `auto`, `disabled`, `enabled` |
| LomPort0state | string | No | LOM Port 0 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| LomPort1state | string | No | LOM Port 1 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| LomPort2state | string | No | LOM Port 2 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| LomPort3state | string | No | LOM Port 3 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| LomPortsAllState | string | No | All LOM Ports State | Values: `platform-default`, `disabled`, `enabled` |
| MakeDeviceNonBootable | string | No | Make Device Non Bootable | Values: `platform-default`, `disabled`, `enabled` |
| MemoryBandwidthBoost | string | No | Memory Bandwidth Boost | Values: `platform-default`, `disabled`, `enabled` |
| MemoryInterLeave | string | No | Memory Interleaving | Values: `platform-default`, `1-way`, `2-way`, `4-way`, `8-way`, `auto` |
| MemoryRefreshRate | string | No | Memory Refresh Rate | Values: `platform-default`, `1x`, `2x` |
| MemoryThermalThrottling | string | No | Memory Thermal Throttling | Values: `platform-default`, `disabled`, `enabled` |
| MirroringMode | string | No | Memory Mirroring Mode | Values: `platform-default`, `inter-socket`, `intra-socket` |
| NetworkStack | string | No | Network Stack | Values: `platform-default`, `disabled`, `enabled` |
| NumaOptimized | string | No | NUMA Optimized | Values: `platform-default`, `disabled`, `enabled` |
| NvmdimmPerformConfig | string | No | NV-DIMM Performance Configuration | Values: `platform-default`, `BW Optimized`, `Balanced Profile`, `Latency Optimized` |
| OpenLoopThermalControl | string | No | Open Loop Thermal Control | Values: `platform-default`, `disabled`, `enabled` |
| OptimizedPowerMode | string | No | Optimized Power Mode | Values: `platform-default`, `disabled`, `enabled` |
| Organization | string | Yes | Name of the organization | - |
| OsBootWatchdogTimer | string | No | OS Boot Watchdog Timer | Values: `platform-default`, `disabled`, `enabled` |
| OsBootWatchdogTimerPolicy | string | No | OS Boot Watchdog Timer Policy | Values: `platform-default`, `do-nothing`, `power-off`, `reset` |
| OsBootWatchdogTimerTimeout | string | No | OS Boot Watchdog Timer Timeout | Values: `platform-default`, `10-minutes`, `15-minutes`, `20-minutes`, `5-minutes` |
| PackageCstateLimit | string | No | Package C State Limit | Values: `platform-default`, `Auto`, `C0 C1 State`, `C0/C1`, `C2`, `C6 Non Retention`, `C6 Retention`, `No Limit` |
| PartialMirrorModeConfig | string | No | Partial Memory Mirror Mode Configuration | Values: `platform-default`, `disabled`, `percentage`, `value-in-gb` |
| PatrolScrub | string | No | Patrol Scrub | Values: `platform-default`, `disabled`, `enabled` |
| PcIeRasSupport | string | No | PCIe RAS Support | Values: `platform-default`, `disabled`, `enabled` |
| PciOptionRoMs | string | No | All PCIe Slots OptionROM | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| PciRomClp | string | No | PCI ROM CLP | Values: `platform-default`, `disabled`, `enabled` |
| PcieAriSupport | string | No | PCIe ARI Support | Values: `platform-default`, `disabled`, `enabled` |
| PciePllSsc | string | No | PCIe PLL SSC | Values: `platform-default`, `Auto`, `Disabled`, `ZeroPointFive` |
| PcieSlotSsd1LinkSpeed | string | No | PCIe Slot SSD 1 Link Speed | Values: `platform-default`, `auto`, `disabled`, `gen-1`, `gen-2`, `gen-3`, `gen-4`, `gen-5` |
| PcieSlotSsd2LinkSpeed | string | No | PCIe Slot SSD 2 Link Speed | Values: `platform-default`, `auto`, `disabled`, `gen-1`, `gen-2`, `gen-3`, `gen-4`, `gen-5` |
| PostErrorPause | string | No | POST Error Pause | Values: `platform-default`, `disabled`, `enabled` |
| ProcessorC1e | string | No | Processor C1E support | Values: `platform-default`, `disabled`, `enabled` |
| ProcessorC3report | string | No | Processor C3 Report | Values: `platform-default`, `disabled`, `enabled` |
| ProcessorC6report | string | No | Processor C6 Report | Values: `platform-default`, `disabled`, `enabled` |
| ProcessorCstate | string | No | CPU C State | Values: `platform-default`, `disabled`, `enabled` |
| ProcessorEistEnable | string | No | Enhanced Intel SpeedStep Technology | Values: `platform-default`, `disabled`, `enabled` |
| ProcessorEppProfile | string | No | Processor EPP Profile | Values: `platform-default`, `Balanced Performance`, `Balanced Power`, `Performance`, `Power` |
| PsdCoordType | string | No | P-State Coordination | Values: `platform-default`, `HW All`, `SW All`, `SW Any` |
| PuttyKeyPad | string | No | Putty KeyPad | Values: `platform-default`, `ESCN`, `LINUX`, `SCO`, `VT100`, `VT400`, `XTERMR6` |
| QpiLinkFrequency | string | No | QPI Link Frequency Select | Values: `platform-default`, `6.4-gt/s`, `7.2-gt/s`, `8.0-gt/s`, `9.6-gt/s`, `auto` |
| QpiSnoopMode | string | No | QPI Snoop Mode | Values: `platform-default`, `auto`, `cluster-on-die`, `early-snoop`, `home-snoop` |
| RankInterLeave | string | No | Rank Interleaving | Values: `platform-default`, `1-way`, `2-way`, `4-way`, `8-way`, `auto` |
| RedirectionAfterPost | string | No | Redirection After BIOS POST | Values: `platform-default`, `Always Enable`, `Bootloader` |
| SataModeSelect | string | No | SATA Mode | Values: `platform-default`, `ahci`, `disabled`, `lsi-sw-raid` |
| SelectMemoryRasConfiguration | string | No | Memory RAS Configuration | Values: `platform-default`, `adddc-sparing`, `lockstep`, `maximum-performance`, `mirror-mode-1lm`, `sparing` |
| SelectPprType | string | No | Post Package Repair | Values: `platform-default`, `disabled`, `hard-ppr`, `soft-ppr` |
| SerialPortAenable | string | No | Serial Port A Enable | Values: `platform-default`, `disabled`, `enabled` |
| Sev | string | No | AMD SEV (Secure Encrypted Virtualization) | Values: `platform-default`, `Auto`, `253 ASIDs`, `509 ASIDs`, `disabled`, `enabled` |
| Slot10state | string | No | Slot 10 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot11state | string | No | Slot 11 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot12state | string | No | Slot 12 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot13state | string | No | Slot 13 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot14state | string | No | Slot 14 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot1state | string | No | Slot 1 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot2state | string | No | Slot 2 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot3state | string | No | Slot 3 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot4state | string | No | Slot 4 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot5state | string | No | Slot 5 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot6state | string | No | Slot 6 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot7state | string | No | Slot 7 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot8state | string | No | Slot 8 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| Slot9state | string | No | Slot 9 State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| SlotFrontNvme1linkSpeed | string | No | Front NVMe 1 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotFrontNvme1optionRom | string | No | Front NVMe 1 OptionROM | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| SlotFrontNvme2linkSpeed | string | No | Front NVMe 2 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotFrontNvme2optionRom | string | No | Front NVMe 2 OptionROM | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| SlotFrontNvme3linkSpeed | string | No | Front NVMe 3 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotFrontNvme4linkSpeed | string | No | Front NVMe 4 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotGpu1state | string | No | GPU Slot 1 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu2state | string | No | GPU Slot 2 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu3state | string | No | GPU Slot 3 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu4state | string | No | GPU Slot 4 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu5state | string | No | GPU Slot 5 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu6state | string | No | GPU Slot 6 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu7state | string | No | GPU Slot 7 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotGpu8state | string | No | GPU Slot 8 State | Values: `platform-default`, `disabled`, `enabled` |
| SlotHbaState | string | No | HBA Slot State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| SlotMlomState | string | No | Modular LOM State | Values: `platform-default`, `disabled`, `enabled` |
| SlotRaidState | string | No | RAID Slot State | Values: `platform-default`, `disabled`, `enabled`, `Legacy Only`, `UEFI Only` |
| SlotRearNvme1linkSpeed | string | No | Rear NVMe 1 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme2linkSpeed | string | No | Rear NVMe 2 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme3linkSpeed | string | No | Rear NVMe 3 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme4linkSpeed | string | No | Rear NVMe 4 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme5linkSpeed | string | No | Rear NVMe 5 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme6linkSpeed | string | No | Rear NVMe 6 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme7linkSpeed | string | No | Rear NVMe 7 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| SlotRearNvme8linkSpeed | string | No | Rear NVMe 8 Link Speed | Values: `platform-default`, `Auto`, `Disabled`, `GEN1`, `GEN2`, `GEN3`, `GEN4`, `GEN5` |
| Smee | string | No | SMEE (Secure Memory Encryption Enable) | Values: `platform-default`, `disabled`, `enabled` |
| SparingMode | string | No | Memory Sparing Mode | Values: `platform-default`, `dimm-sparing`, `rank-sparing` |
| SrIov | string | No | SR-IOV Support | Values: `platform-default`, `disabled`, `enabled` |
| StreamerPrefetch | string | No | DCU Streamer Prefetch | Values: `platform-default`, `disabled`, `enabled` |
| SvmMode | string | No | SVM Mode | Values: `platform-default`, `disabled`, `enabled` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TerminalType | string | No | Terminal Type | Values: `platform-default`, `pc-ansi`, `vt100`, `vt100-plus`, `vt-utf8` |
| TpmControl | string | No | TPM Control | Values: `platform-default`, `disabled`, `enabled` |
| TpmPendingOperation | string | No | TPM Pending Operation | Values: `platform-default`, `None`, `TpmClear` |
| TpmSupport | string | No | TPM Support | Values: `platform-default`, `disabled`, `enabled` |
| Tsme | string | No | TSME (Transparent Secure Memory Encryption) | Values: `platform-default`, `disabled`, `enabled` |
| TxtSupport | string | No | Intel TXT Support | Values: `platform-default`, `disabled`, `enabled` |
| UfsDisable | string | No | Uncore Frequency Scaling | Values: `platform-default`, `disabled`, `enabled` |
| UmaBasedClustering | string | No | UMA Based Clustering | Values: `platform-default`, `Disable (All2All)`, `Hemisphere (2-clusters)` |
| UpiLinkEnablement | string | No | UPI Link Enablement | Values: `platform-default`, `1`, `2`, `3`, `auto` |
| UsbEmul6064 | string | No | Port 60/64 Emulation | Values: `platform-default`, `disabled`, `enabled` |
| UsbPortFront | string | No | USB Port Front | Values: `platform-default`, `disabled`, `enabled` |
| UsbPortInternal | string | No | USB Port Internal | Values: `platform-default`, `disabled`, `enabled` |
| UsbPortKvm | string | No | USB Port KVM | Values: `platform-default`, `disabled`, `enabled` |
| UsbPortRear | string | No | USB Port Rear | Values: `platform-default`, `disabled`, `enabled` |
| UsbPortSdCard | string | No | USB Port SD Card | Values: `platform-default`, `disabled`, `enabled` |
| UsbPortVmedia | string | No | USB Port Virtual Media | Values: `platform-default`, `disabled`, `enabled` |
| UsbXhciSupport | string | No | XHCI Legacy Support | Values: `platform-default`, `disabled`, `enabled` |
| VirtualNuma | string | No | Virtual NUMA | Values: `platform-default`, `disabled`, `enabled` |
| VmdEnable | string | No | VMD Enable | Values: `platform-default`, `disabled`, `enabled` |
| VtForDirectedIo | string | No | Intel VT for Directed I/O | Values: `platform-default`, `disabled`, `enabled` |
| WorkloadConfiguration | string | No | Workload Configuration | Values: `platform-default`, `Balanced`, `IO Sensitive`, `NUMA Sparing` |
| XptPrefetch | string | No | XPT Prefetch | Values: `platform-default`, `Auto`, `disabled`, `enabled` |

**Example:**

```yaml
ObjectType: policies/bios
Name: example-bios-policy
Description: Example BIOS Policy policy for development environment
Organization: default
CpuPerformance: enterprise
CpuPowerManagement: performance
IntelHyperThreadingTech: enabled
IntelTurboBoostTech: enabled
IntelVirtualizationTechnology: enabled
ProcessorC1e: disabled
ProcessorC3report: disabled
ProcessorC6report: disabled
ExecuteDisableBit: enabled
EnergyEfficientTurbo: disabled
SelectMemoryRasConfiguration: maximum-performance
MemoryInterLeave: auto
ChannelInterLeave: auto
RankInterLeave: auto
DramClockThrottling: performance
MemoryBandwidthBoost: enabled
AdvancedMemTest: enabled
PatrolScrub: enabled
BootOptionRetry: enabled
Ipv4pxe: enabled
Ipv6pxe: disabled
NetworkStack: enabled
AllUsbDevices: enabled
LegacyUsbSupport: enabled
UsbEmul6064: enabled
SataModeSelect: ahci
PcieAriSupport: enabled
AspmSupport: Auto
Slot1state: enabled
Slot2state: enabled
SlotGpu1state: enabled
SlotFrontNvme1linkSpeed: Auto
SlotFrontNvme1optionRom: enabled
PcieSlotSsd1LinkSpeed: auto
PcieSlotSsd2LinkSpeed: auto
TxtSupport: enabled
VtForDirectedIo: enabled
IntelVtd: enabled
EnableSgx: enabled
SrIov: enabled
TpmControl: enabled
TpmSupport: enabled
LomPort0state: enabled
LomPort1state: enabled
ConsoleRedirection: enabled
SerialPortAenable: enabled
BaudRate: '115200'
TerminalType: vt100
OptimizedPowerMode: disabled
ConfigTdp: enabled
ClosedLoopThermThrotl: enabled
CiscoOpromLaunchOptimization: enabled
PciOptionRoMs: enabled
OsBootWatchdogTimer: disabled
CiscoDebugLevel: Normal
HardwarePrefetch: enabled
AdjacentCacheLinePrefetch: enabled
NumaOptimized: enabled
QpiSnoopMode: auto
AcsControlGpu1state: platform-default
AcsControlSlot11state: platform-default
Slot9state: enabled
Slot10state: enabled
SlotGpu5state: enabled
SlotGpu6state: disabled
SlotFrontNvme3linkSpeed: Auto
SlotRearNvme1linkSpeed: GEN4
CbsDfCmnMemIntlv: Auto
CbsCmnCpuGenDowncoreCtrl: Auto
CbsCmnGnbNbIommu: enabled
```

---

### Boot Order Policy

**Object Type:** `boot.PrecisionPolicy`
**Folder Path:** `policies/boot/`

**Description:**

Boot Order Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/boot` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| BootDevices | array | No | An array of boot devices that the system will attempt to boot from in order | - |
| ConfiguredBootMode | string | No | Sets the BIOS boot mode. UEFI uses the GUID Partition Table (GPT) whereas Legacy mode uses the Master Boot Record (MBR) partitioning scheme | Values: `Legacy`, `Uefi` |
| Description | string | No | Description of the policy | - |
| EnforceUefiSecureBoot | boolean | No | If UEFI secure boot is enabled, the boot mode is set to UEFI by default. Secure boot enforces signature verification of boot software | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/boot
Name: example-boot-order-policy
Description: Example Boot Order Policy policy for development environment
Organization: default
ConfiguredBootMode: Uefi
EnforceUefiSecureBoot: true
BootDevices:
- ObjectType: boot.LocalDisk
  Name: LocalDisk
  Enabled: true
  Bootloader:
    ObjectType: boot.Bootloader
    Name: BOOTx64.EFI
    Description: Default UEFI bootloader
    Path: \EFI\BOOT\BOOTx64.EFI
- ObjectType: boot.Pxe
  Name: PXE
  Enabled: true
  InterfaceName: MGMT-A
  IpType: IPv4
  Slot: MLOM
- ObjectType: boot.VirtualMedia
  Name: VirtualMedia
  Enabled: true
  Subtype: kvm-mapped-dvd
```

---

### Certificate Management Policy

**Object Type:** `certificatemanagement.Policy`
**Folder Path:** `policies/certificate/`

**Description:**

Certificate Management Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/certificate` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/certificate
Name: example-certificate-management-policy
Description: Example Certificate Management Policy policy for development environment
Organization: default
```

---

### Chassis Profile

**Object Type:** `chassis.Profile`
**Folder Path:** `profiles/chassis/`

**Description:**

Chassis Profile profiles for Cisco Intersight infrastructure management

**Dependencies:**

- `snmp.Policy`
- `access.Policy`
- `power.Policy`
- `organization.Organization`
- `thermal.Policy`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `profiles/chassis` |
| Name | string | Yes | Name of the profile | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AssignedChassis | reference | No | Reference to the equipment chassis assigned to this profile | - |
| Description | string | No | Description of the chassis profile | Max length: 1024 |
| ImcAccessPolicy | reference | No | A reference to an IMC Access Policy for chassis management access | - |
| Organization | string | Yes | Name of the organization | - |
| PowerPolicy | reference | No | A reference to a Power Policy for chassis power management | - |
| SnmpPolicy | reference | No | A reference to an SNMP Policy for chassis monitoring | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| ThermalPolicy | reference | No | A reference to a Thermal Policy for chassis cooling management | - |
| UserLabel | string | No | User label assigned to the chassis profile | Pattern: `^[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]*$`<br>Min length: 0<br>Max length: 64 |

**Example:**

```yaml
ObjectType: profiles/chassis
Name: example-chassis-profile
Description: Production chassis profile for data center operations
Organization: default
UserLabel: Production-Chassis-01
AssignedChassis: chassis-rack-1-1
ImcAccessPolicy: imc-access-production
PowerPolicy: high-performance-power
SnmpPolicy: datacenter-snmp
ThermalPolicy: quiet-thermal
```

---

### Scrub Policy

**Object Type:** `compute.ScrubPolicy`
**Folder Path:** `policies/scrub/`

**Description:**

Scrub Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/scrub` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| ScrubTargets | array | No | Target components to be cleared during scrub. Values: Disk, BIOS | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/scrub
Name: example-scrub-policy
Description: Example Scrub Policy policy for development environment
Organization: default
ScrubTargets:
- Disk
```

---

### Device Connector Policy

**Object Type:** `deviceconnector.Policy`
**Folder Path:** `policies/device_connector/`

**Description:**

Device Connector Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/device_connector` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| lockout_enabled | boolean | No | Enables configuration lockout on the endpoint | - |

**Example:**

```yaml
ObjectType: policies/device_connector
Name: example-device-connector-policy
Description: Example Device Connector Policy policy for development environment
Organization: default
lockout_enabled: true
```

---

### Ethernet Network Control Policy

**Object Type:** `fabric.EthNetworkControlPolicy`
**Folder Path:** `policies/ethernet_network_control/`

**Description:**

Ethernet Network Control Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ethernet_network_control` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| CdpEnabled | boolean | No | Enables the CDP on an interface | - |
| Description | string | No | Description of the policy | - |
| ForgeMac | string | No | Determines if the MAC forging is allowed or denied on an interface | Values: `allow`, `deny` |
| LldpSettings | object | No | LLDP settings for the Ethernet ports | - |
| MacRegistrationMode | string | No | Mac registration mode for the Ethernet ports | Values: `nativeVlanOnly`, `allVlans` |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| UplinkFailAction | string | No | Uplink Fail Action to take when uplink goes down | Values: `linkDown`, `warning` |

**Example:**

```yaml
ObjectType: policies/ethernet_network_control
Name: example-ethernet-network-control-policy
Description: Example Ethernet Network Control Policy policy for development environment
Organization: default
CdpEnabled: false
ForgeMac: allow
MacRegistrationMode: nativeVlanOnly
UplinkFailAction: linkDown
LldpSettings:
  ReceiveEnabled: true
  TransmitEnabled: true
```

---

### Ethernet Network Group Policy

**Object Type:** `fabric.EthNetworkGroupPolicy`
**Folder Path:** `policies/ethernet_network_group/`

**Description:**

Ethernet Network Group Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ethernet_network_group` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| VlanSettings | object | No | VLAN settings for the Ethernet Network Group Policy | - |

**Example:**

```yaml
ObjectType: policies/ethernet_network_group
Name: example-ethernet-network-group-policy
Description: Example Ethernet Network Group Policy policy for development environment
Organization: default
VlanSettings:
  NativeVlan: 1
  AllowedVlans: 100-200,300
```

---

### VLAN Policy

**Object Type:** `fabric.EthNetworkPolicy`
**Folder Path:** `policies/vlan/`

**Description:**

VLAN Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/vlan` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| VlanSettings | object | No | VLAN settings configuration | - |

**Example:**

```yaml
ObjectType: policies/vlan
Name: example-vlan-policy
Description: Example VLAN Policy policy for development environment
Organization: default
VlanSettings:
  NativeVlan: 1
  AllowedVlans: 100-200,300
```

---

### VSAN Policy

**Object Type:** `fabric.FcNetworkPolicy`
**Folder Path:** `policies/vsan/`

**Description:**

VSAN Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/vsan` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| EnableTrunking | boolean | No | Enable or Disable Trunking on all of configured FC uplink ports | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/vsan
Name: example-vsan-policy
Description: Example VSAN Policy policy for development environment
Organization: default
EnableTrunking: true
```

---

### FC Zone Policy

**Object Type:** `fabric.FcZonePolicy`
**Folder Path:** `policies/fc_zone/`

**Description:**

FC Zone Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/fc_zone` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| FcTargetMembers | array | No | List of FC target members for the zone policy | - |
| FcTargetZoningType | string | No | Type of FC zoning (SIST, SIMT, or None) | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/fc_zone
Name: example-fc-zone-policy
Description: Example FC Zone Policy policy for development environment
Organization: default
FcTargetMembers:
- Name: target-1
  Wwpn: 20:00:00:25:B5:00:01:00
```

---

### Flow Control Policy

**Object Type:** `fabric.FlowControlPolicy`
**Folder Path:** `policies/flow_control/`

**Description:**

Flow Control Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/flow_control` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| PriorityFlowControlMode | string | No | Priority Flow Control Mode for the port | Values: `on`, `off`, `auto` |
| ReceiveDirection | string | No | Link level Flow Control configured in the receive direction | Values: `Enabled`, `Disabled` |
| SendDirection | string | No | Link level Flow Control configured in the send direction | Values: `Enabled`, `Disabled` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/flow_control
Name: example-flow-control-policy
Description: Example Flow Control Policy policy for development environment
Organization: default
PriorityFlowControlMode: auto
ReceiveDirection: Disabled
SendDirection: Disabled
```

---

### Link Aggregation Policy

**Object Type:** `fabric.LinkAggregationPolicy`
**Folder Path:** `policies/link_aggregation/`

**Description:**

Link Aggregation Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/link_aggregation` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| LacpRate | string | No | Flag used to indicate whether LACP PDUs are to be sent fast, i.e., every 1 second | Values: `normal`, `fast` |
| Organization | string | Yes | Name of the organization | - |
| SuspendIndividual | boolean | No | Flag tells the switch whether to suspend the port if it does not receive LACP PDU | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/link_aggregation
Name: example-link-aggregation-policy
Description: Example Link Aggregation Policy policy for development environment
Organization: default
LacpRate: normal
SuspendIndividual: true
```

---

### Link Control Policy

**Object Type:** `fabric.LinkControlPolicy`
**Folder Path:** `policies/link_control/`

**Description:**

Link Control Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/link_control` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| UdldSettings | object | No | Unidirectional Link Detection (UDLD) Settings | - |

**Example:**

```yaml
ObjectType: policies/link_control
Name: example-link-control-policy
Description: Example Link Control Policy policy for development environment
Organization: default
UdldSettings:
  AdminState: Enabled
  Mode: normal
```

---

### Multicast Policy

**Object Type:** `fabric.MulticastPolicy`
**Folder Path:** `policies/multicast/`

**Description:**

Multicast Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/multicast` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| QuerierIpAddress | string | No | IP address of the IGMP querier used for IGMP snooping | - |
| QuerierState | string | No | Administrative state of the IGMP querier | Values: `Disabled`, `Enabled` |
| SnoopingState | string | No | Administrative state of the IGMP snooping | Values: `Disabled`, `Enabled` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/multicast
Name: example-multicast-policy
Description: Example Multicast Policy policy for development environment
Organization: default
QuerierIpAddress: 192.168.1.1
QuerierState: Disabled
SnoopingState: Enabled
```

---

### Port Policy

**Object Type:** `fabric.PortPolicy`
**Folder Path:** `policies/port/`

**Description:**

Port Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/port` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| DeviceModel | string | No | Model of the switch/fabric-interconnect for which the port policy is defined | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/port
Name: example-port-policy
Description: Example Port Policy policy for development environment
Organization: default
DeviceModel: UCS-FI-6454
```

---

### Switch Control Policy

**Object Type:** `fabric.SwitchControlPolicy`
**Folder Path:** `policies/switch_control/`

**Description:**

Switch Control Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/switch_control` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| EthernetSwitchingMode | string | No | Enable or Disable Ethernet End Host Switching Mode | Values: `end-host`, `switch` |
| FcSwitchingMode | string | No | Enable or Disable FC End Host Switching Mode | Values: `end-host`, `switch` |
| MacAgingSettings | object | No | MAC address aging timeout settings | - |
| Organization | string | Yes | Name of the organization | - |
| ReservedVlanStartId | integer | No | Starting VLAN ID for reserved VLAN range | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| VlanPortOptimizationEnabled | boolean | No | To enable or disable the VLAN port optimization | - |

**Example:**

```yaml
ObjectType: policies/switch_control
Name: example-switch-control-policy
Description: Example Switch Control Policy policy for development environment
Organization: default
EthernetSwitchingMode: end-host
FcSwitchingMode: end-host
ReservedVlanStartId: 3915
VlanPortOptimizationEnabled: false
MacAgingSettings:
  MacAgingOption: Default
  MacAgingTime: 14500
```

---

### Domain Profile

**Object Type:** `fabric.SwitchProfile`
**Folder Path:** `profiles/domain/`

**Description:**

Domain Profile profiles for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `profiles/domain` |
| Name | string | Yes | Name of the profile | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| ConfigChangeContext | object | No | Context information for configuration changes | - |
| ConfigChanges | object | No | Details of configuration changes | - |
| Description | string | No | Description of the profile | - |
| Organization | string | Yes | Name of the organization | - |
| SwitchClusterProfile | reference | No | Switch cluster profile associated with this domain profile | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| Type | string | No | Defines the type of the profile | Values: `instance`, `template` |

**Example:**

```yaml
ObjectType: profiles/domain
Name: example-domain-profile
Description: Example Domain Profile profile for development environment
Organization: default
Type: instance
```

---

### System QoS Policy

**Object Type:** `fabric.SystemQosPolicy`
**Folder Path:** `policies/system_qos/`

**Description:**

System QoS Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/system_qos` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Classes | array | No | List of system QoS classes | - |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/system_qos
Name: example-system-qos-policy
Description: Example System QoS Policy policy for development environment
Organization: default
Classes:
- AdminState: Enabled
  BandwidthPercent: 0
  Cos: 5
  Mtu: 2240
  MulticastOptimize: false
  Name: Platinum
  PacketDrop: false
  Weight: 10
- AdminState: Enabled
  BandwidthPercent: 0
  Cos: 4
  Mtu: 2240
  MulticastOptimize: false
  Name: Gold
  PacketDrop: true
  Weight: 9
- AdminState: Enabled
  BandwidthPercent: 0
  Cos: 2
  Mtu: 2240
  MulticastOptimize: false
  Name: Silver
  PacketDrop: true
  Weight: 8
- AdminState: Enabled
  BandwidthPercent: 0
  Cos: 1
  Mtu: 2240
  MulticastOptimize: false
  Name: Bronze
  PacketDrop: true
  Weight: 7
- AdminState: Enabled
  BandwidthPercent: 0
  Cos: 255
  Mtu: 2240
  MulticastOptimize: false
  Name: Best Effort
  PacketDrop: true
  Weight: 5
- AdminState: Enabled
  BandwidthPercent: 50
  Cos: 3
  Mtu: 2240
  MulticastOptimize: false
  Name: FC
  PacketDrop: false
  Weight: 5
```

---

### WWNN Pool

**Object Type:** `fcpool.Pool`
**Folder Path:** `pools/wwnn/`

**Description:**

WWNN Pool pools for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `pools/wwnn` |
| Name | string | Yes | Name of the pool | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the pool | - |
| IdBlocks | array | No | List of Identities in this pool | - |
| Organization | string | Yes | Name of the organization | - |
| PoolPurpose | string | No | Purpose of this pool, whether it is for WWPN or WWNN | Values: `WWPN`, `WWNN` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: pools/wwnn
Name: example-wwnn-pool
Description: Example WWNN Pool pool for development environment
Organization: default
PoolPurpose: WWNN
IdBlocks:
- From: 20:00:00:25:B5:01:00:00
  To: 20:00:00:25:B5:01:00:FF
  Size: 256
```

---

### Firmware Policy

**Object Type:** `firmware.Policy`
**Folder Path:** `policies/firmware/`

**Description:**

Firmware Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/firmware` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/firmware
Name: example-firmware-policy
Description: Example Firmware Policy policy for development environment
Organization: default
```

---

### Local User Policy

**Object Type:** `iam.EndPointUserPolicy`
**Folder Path:** `policies/local_user/`

**Description:**

Local User Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/local_user` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| EndPointUserRoles | array | No | List of local users to be configured | - |
| Organization | string | Yes | Name of the organization | - |
| PasswordProperties | object | No | Password properties for the local user policy | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/local_user
Name: example-local-user-policy
Description: Example Local User Policy policy for development environment
Organization: default
PasswordProperties:
  EnforceStrongPassword: true
  EnablePasswordExpiry: false
  PasswordExpiryDuration: 90
  PasswordHistory: 5
  NotificationPeriod: 15
  GracePeriod: 0
EndPointUserRoles:
- Name: admin
  Role: admin
  Enabled: true
```

---

### LDAP Policy

**Object Type:** `iam.LdapPolicy`
**Folder Path:** `policies/ldap/`

**Description:**

LDAP Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ldap` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| BaseProperties | object | No | Base settings of LDAP required while configuring LDAP policy | - |
| Description | string | No | Description of the policy | - |
| DnsParameters | object | No | Configuration settings to resolve LDAP servers, when DNS is enabled | - |
| EnableDns | boolean | No | Enables DNS to access LDAP servers | - |
| Enabled | boolean | No | LDAP server performs authentication | - |
| Groups | array | No | Array of LDAP group mappings | - |
| Organization | string | Yes | Name of the organization | - |
| Providers | array | No | Array of LDAP provider configurations | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| UserSearchPrecedence | string | No | Search precedence between local user database and LDAP user database | Values: `LocalUserDb`, `LDAPUserDb` |

**Example:**

```yaml
ObjectType: policies/ldap
Name: example-ldap-policy
Description: Example LDAP Policy policy for development environment
Organization: default
EnableDns: false
Enabled: true
UserSearchPrecedence: LocalUserDb
BaseProperties:
  class_id: iam.LdapBaseProperties
  object_type: iam.LdapBaseProperties
  base_dn: DC=example,DC=com
  bind_dn: CN=Administrator,CN=Users,DC=example,DC=com
  bind_method: ConfiguredCredentials
  domain: example.com
  enable_encryption: true
  enable_group_authorization: true
  enable_nested_group_search: false
  filter: sAMAccountName
  group_attribute: memberOf
  nested_group_search_depth: 128
  timeout: 0
DnsParameters:
  class_id: iam.LdapDnsParameters
  object_type: iam.LdapDnsParameters
  search_domain: example.com
  search_forest: example.com
  source: Extracted
Providers:
- class_id: iam.LdapProvider
  object_type: iam.LdapProvider
  server: ldap.example.com
  port: 636
  vendor: OpenLDAP
```

---

### IPMI Over LAN Policy

**Object Type:** `ipmioverlan.Policy`
**Folder Path:** `policies/ipmi/`

**Description:**

IPMI Over LAN Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ipmi` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/ipmi
Name: example-ipmi-over-lan-policy
Description: Example IPMI Over LAN Policy policy for development environment
Organization: default
```

---

### IP Pool

**Object Type:** `ippool.Pool`
**Folder Path:** `pools/ip/`

**Description:**

IP Pool pools for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `pools/ip` |
| Name | string | Yes | Name of the pool | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the pool | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: pools/ip
Name: example-ip-pool
Description: Example IP Pool pool for development environment
Organization: default
```

---

### IQN Pool

**Object Type:** `iqnpool.Pool`
**Folder Path:** `pools/iqn/`

**Description:**

IQN Pool pools for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `pools/iqn` |
| Name | string | Yes | Name of the pool | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the pool | - |
| IqnSuffixBlocks | array | No | Collection of IQN suffix blocks that define the IQN ranges | - |
| Organization | string | Yes | Name of the organization | - |
| Prefix | string | Yes | The prefix for any IQN blocks created for this pool. IQN Prefix must have the format "iqn.yyyy-mm.naming-authority" | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: pools/iqn
Name: example-iqn-pool
Description: Example IQN Pool pool for development environment
Organization: default
Prefix: iqn.2023-01.com.example
IqnSuffixBlocks:
- ObjectType: iqnpool.IqnSuffixBlock
  From: 1
  Size: 100
  Suffix: test.pool
```

---

### Virtual KVM Policy

**Object Type:** `kvm.Policy`
**Folder Path:** `policies/kvm/`

**Description:**

Virtual KVM Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/kvm` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/kvm
Name: example-virtual-kvm-policy
Description: Example Virtual KVM Policy policy for development environment
Organization: default
```

---

### MAC Pool

**Object Type:** `macpool.Pool`
**Folder Path:** `pools/mac/`

**Description:**

MAC Pool pools for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `pools/mac` |
| Name | string | Yes | Name of the pool | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AssignmentOrder | string | No | Assignment order decides the order in which the next identifier is allocated | Values: `sequential`, `default` |
| Description | string | No | Description of the pool | - |
| MacBlocks | array | No | Collection of MAC blocks that define the MAC address ranges | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: pools/mac
Name: example-mac-pool
Description: Example MAC Pool pool for development environment
Organization: default
AssignmentOrder: sequential
MacBlocks:
- ObjectType: macpool.Block
  From: 00:25:B5:00:00:01
  To: 00:25:B5:00:00:FF
```

---

### Persistent Memory Policy

**Object Type:** `memory.PersistentMemoryPolicy`
**Folder Path:** `policies/persistent_memory/`

**Description:**

Persistent Memory Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/persistent_memory` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Goals | array | No | List of persistent memory configuration goals | - |
| LocalSecurity | object | No | Local security settings for persistent memory | - |
| LogicalNamespaces | array | No | List of logical namespaces for persistent memory | - |
| ManagementMode | string | No | Management mode for the persistent memory policy | Values: `configured-from-intersight`, `configured-from-operating-system` |
| Organization | string | Yes | Name of the organization | - |
| RetainNamespaces | boolean | No | Persistent Memory Namespaces to be retained or not | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/persistent_memory
Name: example-persistent-memory-policy
Description: Example Persistent Memory Policy policy for development environment
Organization: default
ManagementMode: configured-from-intersight
RetainNamespaces: true
Goals:
- MemoryModePercentage: 0
  PersistentMemoryType: app-direct
  SocketId: All Sockets
LocalSecurity:
  Enabled: false
  SecurePassphrase: ''
```

---

### Memory Policy

**Object Type:** `memory.Policy`
**Folder Path:** `policies/memory/`

**Description:**

Memory Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/memory` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| EnableDimmBlocklisting | boolean | No | Enable DIMM Blocklisting on the server. This feature allows faulty DIMMs to be blocklisted and removed from system inventory | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/memory
Name: example-memory-policy
Description: Example Memory Policy policy for development environment
Organization: default
EnableDimmBlocklisting: true
```

---

### Network Configuration Policy

**Object Type:** `networkconfig.Policy`
**Folder Path:** `policies/network/`

**Description:**

Network Configuration Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/network` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/network
Name: example-network-configuration-policy
Description: Example Network Configuration Policy policy for development environment
Organization: default
```

---

### NTP Policy

**Object Type:** `ntp.Policy`
**Folder Path:** `policies/ntp/`

**Description:**

NTP Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ntp` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| authenticated_ntp_servers | array | No | Collection of authenticated NTP servers with respective Key Information | - |
| enabled | boolean | No | State of NTP service on the endpoint | - |
| ntp_servers | array | No | Collection of unauthenticated NTP server IP addresses or hostnames | - |
| timezone | string | No | Timezone of services on the endpoint | - |

**Example:**

```yaml
ObjectType: policies/ntp
Name: example-ntp-policy
Description: Example NTP Policy policy for development environment
Organization: default
enabled: true
ntp_servers:
- pool.ntp.org
- time.nist.gov
- 0.pool.ntp.org
authenticated_ntp_servers:
- class_id: ntp.AuthNtpServer
  object_type: ntp.AuthNtpServer
  server_name: secure-ntp.example.com
  key_type: SHA1
  sym_key_id: 1
  sym_key_value: secret-key-value
timezone: America/Los_Angeles
```

---

### Organization

**Object Type:** `organization.Organization`
**Folder Path:** `organizations/`

**Description:**

Organizations provide multi-tenancy within an account. Resources are associated to organizations using resource groups.

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `organizations/organization` |
| Name | string | Yes | The name of the organization | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | The informative description about the usage of this organization | - |
| ResourceGroups | array | No | Array of resource group names associated with this organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: organizations/organization
Name: my-organization
Description: Example organization for development environment
ResourceGroups:
- default-resource-group
- development-resources
```

---

### Power Policy

**Object Type:** `power.Policy`
**Folder Path:** `policies/power/`

**Description:**

Power Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/power` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AllocatedBudget | integer | No | Allocated power budget (0-65535 watts) | - |
| Description | string | No | Description of the policy | - |
| DynamicRebalancing | string | No | Dynamic power rebalancing | Values: `Enabled`, `Disabled` |
| ExtendedPowerCapacity | string | No | Extended power capacity | Values: `Enabled`, `Disabled` |
| Organization | string | Yes | Name of the organization | - |
| PowerPriority | string | No | Power priority level | Values: `Low`, `Medium`, `High` |
| PowerProfiling | string | No | Power profiling | Values: `Enabled`, `Disabled` |
| PowerRestoreState | string | No | Power restore state | Values: `AlwaysOff`, `AlwaysOn`, `LastState` |
| PowerSaveMode | string | No | Power save mode | Values: `Enabled`, `Disabled` |
| ProcessorPackagePowerLimit | string | No | Processor package power limit | Values: `Default`, `Maximum`, `Minimum` |
| RedundancyMode | string | No | Redundancy mode | Values: `Grid`, `NotRedundant`, `N+1`, `N+2` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/power
Name: example-power-policy
Description: Example Power Policy policy for development environment
Organization: default
AllocatedBudget: 800
DynamicRebalancing: Enabled
ExtendedPowerCapacity: Enabled
PowerPriority: Medium
PowerProfiling: Enabled
PowerRestoreState: LastState
PowerSaveMode: Enabled
ProcessorPackagePowerLimit: Default
RedundancyMode: N+1
```

---

### Resource Pool

**Object Type:** `resourcepool.Pool`
**Folder Path:** `pools/resource/`

**Description:**

Resource Pool pools for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `pools/resource` |
| Name | string | Yes | Name of the pool | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the pool | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: pools/resource
Name: example-resource-pool
Description: Example Resource Pool pool for development environment
Organization: default
```

---

### Server Pool Qualification Policy

**Object Type:** `resourcepool.QualificationPolicy`
**Folder Path:** `policies/server_pool_qualification/`

**Description:**

Server Pool Qualification Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/server_pool_qualification` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Qualifiers | array | No | Array of resource qualifiers for server qualification | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/server_pool_qualification
Name: example-server-pool-qualification-policy
Description: Example Server Pool Qualification Policy policy for development environment
Organization: default
Qualifiers:
- ClassId: resource.ServerQualifier
  ObjectType: resource.ServerQualifier
  Pids:
  - UCSC-C220-M5SX
  - UCSC-C240-M5SX
- ClassId: resource.ProcessorQualifier
  ObjectType: resource.ProcessorQualifier
  CpuCoresRange:
    ClassId: resource.CpuCoreRangeFilter
    ObjectType: resource.CpuCoreRangeFilter
    MinValue: 8
    MaxValue: 64
- ClassId: resource.MemoryQualifier
  ObjectType: resource.MemoryQualifier
  MemoryCapacityRange:
    ClassId: resource.MemoryCapacityRangeFilter
    ObjectType: resource.MemoryCapacityRangeFilter
    MinValue: 32
    MaxValue: 1024
```

---

### SD Card Policy

**Object Type:** `sdcard.Policy`
**Folder Path:** `policies/sdcard/`

**Description:**

SD Card Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/sdcard` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/sdcard
Name: example-sd-card-policy
Description: Example SD Card Policy policy for development environment
Organization: default
```

---

### Server Profile

**Object Type:** `server.Profile`
**Folder Path:** `profiles/server/`

**Description:**

Server Profile profiles for Cisco Intersight infrastructure management

**Dependencies:**

- `vmedia.Policy`
- `memory.PersistentMemoryPolicy`
- `deviceconnector.Policy`
- `vnic.SanConnectivityPolicy`
- `vnic.LanConnectivityPolicy`
- `organization.Organization`
- `sol.Policy`
- `networkconfig.Policy`
- `snmp.Policy`
- `storage.StoragePolicy`
- `boot.PrecisionPolicy`
- `syslog.Policy`
- `bios.Policy`
- `compute.ServerPowerPolicy`
- `adapter.ConfigPolicy`
- `ssh.Policy`
- `ntp.Policy`
- `power.Policy`
- `kvm.Policy`
- `access.Policy`
- `certificatemanagement.Policy`
- `iam.EndPointUserPolicy`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `profiles/server` |
| Name | string | Yes | Name of the profile | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AccessPolicy | reference | No | A reference to an Access Policy for server or chassis management options | - |
| AdapterConfigPolicy | reference | No | A reference to an Adapter Configuration Policy for Ethernet and Fibre-Channel settings | - |
| AssignedServer | reference | No | Reference to the compute server assigned to this profile | - |
| BiosPolicy | reference | No | A reference to a BIOS Policy for setting BIOS tokens on the endpoint | - |
| BootPrecisionPolicy | reference | No | A reference to a Boot Order Policy for reusable boot order configuration | - |
| CertificateManagementPolicy | reference | No | A reference to a Certificate Management Policy for certificate and private key configuration | - |
| ConfigChangeContext | object | No | Configuration change context information (read-only) | - |
| ConfigChanges | object | No | Configuration changes information (read-only) | - |
| Description | string | No | Description of the profile | - |
| DeviceConnectorPolicy | reference | No | A reference to a Device Connector Policy to control configuration changes from Cisco IMC | - |
| KvmPolicy | reference | No | A reference to a Virtual KVM Policy for KVM Launch settings | - |
| LanConnectivityPolicy | reference | No | A reference to a LAN Connectivity Policy for network resources and LAN connections | - |
| LocalUserPolicy | reference | No | A reference to a Local User Policy for creating local users on endpoints | - |
| NetworkConnectivityPolicy | reference | No | A reference to a Network Connectivity Policy for DNS settings and network configuration | - |
| NtpPolicy | reference | No | A reference to an NTP Policy to configure NTP Servers | - |
| Organization | string | Yes | Name of the organization | - |
| PersistentMemoryPolicy | reference | No | A reference to a Persistent Memory Policy for Persistent Memory configuration | - |
| PowerPolicy | reference | No | A reference to a Power Policy for power management settings | - |
| SanConnectivityPolicy | reference | No | A reference to a SAN Connectivity Policy for network storage resources and SAN connections | - |
| ServerPowerPolicy | reference | No | A reference to a Server Power Policy to determine power tasks during deploy/undeploy | - |
| SnmpPolicy | reference | No | A reference to an SNMP Policy to configure SNMP settings on endpoint | - |
| SolPolicy | reference | No | A reference to a Serial over LAN Policy | - |
| SshPolicy | reference | No | A reference to an SSH Policy for SSH configuration | - |
| StoragePolicy | reference | No | A reference to a Storage Policy for storage configuration | - |
| SyslogPolicy | reference | No | A reference to a Syslog Policy for syslog configuration | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| UserLabel | string | No | User label assigned to the server profile | Pattern: `^[ !#$%&\(\)\*\+,\-\./:;\?@\[\]_\{\|\}~a-zA-Z0-9]*$`<br>Min length: 0<br>Max length: 64 |
| VmediaPolicy | reference | No | A reference to a Virtual Media Policy for virtual media configuration | - |

**Example:**

```yaml
ObjectType: profiles/server
Name: example-server-profile
Description: Example Server Profile profile for development environment
Organization: default
UserLabel: Production-Server-01
AssignedServer: server-blade-1-1
AccessPolicy: imc-access-production
BiosPolicy: bios-virtualization-enabled
BootPrecisionPolicy: uefi-local-boot
LanConnectivityPolicy: dual-port-lan
SanConnectivityPolicy: dual-path-san
PowerPolicy: high-performance-power
SnmpPolicy: datacenter-snmp
StoragePolicy: raid-1-storage
```

---

### SMTP Policy

**Object Type:** `smtp.Policy`
**Folder Path:** `policies/smtp/`

**Description:**

SMTP Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/smtp` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/smtp
Name: example-smtp-policy
Description: Example SMTP Policy policy for development environment
Organization: default
```

---

### SNMP Policy

**Object Type:** `snmp.Policy`
**Folder Path:** `policies/snmp/`

**Description:**

SNMP Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/snmp` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/snmp
Name: example-snmp-policy
Description: Example SNMP Policy policy for development environment
Organization: default
```

---

### Serial Over LAN Policy

**Object Type:** `sol.Policy`
**Folder Path:** `policies/sol/`

**Description:**

Serial Over LAN Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/sol` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/sol
Name: example-serial-over-lan-policy
Description: Example Serial Over LAN Policy policy for development environment
Organization: default
```

---

### SSH Policy

**Object Type:** `ssh.Policy`
**Folder Path:** `policies/ssh/`

**Description:**

SSH Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ssh` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/ssh
Name: example-ssh-policy
Description: Example SSH Policy policy for development environment
Organization: default
```

---

### Drive Security Policy

**Object Type:** `storage.DriveSecurityPolicy`
**Folder Path:** `policies/drive_security/`

**Description:**

Drive Security Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/drive_security` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| KeySetting | object | No | Key details for supporting drive security | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/drive_security
Name: example-drive-security-policy
Description: Example Drive Security Policy policy for development environment
Organization: default
KeySetting:
  KeyType: Manual
  ManualKey:
    Passphrase: secure-passphrase-123
    IsPassphraseSet: true
```

---

### Storage Policy

**Object Type:** `storage.StoragePolicy`
**Folder Path:** `policies/storage/`

**Description:**

Storage Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/storage` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| DefaultDriveMode | string | No | All the drives that are not used in this policy, will move to the selected state | Values: `UnconfiguredGood`, `Jbod` |
| Description | string | No | Description of the policy | - |
| DiskGroupPolicies | array | No | List of disk group policies to be configured | - |
| DriveGroup | array | No | List of drive groups for RAID configuration | - |
| M2VirtualDrive | object | No | Virtual drive configuration for M.2 drives | - |
| Organization | string | Yes | Name of the organization | - |
| RaidController | object | No | RAID controller configuration | - |
| RetainPolicyVirtualDrives | boolean | No | Retains the virtual drives defined in policy as it is where it has not been modified by user | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| UnusedDisksState | string | No | State to which drives, not used in this policy, are set | Values: `UnconfiguredGood`, `Jbod`, `NoChange` |
| UseJbodForVdCreation | boolean | No | Disks would be moved to JBOD state first and then Virtual Drives would be created on the drives | - |
| VirtualDrives | array | No | List of virtual drives to be configured | - |

**Example:**

```yaml
ObjectType: policies/storage
Name: example-storage-policy
Description: Example Storage Policy policy for development environment
Organization: default
DefaultDriveMode: UnconfiguredGood
RetainPolicyVirtualDrives: true
UnusedDisksState: UnconfiguredGood
UseJbodForVdCreation: false
VirtualDrives:
- Name: VD0
  Size: 100
  ExpandToAvailable: false
  BootDrive: true
  VirtualDrivePolicy:
    AccessPolicy: Default
    DriveCache: Default
    ReadPolicy: Default
    StripSize: 64
    WritePolicy: Default
```

---

### Syslog Policy

**Object Type:** `syslog.Policy`
**Folder Path:** `policies/syslog/`

**Description:**

Syslog Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/syslog` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| LocalClients | array | No | Array of local syslog clients | - |
| Organization | string | Yes | Name of the organization | - |
| RemoteClients | array | No | Array of remote syslog clients | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/syslog
Name: example-syslog-policy
Description: Example Syslog Policy policy for development environment
Organization: default
```

---

### Thermal Policy

**Object Type:** `thermal.Policy`
**Folder Path:** `policies/thermal/`

**Description:**

Thermal Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/thermal` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| fan_control_mode | string | No | Sets the Fan Control Mode. High Power, Maximum Power and Acoustic modes are supported only on the Cisco UCS C-Series servers and on the X-Series Chassis. | Values: `Balanced`, `LowPower`, `HighPower`, `MaximumPower`, `Acoustic` |

**Example:**

```yaml
ObjectType: policies/thermal
Name: example-thermal-policy
Description: Example Thermal Policy policy for development environment
Organization: default
fan_control_mode: Balanced
```

---

### UUID Pool

**Object Type:** `uuidpool.Pool`
**Folder Path:** `pools/uuid/`

**Description:**

UUID Pool pools for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `pools/uuid` |
| Name | string | Yes | Name of the pool | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the pool | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: pools/uuid
Name: example-uuid-pool
Description: Example UUID Pool pool for development environment
Organization: default
```

---

### Virtual Media Policy

**Object Type:** `vmedia.Policy`
**Folder Path:** `policies/vmedia/`

**Description:**

Virtual Media Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/vmedia` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |

**Example:**

```yaml
ObjectType: policies/vmedia
Name: example-virtual-media-policy
Description: Example Virtual Media Policy policy for development environment
Organization: default
```

---

### Ethernet Adapter Policy

**Object Type:** `vnic.EthAdapterPolicy`
**Folder Path:** `policies/ethernet_adapter/`

**Description:**

Ethernet Adapter Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ethernet_adapter` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AdvancedFilter | boolean | No | Enables advanced filtering on the interface | - |
| ArfsSettings | object | No | Settings for Accelerated Receive Flow Steering to reduce the network latency and increase CPU cache efficiency | - |
| CompletionQueueSettings | object | No | Completion Queue resource settings | - |
| Description | string | No | Description of the policy | - |
| EtherChannelPinningEnabled | boolean | No | Enables EtherChannel Pinning to combine multiple physical links between two network switches into a single logical link | - |
| GeneveEnabled | boolean | No | GENEVE offload protocol allows you to create logical networks that span physical network boundaries | - |
| InterruptScaling | boolean | No | Enables Interrupt Scaling on the interface | - |
| InterruptSettings | object | No | Interrupt Settings for the virtual ethernet interface | - |
| Organization | string | Yes | Name of the organization | - |
| RssSettings | boolean | No | Receive Side Scaling allows the incoming traffic to be spread across multiple CPU cores | - |
| RxQueueSettings | object | No | Receive Queue resource settings | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TcpOffloadSettings | object | No | The TCP offload settings decide whether to offload the TCP related network functions from the CPU to the network hardware or not | - |
| TxQueueSettings | object | No | Transmit Queue resource settings | - |
| UplinkFailbackTimeout | integer | No | Uplink Failback Timeout in seconds when uplink failover is enabled for a vNIC | - |
| VxlanSettings | object | No | Virtual Extensible LAN Protocol Settings | - |

**Example:**

```yaml
ObjectType: policies/ethernet_adapter
Name: example-ethernet-adapter-policy
Description: Example Ethernet Adapter Policy policy for development environment
Organization: default
AdvancedFilter: false
EtherChannelPinningEnabled: false
GeneveEnabled: false
InterruptScaling: false
RssSettings: true
UplinkFailbackTimeout: 5
InterruptSettings:
  CoalescingTime: 125
  CoalescingType: MIN
  Count: 32
  Mode: MSIx
RxQueueSettings:
  Count: 4
  RingSize: 512
TxQueueSettings:
  Count: 4
  RingSize: 256
```

---

### Ethernet QoS Policy

**Object Type:** `vnic.EthQosPolicy`
**Folder Path:** `policies/ethernet_qos/`

**Description:**

Ethernet QoS Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/ethernet_qos` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Burst | integer | No | The burst traffic, in bytes, allowed on the vNIC | - |
| Cos | integer | No | Class of Service to be associated to the traffic on the virtual interface | - |
| Description | string | No | Description of the policy | - |
| Mtu | integer | No | The Maximum Transmission Unit (MTU) or packet size that the virtual interface accepts | - |
| Organization | string | Yes | Name of the organization | - |
| Priority | string | No | The priortiy matching the System QoS specified in the fabric profile | Values: `Best Effort`, `FC`, `Platinum`, `Gold`, `Silver`, `Bronze` |
| RateLimit | integer | No | The value in Mbps to use for limiting the data rate on the virtual interface | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TrustHostCos | boolean | No | Enables usage of the Class of Service provided by the operating system | - |

**Example:**

```yaml
ObjectType: policies/ethernet_qos
Name: example-ethernet-qos-policy
Description: Example Ethernet QoS Policy policy for development environment
Organization: default
Burst: 1024
Cos: 0
Mtu: 1500
Priority: Best Effort
RateLimit: 0
TrustHostCos: false
```

---

### Fibre Channel Adapter Policy

**Object Type:** `vnic.FcAdapterPolicy`
**Folder Path:** `policies/fibre_channel_adapter/`

**Description:**

Fibre Channel Adapter Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/fibre_channel_adapter` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| ErrorDetectionTimeout | integer | No | Error Detection Timeout, in milliseconds | - |
| ErrorRecoverySettings | object | No | Error Recovery Settings for the vHBA | - |
| FlogiSettings | object | No | Fibre Channel Fabric Login (FLOGI) Settings | - |
| InterruptSettings | object | No | Interrupt Settings for the vHBA | - |
| IoThrottleCount | integer | No | The maximum number of data or control I/O operations that can be pending for the virtual interface at one time | - |
| LunCount | integer | No | The maximum number of LUNs that the HBA can support | - |
| LunQueueDepth | integer | No | The number of commands that the HBA can send and receive in a single transmission per LUN | - |
| Organization | string | Yes | Name of the organization | - |
| PlogiSettings | object | No | Fibre Channel Port Login (PLOGI) Settings | - |
| ResourceAllocationTimeout | integer | No | Resource Allocation Timeout, in seconds | - |
| RxQueueSettings | object | No | Receive Queue Settings for the vHBA | - |
| ScsiQueueSettings | object | No | SCSI Queue Settings for the vHBA | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TxQueueSettings | object | No | Transmit Queue Settings for the vHBA | - |

**Example:**

```yaml
ObjectType: policies/fibre_channel_adapter
Name: example-fibre-channel-adapter-policy
Description: Example Fibre Channel Adapter Policy policy for development environment
Organization: default
ErrorDetectionTimeout: 2000
IoThrottleCount: 512
LunCount: 1024
LunQueueDepth: 20
ResourceAllocationTimeout: 10000
ErrorRecoverySettings:
  Enabled: false
  IoRetryCount: 8
  IoRetryTimeout: 5
  LinkDownTimeout: 30000
  PortDownTimeout: 10000
FlogiSettings:
  Retries: 8
  Timeout: 4000
PlogiSettings:
  Retries: 8
  Timeout: 20000
```

---

### Fibre Channel Network Policy

**Object Type:** `vnic.FcNetworkPolicy`
**Folder Path:** `policies/fibre_channel_network/`

**Description:**

Fibre Channel Network Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/fibre_channel_network` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| EnableTrunking | boolean | No | Enable or disable Trunking on all of configured FC uplink ports | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| VsanSettings | object | No | VSAN settings for the Fibre Channel Network Policy | - |

**Example:**

```yaml
ObjectType: policies/fibre_channel_network
Name: example-fibre-channel-network-policy
Description: Example Fibre Channel Network Policy policy for development environment
Organization: default
EnableTrunking: false
VsanSettings:
  DefaultVlan: 4048
  Id: 100
```

---

### iSCSI Adapter Policy

**Object Type:** `vnic.IscsiAdapterPolicy`
**Folder Path:** `policies/iscsi_adapter/`

**Description:**

iSCSI Adapter Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/iscsi_adapter` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| ConnectionTimeOut | integer | No | The number of seconds to wait until Cisco UCS assumes that the initial login has failed and the iSCSI adapter is unavailable | - |
| Description | string | No | Description of the policy | - |
| DhcpTimeout | integer | No | The number of seconds to wait before the initiator assumes that the DHCP server is unavailable | - |
| LunBusyRetryCount | integer | No | The number of times to retry the connection in case of a failure during iSCSI LUN discovery | - |
| Organization | string | Yes | Name of the organization | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TcpConnectionTimeOut | integer | No | The number of seconds to wait before the system decides that the TCP connection is lost | - |

**Example:**

```yaml
ObjectType: policies/iscsi_adapter
Name: example-iscsi-adapter-policy
Description: Example iSCSI Adapter Policy policy for development environment
Organization: default
ConnectionTimeOut: 15
DhcpTimeout: 60
LunBusyRetryCount: 15
TcpConnectionTimeOut: 15
```

---

### iSCSI Boot Policy

**Object Type:** `vnic.IscsiBootPolicy`
**Folder Path:** `policies/iscsi_boot/`

**Description:**

iSCSI Boot Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/iscsi_boot` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AutoTargetvendorName | string | No | Auto target interface that is represented via the Initiator name or the DHCP vendor ID | - |
| Chap | object | No | Challenge Handshake Authentication Protocol (CHAP) settings | - |
| Description | string | No | Description of the policy | - |
| InitiatorIpPool | reference | No | IP pool to be associated with the iSCSI vNIC | - |
| InitiatorIpSource | string | No | Source Type of Initiator IP Address - DHCP/Static/Pool | Values: `DHCP`, `Static`, `Pool` |
| InitiatorStaticIpV4Address | string | No | Static IPv4 address for iSCSI boot interface | - |
| InitiatorStaticIpV4Config | object | No | Static IP settings for the iSCSI boot interface | - |
| InitiatorStaticIpV6Address | string | No | Static IPv6 address for iSCSI boot interface | - |
| InitiatorStaticIpV6Config | object | No | Static IPv6 settings for the iSCSI boot interface | - |
| IscsiAdapterPolicy | reference | No | Reference to associated iSCSI Adapter Policy | - |
| IscsiIpType | string | No | IP type to be used for iSCSI communication | Values: `IPv4`, `IPv6` |
| MutualChap | object | No | Mutual Challenge Handshake Authentication Protocol (CHAP) settings | - |
| Organization | string | Yes | Name of the organization | - |
| PrimaryTargetPolicy | reference | No | The primary target policy associated with the iSCSI boot policy | - |
| SecondaryTargetPolicy | reference | No | The secondary target policy associated with the iSCSI boot policy | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TargetSourceType | string | No | Source Type of Targets that can be assigned to the iSCSI boot policy | Values: `Static`, `Auto` |

**Example:**

```yaml
ObjectType: policies/iscsi_boot
Name: example-iscsi-boot-policy
Description: Example iSCSI Boot Policy policy for development environment
Organization: default
TargetSourceType: Static
InitiatorIpSource: Static
IscsiIpType: IPv4
AutoTargetvendorName: ''
Chap:
  ClassId: vnic.IscsiAuthProfile
  ObjectType: vnic.IscsiAuthProfile
  IsPasswordSet: false
InitiatorStaticIpV4Address: 192.168.1.100
InitiatorStaticIpV4Config:
  ClassId: ippool.IpV4Config
  ObjectType: ippool.IpV4Config
  Gateway: 192.168.1.1
  Netmask: 255.255.255.0
  PrimaryDns: 8.8.8.8
  SecondaryDns: 8.8.4.4
```

---

### iSCSI Static Target Policy

**Object Type:** `vnic.IscsiStaticTargetPolicy`
**Folder Path:** `policies/iscsi_static_target/`

**Description:**

iSCSI Static Target Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/iscsi_static_target` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| IpAddress | string | No | The IPv4 address assigned to the iSCSI target | - |
| Lun | object | No | LUN information for the iSCSI target | - |
| Organization | string | Yes | Name of the organization | - |
| Port | integer | No | The port associated with the iSCSI target | - |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TargetName | string | No | Qualified Name (IQN) or Extended Unique Identifier (EUI) name of the iSCSI target | - |

**Example:**

```yaml
ObjectType: policies/iscsi_static_target
Name: example-iscsi-static-target-policy
Description: Example iSCSI Static Target Policy policy for development environment
Organization: default
IpAddress: 192.168.1.10
Port: 3260
TargetName: iqn.2010-11.com.example:storage.target01
Lun:
  Bootable: true
  LunId: 0
```

---

### LAN Connectivity Policy

**Object Type:** `vnic.LanConnectivityPolicy`
**Folder Path:** `policies/lan_connectivity/`

**Description:**

LAN Connectivity Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/lan_connectivity` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| AzureQosEnabled | boolean | No | Enables Azure Stack Host QOS on an adapter | - |
| Description | string | No | Description of the policy | - |
| IqnAllocationType | string | No | Allocation Type of iSCSI Qualified Name | Values: `None`, `Sequential`, `Pool` |
| IqnPool | reference | No | IQN pool to be associated with LAN Connectivity Policy | - |
| IqnStaticIdentifier | string | No | User provided static iSCSI Qualified Name (IQN) for use as initiator identifiers by iSCSI vNICs | - |
| Organization | string | Yes | Name of the organization | - |
| PlacementMode | string | No | The mode used for placement of vNICs on network adapters | Values: `custom`, `auto` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TargetPlatform | string | No | The platform for which the server profile is applicable | Values: `Standalone`, `FIAttached` |

**Example:**

```yaml
ObjectType: policies/lan_connectivity
Name: example-lan-connectivity-policy
Description: Example LAN Connectivity Policy policy for development environment
Organization: default
AzureQosEnabled: false
IqnAllocationType: None
PlacementMode: custom
TargetPlatform: FIAttached
```

---

### SAN Connectivity Policy

**Object Type:** `vnic.SanConnectivityPolicy`
**Folder Path:** `policies/san_connectivity/`

**Description:**

SAN Connectivity Policy policies for Cisco Intersight infrastructure management

**Dependencies:**

- `organization.Organization`

**Fields:**

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| ObjectType | string | Yes | The concrete type of this complex type | Format: `policies/san_connectivity` |
| Name | string | Yes | Name of the policy | Pattern: `^[a-zA-Z0-9_.:-]{1,64}$`<br>Min length: 1<br>Max length: 64 |
| Description | string | No | Description of the policy | - |
| Organization | string | Yes | Name of the organization | - |
| PlacementMode | string | No | The mode used for placement of vHBAs on network adapters | Values: `custom`, `auto` |
| Tags | array | No | An array of tags, which allow to add key, value meta-data to managed objects | - |
| TargetPlatform | string | No | The platform for which the server profile is applicable | Values: `Standalone`, `FIAttached` |
| WwnnAddressType | string | No | Type of allocation selected to assign a WWNN address for the server associated with the SAN Connectivity Policy | Values: `POOL`, `STATIC` |
| WwnnPool | reference | No | WWNN pool to be associated with SAN Connectivity Policy | - |
| WwnnStatic | string | No | The WWNN address for the server node must be in hexadecimal format xx:xx:xx:xx:xx:xx:xx:xx | - |

**Example:**

```yaml
ObjectType: policies/san_connectivity
Name: example-san-connectivity-policy
Description: Example SAN Connectivity Policy policy for development environment
Organization: default
PlacementMode: custom
TargetPlatform: FIAttached
WwnnAddressType: POOL
```

---

## Usage Examples

### Export Objects

Export all supported object types:
```bash
python export.py
```

Export specific object types:
```bash
python export.py --object-types organization.Organization,bios.Policy
```

### Import Objects

Import all YAML files:
```bash
python import.py
```

Import in safe mode (prevents deletions):
```bash
python import.py --safe-mode
```

Dry run to see what would be changed:
```bash
python import.py --dry-run
```

### Environment Configuration

Create a `.env` file with your Intersight credentials:

```bash
# Copy the example configuration
cp .env.example .env

# Edit with your credentials
vi .env
```

Required environment variables:

- `API_KEY`: Your Intersight API Key ID
- `API_SECRET`: Your Intersight API Secret Key (file path or key content)
- `IS_ENDPOINT`: Intersight API endpoint (default: https://intersight.com)

Optional environment variables:

- `FILES_DIR`: Directory for YAML files (default: ./files)
- `SAFE_MODE`: Prevent destructive operations (default: true)
- `LOG_LEVEL`: Logging level (default: INFO)
- `DEBUG`: Enable debug logging (default: false)

## Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify API_KEY and API_SECRET are correct
- Ensure the private key file is readable
- Check that the API key has sufficient permissions

**Validation Errors:**
- Check YAML syntax with `yamllint`
- Ensure required fields are present
- Verify field values match constraints

**Import Failures:**
- Check object dependencies are satisfied
- Verify referenced objects exist
- Review logs for detailed error messages

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
python export.py --debug
python import.py --debug
```

---

*Documentation generated by Intersight GitOps Tool on 2025-08-03 21:19:55*