# Part 2 Q3: Traceroute-like Tool in C

## Components
- `src/traceroute.c`: Sends UDP probes with increasing TTL and receives ICMP via raw socket.

## Build
```bash
make
```

## Run
Raw ICMP socket requires elevated privileges:
```bash
sudo ./bin/traceroute 8.8.8.8
```

Optional arguments:
```bash
sudo ./bin/traceroute <destination> [max_hops] [timeout_ms]
```

Examples:
```bash
sudo ./bin/traceroute 127.0.0.1 10 500
sudo ./bin/traceroute iitbhilai.ac.in 30 1000
```

## Behavior
- 3 probes per hop.
- Prints `*` when timeout occurs.
- Stops when destination is reached (ICMP port unreachable from destination) or max hops exceeded.
