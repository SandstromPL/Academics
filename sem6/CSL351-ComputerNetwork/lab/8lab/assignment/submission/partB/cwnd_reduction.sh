#!/bin/bash

for algo in newreno highspeed veno vegas; do
  echo -n "TCP ${algo} cwnd reductions: "
  awk '$3 < $2 {count++} END {print count+0}' results/${algo}_cwnd.txt
done
