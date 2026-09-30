#!/usr/bin/env python3
"""
Hypervisor Performance Analysis & Statistical Comparison Engine
Project: Performance Analysis of Type-1 and Type-2 Hypervisors
Author: Arihant Narayankar

Processes raw Sysbench benchmark metrics and calculates:
- Throughput speedup & percentage differential
- Total event processing capacity differential
- Latency reduction factor and response time improvements
- Structured JSON output saved to results/processed/performance_summary.json
"""

import os
import csv
import json
from pathlib import Path

def analyze():
    base_dir = Path(__file__).resolve().parent.parent
    csv_path = base_dir / "results" / "raw" / "sysbench_results.csv"
    output_json = base_dir / "results" / "processed" / "performance_summary.json"
    output_json.parent.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV at {csv_path}")

    records = {}
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records[row["hypervisor"]] = {
                "type": row["type"],
                "total_time_s": float(row["total_time_s"]),
                "total_events": int(row["total_events"]),
                "events_per_sec": float(row["events_per_sec"]),
                "avg_latency_ms": float(row["avg_latency_ms"]),
            }

    t1 = records["Proxmox VE"]
    t2 = records["VMware Workstation"]

    # Comparative calculations
    eps_diff_abs = t1["events_per_sec"] - t2["events_per_sec"]
    eps_diff_pct = (eps_diff_abs / t2["events_per_sec"]) * 100.0

    events_diff_abs = t1["total_events"] - t2["total_events"]
    events_diff_pct = (events_diff_abs / t2["total_events"]) * 100.0

    time_diff_s = t1["total_time_s"] - t2["total_time_s"]

    lat_diff_abs = t2["avg_latency_ms"] - t1["avg_latency_ms"] # positive means t1 is lower
    lat_reduction_pct = (lat_diff_abs / t2["avg_latency_ms"]) * 100.0
    speedup_ratio = t1["events_per_sec"] / t2["events_per_sec"]

    summary = {
        "experiment_title": "Performance Analysis of Type-1 and Type-2 Hypervisors",
        "benchmark_workload": "sysbench cpu --cpu-max-prime=20000 run",
        "guest_os": "Ubuntu Linux",
        "vm_resources": {
            "vCPU": 2,
            "RAM_GB": 2,
            "virtual_disk_GB": 20
        },
        "empirical_measurements": {
            "proxmox_ve_type1": t1,
            "vmware_workstation_type2": t2
        },
        "comparative_analysis": {
            "throughput_difference_events_per_sec": round(eps_diff_abs, 2),
            "throughput_percentage_advantage_type1": round(eps_diff_pct, 2),
            "total_events_processed_differential": events_diff_abs,
            "total_events_percentage_differential": round(events_diff_pct, 2),
            "execution_time_delta_seconds": round(time_diff_s, 4),
            "average_latency_reduction_ms": round(lat_diff_abs, 3),
            "average_latency_reduction_percentage": round(lat_reduction_pct, 2),
            "throughput_speedup_factor": round(speedup_ratio, 3)
        }
    }

    with open(output_json, mode="w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Print formatted terminal report
    print("=" * 82)
    print("       HYPERVISOR COMPARATIVE PERFORMANCE ANALYSIS: TYPE-1 VS TYPE-2       ")
    print("=" * 82)
    print(f"{'Performance Metric':<28} | {'Proxmox VE (Type-1)':<18} | {'VMware Workstation':<18} | {'Variance / Delta':<12}")
    print("-" * 82)
    print(f"{'Total Execution Time':<28} | {t1['total_time_s']:<18.4f}s | {t2['total_time_s']:<18.4f}s | {time_diff_s:+.4f}s")
    print(f"{'Total Events Processed':<28} | {t1['total_events']:<18,d} | {t2['total_events']:<18,d} | {events_diff_abs:+d} ({eps_diff_pct:+.2f}%)")
    print(f"{'Throughput (Events/sec)':<28} | {t1['events_per_sec']:<18,.2f} | {t2['events_per_sec']:<18,.2f} | {eps_diff_abs:+,.2f} ({eps_diff_pct:+.2f}%)")
    print(f"{'Average Latency':<28} | {t1['avg_latency_ms']:<18.2f}ms | {t2['avg_latency_ms']:<18.2f}ms | -{lat_reduction_pct:.2f}% (Faster)")
    print(f"{'Throughput Speedup Factor':<28} | {speedup_ratio:<18.3f}x | 1.000x             | +{eps_diff_pct:.2f}%")
    print("=" * 82)
    print(f"[OK] Structured analysis successfully exported to: {output_json}")

if __name__ == "__main__":
    analyze()
