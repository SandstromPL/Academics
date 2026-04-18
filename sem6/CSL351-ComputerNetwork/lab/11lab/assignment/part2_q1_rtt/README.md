# Part 2 Q1: UDP RTT Measurement Tool

## Components
- `src/echo_server.c`: UDP echo server.
- `src/echo_client.c`: Configurable UDP client that measures RTT and packet loss.

## Build
```bash
make
```

## Run
Terminal 1:
```bash
./bin/echo_server 7000
```

Terminal 2:
```bash
./bin/echo_client 127.0.0.1 7000 20 128 200
```

Arguments for client:
1. `server_ip`
2. `port`
3. `num_packets`
4. `packet_size_bytes`
5. `interval_ms`

## Output
- Per packet: sequence number, bytes, RTT.
- Summary: sent, received, lost, loss percentage, average RTT.
