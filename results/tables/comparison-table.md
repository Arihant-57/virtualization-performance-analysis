# Comparative Performance Tables

This document summarizes the quantitative performance metrics recorded from the identical Sysbench CPU benchmark workload ($20,000$ prime limit) executed on **Type-1 Proxmox VE / KVM** and **Type-2 VMware Workstation**.

---

## 1. Primary Benchmark Metrics Comparison

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Absolute Delta ($\Delta$) | Relative Variance (%) | Impact Summary |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Total Execution Time** | `10.0030 s` | `10.0002 s` | `+0.0028 s` | `+0.03%` | Nominal duration equivalent |
| **Total Events Processed** | `14,548` | `10,381` | `+4,167 events` | `+40.08%` | **Proxmox processed +40% more events** |
| **Throughput (Events/sec)** | `1,453.98 eps` | `1,037.93 eps` | `+416.05 eps` | `+40.08%` | **Proxmox delivered +40% throughput** |
| **Average Latency** | `0.69 ms` | `0.96 ms` | `-0.27 ms` | `-28.13%` | **Proxmox reduced latency by 28.1%** |
| **Throughput Speedup Factor** | `1.401x` | `1.000x` | `+0.401x` | `+40.08%` | Bare-metal execution efficiency |

---

## 2. Latency Distribution & Tail Latency Profile

| Latency Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Absolute Difference | Lower Latency Platform |
| :--- | :---: | :---: | :---: | :--- |
| **Minimum Latency ($L_{\min}$)** | `0.57 ms` | `0.94 ms` | `0.37 ms` | Proxmox VE (-39.36%) |
| **Average Latency ($L_{\text{avg}}$)** | `0.69 ms` | `0.96 ms` | `0.27 ms` | Proxmox VE (-28.13%) |
| **95th Percentile ($L_{p95}$)** | `0.74 ms` | `1.03 ms` | `0.29 ms` | Proxmox VE (-28.16%) |
| **Maximum Latency ($L_{\max}$)** | `1.24 ms` | `3.30 ms` | `2.06 ms` | Proxmox VE (-62.42%) |
| **Total Latency Sum** | `9,994.30 ms` | `9,993.73 ms` | `+0.57 ms` | Equivalent active CPU time |

> [!NOTE]
> The maximum latency recorded on VMware Workstation ($3.30\text{ ms}$) represents a **2.66× spike** relative to Proxmox VE's worst-case event ($1.24\text{ ms}$). This demonstrates the impact of hosted OS background scheduling interruptions and thread preemption.

---

## 3. Virtual Machine Resource Standardization Baseline

| Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Verification Method |
| :--- | :---: | :---: | :--- |
| **Guest OS Distribution** | Ubuntu 64-bit | Ubuntu 64-bit | `cat /etc/os-release` |
| **Assigned Virtual Cores** | 2 vCPUs | 2 vCPUs | `lscpu` |
| **Assigned Memory** | 2048 MB (2.0 GB) | 2048 MB (2.0 GB) | `free -h` |
| **Virtual Storage** | 20 GB | 20 GB | `df -h /` |
| **Benchmark Suite** | Sysbench 1.0.20 | Sysbench 1.0.20 | `sysbench --version` |
| **Computational Workload** | 20,000 Primes | 20,000 Primes | `--cpu-max-prime=20000` |
