#!/usr/bin/env bash
# ==============================================================================
# Sysbench CPU Benchmark Automation Script
# Project: Performance Analysis of Type-1 and Type-2 Hypervisors
# Author: Arihant Narayankar
# ==============================================================================

set -euo pipefail

# Output configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
HOSTNAME_STR=$(hostname)
OUTPUT_DIR="${1:-./benchmark_logs}"
OUTPUT_FILE="${OUTPUT_DIR}/sysbench_cpu_${HOSTNAME_STR}_${TIMESTAMP}.log"

mkdir -p "${OUTPUT_DIR}"

echo "======================================================================" | tee "${OUTPUT_FILE}"
echo "    CLOUD COMPUTING EXPERIMENTAL BENCHMARK: SYSBENCH CPU             " | tee -a "${OUTPUT_FILE}"
echo "======================================================================" | tee -a "${OUTPUT_FILE}"
echo "Execution Timestamp : $(date -u +"%Y-%m-%d %H:%M:%S UTC")" | tee -a "${OUTPUT_FILE}"
echo "Node / Hostname     : ${HOSTNAME_STR}" | tee -a "${OUTPUT_FILE}"
echo "Kernel Release      : $(uname -r)" | tee -a "${OUTPUT_FILE}"
echo "Architecture        : $(uname -m)" | tee -a "${OUTPUT_FILE}"
echo "----------------------------------------------------------------------" | tee -a "${OUTPUT_FILE}"

echo -e "\n[1/3] Collecting Hardware & Environmental Specifications..." | tee -a "${OUTPUT_FILE}"
echo "--- CPU Configuration (lscpu) ---" | tee -a "${OUTPUT_FILE}"
lscpu | grep -E "Model name|CPU\(s\)|Thread\(s\) per core|Core\(s\) per socket|Socket\(s\)|Architecture|CPU MHz" | tee -a "${OUTPUT_FILE}" || true

echo -e "\n--- Memory Allocation (free -h) ---" | tee -a "${OUTPUT_FILE}"
free -h | tee -a "${OUTPUT_FILE}"

echo -e "\n--- Disk Allocation (df -h /) ---" | tee -a "${OUTPUT_FILE}"
df -h / | tee -a "${OUTPUT_FILE}"

echo -e "\n[2/3] Verifying / Installing Sysbench Benchmark Suite..." | tee -a "${OUTPUT_FILE}"
if ! command -v sysbench &> /dev/null; then
    echo "Sysbench not found. Installing via apt-get..." | tee -a "${OUTPUT_FILE}"
    sudo apt-get update -y
    sudo apt-get install -y sysbench
fi

SYSBENCH_VER=$(sysbench --version)
echo "Sysbench Engine Version: ${SYSBENCH_VER}" | tee -a "${OUTPUT_FILE}"

echo -e "\n[3/3] Executing Standardized CPU Benchmark..." | tee -a "${OUTPUT_FILE}"
echo "Command: sysbench cpu --cpu-max-prime=20000 run" | tee -a "${OUTPUT_FILE}"
echo "----------------------------------------------------------------------" | tee -a "${OUTPUT_FILE}"

# Standardized benchmark workload
sysbench cpu --cpu-max-prime=20000 run | tee -a "${OUTPUT_FILE}"

echo "----------------------------------------------------------------------" | tee -a "${OUTPUT_FILE}"
echo "Benchmark completed successfully." | tee -a "${OUTPUT_FILE}"
echo "Full execution log captured at: ${OUTPUT_FILE}" | tee -a "${OUTPUT_FILE}"
echo "======================================================================" | tee -a "${OUTPUT_FILE}"
