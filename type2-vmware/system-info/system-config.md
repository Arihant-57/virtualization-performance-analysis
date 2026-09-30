# VMware Workstation (Type-2) — System Configuration

## 1. Hypervisor & Environment Details

- **Hypervisor Platform:** VMware Workstation
- **Virtualization Core:** Hosted Type-2 Virtual Machine Monitor (VMM)
- **Host Operating System:** Windows 64-bit multi-tasking host
- **Virtual Machine Name:** `Ubuntu 64-bit` (`arihant-VMware-Virtual-Platform`)

## 2. Virtual Hardware Allocation

| Parameter | Allocated Specification | Status Inside Guest |
| :--- | :--- | :--- |
| **Virtual Cores (vCPU)** | 2 Cores | Verified via `lscpu` |
| **Memory (RAM)** | 2048 MB (2.0 GB) | Verified via `free -h` |
| **Virtual Storage** | 20 GB Virtual SCSI Disk | Verified via `df -h /` |
| **Network Interface** | VMware Virtual NIC (NAT) | Active |
| **Display Device** | VMware SVGA 3D | Standard console |

## 3. Configuration Evidence

Photographic evidence of the VMware Workstation configuration and guest system audits:

- [VMware VM Hardware Settings](../../docs/screenshots/type2-vmware/01-vmware-vm-configuration.png)
- [VMware VM Running State](../../docs/screenshots/type2-vmware/02-vmware-vm-running.png)
- [Guest CPU Topology (`lscpu` Part 1)](../../docs/screenshots/type2-vmware/03-vmware-lscpu--01--.png)
- [Guest CPU Topology (`lscpu` Part 2)](../../docs/screenshots/type2-vmware/03-vmware-lscpu--02--.png)
- [Guest Memory Audit (`free -h`)](../../docs/screenshots/type2-vmware/04-vmware-memory.png)
- [Guest Filesystem Storage (`df -h`)](../../docs/screenshots/type2-vmware/05-vmware-disk.png)
