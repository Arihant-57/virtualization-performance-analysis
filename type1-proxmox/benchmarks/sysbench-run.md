# Proxmox VE (Type-1) — Sysbench Benchmark Procedure

## 1. Execution Procedure

Inside the Ubuntu virtual machine on Proxmox VE (`arihant@arihant-Standard-PC-i440FX-PIIX-1996`):

1. **Verify Packages**:
   Ensure `sysbench` is installed:
   ```bash
   sudo apt update
   sudo apt install sysbench -y
   ```

2. **Verify Version**:
   ```bash
   sysbench --version
   ```
   *Output recorded:* `sysbench 1.0.20 (using system LuaJIT 2.1.0-beta3)`

3. **Execute Benchmark**:
   ```bash
   sysbench cpu --cpu-max-prime=20000 run
   ```

## 2. Test Parameters

- **Prime numbers limit:** 20,000
- **Threads:** 1 worker thread
- **Random Number Generator:** Initialized from system time
- **Duration:** Fixed 10-second sampling window
- **Measured Metrics:** CPU throughput (events/sec), total events, latency distribution (min, avg, 95th percentile, max)
