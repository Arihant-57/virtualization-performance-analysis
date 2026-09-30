# Proxmox VE (Type-1) — Benchmark Results

## 1. Primary Empirical Measurements

The following measurements were recorded directly from the Proxmox VE Ubuntu VM console:

| Metric | Measured Value | Unit |
| :--- | :--- | :--- |
| **Total Execution Time** | `10.0030` | seconds |
| **Total Events Processed** | `14,548` | events |
| **Throughput (Events/sec)** | `1,453.98` | events/second |
| **Minimum Latency** | `0.57` | ms |
| **Average Latency** | `0.69` | ms |
| **Maximum Latency** | `1.24` | ms |
| **95th Percentile Latency** | `0.74` | ms |
| **Latency Sum** | `9,994.30` | ms |
| **Thread Events (avg/stddev)** | `14548.0000 / 0.00` | events |
| **Thread Time (avg/stddev)** | `9.9943 / 0.00` | seconds |

## 2. Terminal Transcript

```text
sysbench 1.0.20 (using system LuaJIT 2.1.0-beta3)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time


Prime numbers limit: 20000

Initializing worker threads...

Threads started!

CPU speed:
    events per second:  1453.98

General statistics:
    total time:                          10.0030s
    total number of events:              14548

Latency (ms):
         min:                                    0.57
         avg:                                    0.69
         max:                                    1.24
         95th percentile:                        0.74
         sum:                                 9994.30

Threads fairness:
    events (avg/stddev):           14548.0000/0.00
    execution time (avg/stddev):   9.9943/0.00
```

## 3. Evidence References

- Primary Result Screenshot: [`06-proxmox-sysbench-result.png`](../../docs/screenshots/type1-proxmox/06-proxmox-sysbench-result.png)
- Host Resource Monitoring:
  - [`07-01proxmox-resource-monitoring.png`](../../docs/screenshots/type1-proxmox/07-01proxmox-resource-monitoring.png)
  - [`07-02proxmox-resource-monitoring.png`](../../docs/screenshots/type1-proxmox/07-02proxmox-resource-monitoring.png)
  - [`07-03proxmox-resource-monitoring.png`](../../docs/screenshots/type1-proxmox/07-03proxmox-resource-monitoring.png)
  - [`07-04proxmox-resource-monitoring.png`](../../docs/screenshots/type1-proxmox/07-04proxmox-resource-monitoring.png)
