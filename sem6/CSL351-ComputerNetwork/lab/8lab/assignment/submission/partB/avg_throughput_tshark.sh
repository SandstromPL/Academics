#!/bin/bash

for algo in newreno highspeed veno vegas; do
  echo -n "TCP ${algo} Average Throughput: "
  tshark -r results/${algo}-1-0.pcap -Y "tcp.dstport == 8080" -T fields -e frame.len 2>/dev/null |
  awk '{sum+=$1} END {printf "%.3f Mbps\n", (sum*8)/(19*1000000)}'
done
