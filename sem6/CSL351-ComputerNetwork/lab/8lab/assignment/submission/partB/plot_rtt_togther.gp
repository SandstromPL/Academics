# Set terminal to generate a high-quality PNG
set terminal pngcairo size 1024,768 enhanced font 'Verdana,12'
set output 'results/rtt_comparison.png'

# Titles and Labels
set title "Round Trip Time (RTT) Dynamics" font ",16"
set xlabel "Time (Seconds)" font ",14"
set ylabel "RTT (Seconds)" font ",14"

# Grid and Legend (Key)
set grid
set key top right box

# Ensure Y-axis starts at 0 for accurate perspective
set yrange [0:*]

# Plotting the data using Column 1 (Time) and Column 3 (New RTT)
plot "results/newreno_rtt.txt" using 1:3 with lines linewidth 2 title "TCP NewReno", \
     "results/highspeed_rtt.txt" using 1:3 with lines linewidth 2 title "TCP HighSpeed", \
     "results/veno_rtt.txt" using 1:3 with lines linewidth 2 title "TCP Veno", \
     "results/vegas_rtt.txt" using 1:3 with lines linewidth 2 title "TCP Vegas"
