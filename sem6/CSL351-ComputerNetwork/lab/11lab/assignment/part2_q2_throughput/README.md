# Part 2 Q2: Throughput and Delay Measurement (iPerf-like)

## Components
- `src/echo_server.c`: UDP echo server.
- `src/echo_perf_client.c`: High-rate UDP echo client with 1-second throughput and delay windows.
- `plot_metrics.py`: Generates throughput and delay plots from CSV output.

## Build
```bash
make
```

## Run
Terminal 1:
```bash
./bin/echo_server 7100
```

Terminal 2:
```bash
./bin/echo_perf_client 127.0.0.1 7100 15 512 1000 results/run1
```

Create results directory if needed:
```bash
mkdir -p results
```

## CSV Outputs
- `results/run1_throughput.csv` -> `second,throughput_mbps`
- `results/run1_delay.csv` -> `second,avg_delay_ms`

## Generate Plots
```bash
python3 plot_metrics.py results/run1
```
Produces:
- `results/run1_throughput.png`
- `results/run1_delay.png`

## Notes
- Use lower interval and larger duration to stress throughput.
- Delay is computed as echo round-trip delay for replies received in each 1-second window.
