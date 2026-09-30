# Proxmox VE (Type-1) — System Configuration

## 1. Node & Hypervisor Details

- **Hypervisor Platform:** Proxmox Virtual Environment (PVE)
- **Virtualization Core:** Linux KVM (Kernel-based Virtual Machine) / QEMU
- **Host Node Identifier:** `admin1-HP-Pro-Tower-280-G9-E-PCI-Desktop-PC`
- **Management Endpoint:** HTTPS Web Interface (`https://10.11.0.252:8006/`)
- **Virtual Machine ID:** VM 1228 (`arihant-cc-type1`)

## 2. Virtual Hardware Allocation

| Parameter | Allocated Specification | Status Inside Guest |
| :--- | :--- | :--- |
| **Virtual Cores (vCPU)** | 2 vCPUs | Verified via `lscpu` |
| **Memory (RAM)** | 2048 MB (2.0 GB) | Verified via `free -h` |
| **Virtual Storage** | 20 GB SCSI Volume | Verified via `df -h` |
| **Network Interface** | VirtIO Paravirtualized NIC | Bridged to `vmbr0` |
| **Display Device** | QEMU Standard VGA | Accessed via noVNC console |

## 3. Configuration Evidence

Photographic evidence of the Proxmox VE deployment and guest VM configuration:

- [Proxmox VE Cluster Dashboard](../../docs/screenshots/type1-proxmox/01-proxmox-dashboard.png)
- [VM 1228 Hardware Configuration](../../docs/screenshots/type1-proxmox/02-proxmox-vm-configuration.png)
- [Proxmox VM Running Status](../../docs/screenshots/type1-proxmox/03-proxmox-vm-running.png)
- [Ubuntu Guest noVNC Console](../../docs/screenshots/type1-proxmox/04-proxmox-ubuntu-console.png)
- [Guest System Configuration Inspection 1](../../docs/screenshots/type1-proxmox/05-01-proxmox-system-configuration.png)
- [Guest System Configuration Inspection 2](../../docs/screenshots/type1-proxmox/05-02-proxmox-system-configuration.png)
