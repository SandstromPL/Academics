import matplotlib.pyplot as plt
import numpy as np

# Data extracted directly from partA_terminal_out.txt
flows = ['Flow 1 (TCP\nn7->n4)', 'Flow 2 (TCP\nn2->n6)', 'Flow 3 (TCP\nn0->n3)', 'Flow 7 (UDP\nn1->n5)']
throughput_mbps = [1.04051, 1.04051, 0.521886, 0.280073]
lost_packets = [0, 0, 0, 0]

# Goodput Calculation
# TCP Total Size = 1024 (Payload) + 20 (IP Header) + 20 (TCP Header) = 1064 bytes
# UDP Total Size = 1024 (Payload) + 20 (IP Header) + 8 (UDP Header) = 1052 bytes
tcp_ratio = 1024 / 1064
udp_ratio = 1024 / 1052

goodput_mbps = [
    throughput_mbps[0] * tcp_ratio,
    throughput_mbps[1] * tcp_ratio,
    throughput_mbps[2] * tcp_ratio,
    throughput_mbps[3] * udp_ratio
]

# 1. Plot Flow vs Throughput
plt.figure(figsize=(8, 5))
plt.bar(flows, throughput_mbps, color=['blue', 'blue', 'blue', 'orange'])
plt.title('Flow vs Throughput')
plt.xlabel('Downlink Flows')
plt.ylabel('Throughput (Mbps)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('flow_vs_throughput.png')
plt.close()

# 2. Plot Flow vs Goodput
plt.figure(figsize=(8, 5))
plt.bar(flows, goodput_mbps, color=['green', 'green', 'green', 'red'])
plt.title('Flow vs Goodput')
plt.xlabel('Downlink Flows')
plt.ylabel('Goodput (Mbps)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('flow_vs_goodput.png')
plt.close()

# 3. Plot Flow vs Total Packets Lost
plt.figure(figsize=(8, 5))
plt.bar(flows, lost_packets, color='purple')
plt.title('Flow vs Total Packets Lost')
plt.xlabel('Downlink Flows')
plt.ylabel('Total Packets Lost')
plt.yticks(np.arange(0, 5, 1)) # Set y-axis to small integers since loss is 0
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('flow_vs_packets_lost.png')
plt.close()

print("Graphs successfully generated: 'flow_vs_throughput.png', 'flow_vs_goodput.png', and 'flow_vs_packets_lost.png'")
