#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Array of protocols to test and their corresponding ns-3 class names
declare -A variants=(
    ["newreno"]="TcpNewReno"
    ["highspeed"]="TcpHighSpeed"
    ["veno"]="TcpVeno"
    ["vegas"]="TcpVegas"
)

# Loop through each variant, run the simulation, and save outputs
for var_name in "${!variants[@]}"; do
    tcp_class="${variants[$var_name]}"
    echo "Running simulation for $tcp_class..."
    
    ./ns3 run "scratch/Demo_2 \
        --tcpVariant=$tcp_class \
        --cwndFile=results/${var_name}_cwnd.txt \
        --rttFile=results/${var_name}_rtt.txt \
        --ssthreshFile=results/${var_name}_ssthresh.txt \
        --pcapFile=results/${var_name}"
done

echo "All simulations complete. Check the 'results' directory."