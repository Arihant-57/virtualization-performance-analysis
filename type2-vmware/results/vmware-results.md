# VMware Workstation (Type-2) — Benchmark Results

## 1. Primary Empirical Measurements

The following measurements were recorded directly from the VMware Workstation Ubuntu VM terminal:

| Metric | Measured Value | Unit |
| :--- | :--- | :--- |
| **Total Execution Time** | `10.0002` | seconds |
| **Total Events Processed** | `10,381` | events |
| **Throughput (Events/sec)** | `1,037.93` | events/second |
| **Minimum Latency** | `0.94` | ms |
| **Average Latency** | `0.96` | ms |
| **Maximum Latency** | `3.30` | ms |
| **95th Percentile Latency** | `1.03` | ms |
| **Latency Sum** | `9,993.73` | ms |
| **Thread Events (avg/stddev)** | `10381.0000 / 0.00` | events |
| **Thread Time (avg/stddev)** | `9.9937 / 0.00` | seconds |

## 2. Terminal Transcript (Primary Run)

```text
sysbench 1.0.20 (using system LuaJIT 2.1.0-beta3)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time


Prime numbers limit: 20000

Initializing worker threads...

Threads started!

CPU speed:
    events per second:  1037.93

General statistics:
    total time:                          10.0002s
    total number of events:              10381

Latency (ms):
         min:                                    0.94
         avg:                                    0.96
         max:                                    3.30
         95th percentile:                        1.03
         sum:                                 9993.73

Threads fairness:
    events (avg/stddev):           10381.0000/0.00
    execution time (avg/stddev):   9.9937/0.00
```

## 3. Secondary Verification Run

An additional benchmark test was executed to evaluate repeatability on the hosted platform:

| Metric | Primary Run | Secondary Verification Run | Delta |
| :--- | :--- | :--- | :--- |
| **Throughput (Events/sec)** | `1,037.93` eps | `1,021.12` eps | -1.62% |
| **Total Events** | `10,381` events | `10,214` events | -167 events |
| **Total Time** | `10.0002` s | `10.0010` s | +0.0008 s |
| **Average Latency** | `0.96` ms | `0.98` ms | +0.02 ms |
| **95th Percentile Latency** | `1.03` ms | `1.10` ms | +0.07 ms |
| **Maximum Latency** | `3.30` ms | `3.67` ms | +0.37 ms |

## 4. Evidence References

- Primary Result Screenshot: [`06-vmware-sysbench-cpu.png`](../../docs/screenshots/type2-vmware/06-vmware-sysbench-cpu.png)
- Secondary Verification Run Screenshot: [`Type2_Sysbench_CPU_Benchmark.png`](../../docs/screenshots/type2-vmware/Type2_Sysbench_CPU_Benchmark.png)
