#!/usr/bin/env python3
"""
Sysbench Output Parser
Project: Performance Analysis of Type-1 and Type-2 Hypervisors
Author: Arihant Narayankar

Parses Sysbench CPU benchmark logs and extracts quantitative metrics:
- Throughput (events per second)
- Total execution time (seconds)
- Total events processed
- Latency statistics: min, avg, max, 95th percentile, sum (milliseconds)
- Thread fairness statistics
"""

import sys
import re
import json
import argparse
from pathlib import Path

def parse_sysbench_text(content: str) -> dict:
    """Extracts benchmark metrics from standard Sysbench CPU output text."""
    metrics = {}
    
    # Extract prime limit
    m_prime = re.search(r"Prime numbers limit:\s*(\d+)", content)
    if m_prime:
        metrics["prime_limit"] = int(m_prime.group(1))

    # Extract thread count
    m_threads = re.search(r"Number of threads:\s*(\d+)", content)
    if m_threads:
        metrics["threads"] = int(m_threads.group(1))

    # Extract events per second (throughput)
    m_eps = re.search(r"events per second:\s*([\d\.]+)", content)
    if m_eps:
        metrics["events_per_sec"] = float(m_eps.group(1))

    # Extract total time
    m_time = re.search(r"total time:\s*([\d\.]+)s", content)
    if m_time:
        metrics["total_time_s"] = float(m_time.group(1))

    # Extract total number of events
    m_events = re.search(r"total number of events:\s*(\d+)", content)
    if m_events:
        metrics["total_events"] = int(m_events.group(1))

    # Extract latency metrics (ms)
    m_min = re.search(r"min:\s*([\d\.]+)", content)
    m_avg = re.search(r"avg:\s*([\d\.]+)", content)
    m_max = re.search(r"max:\s*([\d\.]+)", content)
    m_p95 = re.search(r"95th percentile:\s*([\d\.]+)", content)
    m_sum = re.search(r"sum:\s*([\d\.]+)", content)

    metrics["latency_ms"] = {
        "min": float(m_min.group(1)) if m_min else None,
        "avg": float(m_avg.group(1)) if m_avg else None,
        "max": float(m_max.group(1)) if m_max else None,
        "p95": float(m_p95.group(1)) if m_p95 else None,
        "sum": float(m_sum.group(1)) if m_sum else None,
    }

    return metrics

def main():
    parser = argparse.ArgumentParser(description="Parse Sysbench CPU benchmark output files.")
    parser.add_argument("log_files", nargs="*", help="Path(s) to sysbench log files.")
    parser.add_argument("--json", action="store_true", help="Print structured output as JSON.")
    args = parser.parse_args()

    # Default to repository's raw log files if none passed
    if not args.log_files:
        base_dir = Path(__file__).resolve().parent.parent
        default_files = [
            base_dir / "results" / "raw" / "proxmox_sysbench_output.txt",
            base_dir / "results" / "raw" / "vmware_sysbench_output.txt"
        ]
        args.log_files = [str(p) for p in default_files if p.exists()]

    if not args.log_files:
        print("No log files specified or found.")
        sys.exit(1)

    all_results = {}
    for log_path_str in args.log_files:
        path = Path(log_path_str)
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            continue
        content = path.read_text(encoding="utf-8")
        parsed = parse_sysbench_text(content)
        all_results[path.stem] = parsed

    if args.json:
        print(json.dumps(all_results, indent=2))
    else:
        print("=" * 80)
        print("                 SYSBENCH CPU BENCHMARK PARSER RESULTS                  ")
        print("=" * 80)
        for label, data in all_results.items():
            print(f"\n--- Benchmark Target: {label} ---")
            print(f"  Prime Limit       : {data.get('prime_limit', 'N/A')}")
            print(f"  Execution Time    : {data.get('total_time_s', 'N/A')} s")
            print(f"  Total Events      : {data.get('total_events', 'N/A'):,}")
            print(f"  Throughput        : {data.get('events_per_sec', 'N/A'):,.2f} events/sec")
            lats = data.get("latency_ms", {})
            print(f"  Latency (min/avg/95th/max): {lats.get('min')} / {lats.get('avg')} / {lats.get('p95')} / {lats.get('max')} ms")
        print("=" * 80)

if __name__ == "__main__":
    main()
