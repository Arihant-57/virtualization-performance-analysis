# Experimental Notes & Field Observations

This document captures low-level environmental notes, terminal observations, and technical commentary recorded during the execution of the hypervisor benchmark runs.

---

## 1. Environmental Audit & System Verification

### Proxmox VE (Type-1) Environment
- **Web UI & Management**: Proxmox VE 8.x web GUI accessed via secure HTTPS (`https://10.11.0.252:8006/`).
- **Node Identifier**: `admin1-HP-Pro-Tower-280-G9-E-PCI-Desktop-PC`.
- **VM Identifier**: VM 1228 (`arihant-cc-type1`).
- **VM Hardware Spec**:
  - Virtual CPU: 2 cores (KVM64 CPU type).
  - Virtual RAM: 2048 MB (2 GB) ballooning enabled.
  - Boot Disk: 20 GB SCSI/VirtIO storage volume.
  - Console Access: HTML5 noVNC terminal interface.
- **System Verification Inside Guest**:
  - Verified via console terminal `arihant@arihant-Standard-PC-i440FX-PIIX-1996`.
  - Kernel and memory reported 2.0 GB allocated with clean zero-swap utilization.

### VMware Workstation (Type-2) Environment
- **Application Environment**: VMware Workstation running on a multi-core host computer.
- **VM Identifier**: `Ubuntu 64-bit` (`arihant-VMware-Virtual-Platform`).
- **VM Hardware Spec**:
  - Processors: 2 Cores.
  - Memory: 2 GB (2048 MB).
  - Hard Disk: 20 GB (SCSI virtual disk).
  - Display & Graphics: Standard 3D acceleration enabled.
- **System Verification Inside Guest**:
  - Verified via terminal session `arihant@arihant-VMware-Virtual-Platform`.
  - `lscpu` command confirmed 2 virtual CPU sockets/threads.
  - `free -h` verified 1.9G available RAM.
  - `df -h` verified 20G virtual filesystem.

---

## 2. Benchmark Execution Observations

### Workload Invariance
Both systems executed the exact command:
```bash
sysbench cpu --cpu-max-prime=20000 run
```
Both benchmark instances ran under Sysbench version `1.0.20` using LuaJIT `2.1.0-beta3`. Both tests targeted a nominal 10-second sampling window.

### Observed Quantitative Metrics

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Direct Observation |
| :--- | :--- | :--- | :--- |
| **Duration** | 10.0030 s | 10.0002 s | Both terminated within 3 ms of target 10.0 s window |
| **Total Events** | 14,548 | 10,381 | Proxmox completed 4,167 more events (+40.08%) |
| **Throughput** | 1,453.98 eps | 1,037.93 eps | Proxmox achieved 416.05 eps higher throughput |
| **Average Latency** | 0.69 ms | 0.96 ms | Proxmox delivered 0.27 ms lower avg latency (28.13% faster) |
| **Minimum Latency** | 0.57 ms | 0.94 ms | Proxmox best-case event was 0.37 ms faster |
| **95th Percentile** | 0.74 ms | 1.03 ms | Proxmox tail latency remained well under 1.0 ms |
| **Maximum Latency** | 1.24 ms | 3.30 ms | VMware exhibited higher tail jitter (3.30 ms max spike) |

---

## 3. Secondary VMware Verification Run

In addition to the primary benchmark run documented above (1037.93 eps), a secondary benchmark verification run was performed on VMware Workstation, preserved in screenshot `Type2_Sysbench_CPU_Benchmark.png`:
- **Secondary Run Throughput**: 1,021.12 events/sec
- **Secondary Run Total Events**: 10,214 events
- **Secondary Run Avg Latency**: 0.98 ms
- **Secondary Run Max Latency**: 3.67 ms

This secondary run demonstrates high repeatability across VMware test cycles, with throughput remaining closely clustered around $\sim 1,020 - 1,038\text{ eps}$ and average latency holding steady at $\sim 0.96 - 0.98\text{ ms}$.

---

## 4. Architectural Analysis of the Performance Delta

The measured throughput advantage (+40.08%) and latency reduction (28.13%) observed in Proxmox VE can be attributed to several core virtualization mechanics:

1. **Direct Hardware Scheduling**:
   Under Proxmox VE (Type-1), the KVM kernel module acts directly as the hypervisor. Guest vCPUs are scheduled directly as kernel threads on the bare-metal Linux scheduler without an intervening user-space application supervisor.

2. **Absence of Host OS Contention**:
   In Type-2 virtualization (VMware Workstation), the hypervisor runs as a hosted process. The host operating system maintains its own GUI, background services, anti-virus monitors, and userland applications, introducing scheduling jitter and periodic thread preemption.

3. **VM Exit & Context Switching Overhead**:
   When a privileged instruction or timer interrupt triggers a VM Exit:
   - In Type-1: Control transfers directly to the bare-metal KVM hypervisor.
   - In Type-2: Control transfers to the VMware monitor process, which often requires interaction with the host OS kernel drivers before returning control to the VM.
