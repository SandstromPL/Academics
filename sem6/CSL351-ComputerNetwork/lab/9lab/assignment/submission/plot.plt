# ==========================================
# NS-3 Trace File Plotter for TCP Assignment
# ==========================================

# Set terminal to output high-quality PNGs
set terminal pngcairo size 800,600 enhanced font 'Arial,11'
set grid

# Define the folder where your trace files are located. 
# Change this to "flow-4-Mixed/" or "flow-8-Paritosh/" as needed!
DIR = "flow-4-NewReno/"

# ------------------------------------------
# 1. Plot Congestion Window (cwnd)
# ------------------------------------------
set output DIR.'plot_cwnd.png'
set title 'Congestion Window (cwnd) over Time'
set xlabel 'Time (Seconds)'
set ylabel 'Congestion Window (Bytes)'
set key right bottom

# We use awk to filter by NodeList/0, NodeList/1, etc.
plot "< awk '$2 ~ /NodeList\\/0/' ".DIR."cwnd.tr" using 1:3 with lines lw 2 title "Flow 1 (Node 0)", \
     "< awk '$2 ~ /NodeList\\/1/' ".DIR."cwnd.tr" using 1:3 with lines lw 2 title "Flow 2 (Node 1)", \
     "< awk '$2 ~ /NodeList\\/2/' ".DIR."cwnd.tr" using 1:3 with lines lw 2 title "Flow 3 (Node 2)", \
     "< awk '$2 ~ /NodeList\\/3/' ".DIR."cwnd.tr" using 1:3 with lines lw 2 title "Flow 4 (Node 3)"

# ------------------------------------------
# 2. Plot Slow Start Threshold (ssthresh)
# ------------------------------------------
set output DIR.'plot_ssthresh.png'
set title 'Slow Start Threshold (ssthresh) over Time'
set xlabel 'Time (Seconds)'
set ylabel 'ssthresh (Bytes)'
set key right top

plot "< awk '$2 ~ /NodeList\\/0/' ".DIR."ssthresh.tr" using 1:3 with lines lw 2 title "Flow 1 (Node 0)", \
     "< awk '$2 ~ /NodeList\\/1/' ".DIR."ssthresh.tr" using 1:3 with lines lw 2 title "Flow 2 (Node 1)", \
     "< awk '$2 ~ /NodeList\\/2/' ".DIR."ssthresh.tr" using 1:3 with lines lw 2 title "Flow 3 (Node 2)", \
     "< awk '$2 ~ /NodeList\\/3/' ".DIR."ssthresh.tr" using 1:3 with lines lw 2 title "Flow 4 (Node 3)"

# ------------------------------------------
# 3. Plot Round Trip Time (RTT)
# ------------------------------------------
set output DIR.'plot_rtt.png'
set title 'Round Trip Time (RTT) over Time'
set xlabel 'Time (Seconds)'
set ylabel 'RTT (Seconds)'
set key right top

plot "< awk '$2 ~ /NodeList\\/0/' ".DIR."rtt.tr" using 1:3 with lines lw 2 title "Flow 1 (Node 0)", \
     "< awk '$2 ~ /NodeList\\/1/' ".DIR."rtt.tr" using 1:3 with lines lw 2 title "Flow 2 (Node 1)", \
     "< awk '$2 ~ /NodeList\\/2/' ".DIR."rtt.tr" using 1:3 with lines lw 2 title "Flow 3 (Node 2)", \
     "< awk '$2 ~ /NodeList\\/3/' ".DIR."rtt.tr" using 1:3 with lines lw 2 title "Flow 4 (Node 3)"

print "Plots generated successfully in ".DIR
