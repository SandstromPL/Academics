# Set terminal to generate a high-quality PNG
set terminal pngcairo size 1024,768 enhanced font 'Verdana,12'
set output 'results/cwnd_comparison.png'

# Titles and Labels
set title "TCP Congestion Window Dynamics (cwnd vs Time)" font ",16"
set xlabel "Time (Seconds)" font ",14"
set ylabel "Congestion Window (Bytes)" font ",14"

# Grid and Legend (Key)
set grid
set key bottom right box

# Plotting the data using Column 1 (Time) and Column 3 (New Cwnd)
plot "results/newreno_cwnd.txt" using 1:3 with lines linewidth 2 title "TCP NewReno", \
     "results/highspeed_cwnd.txt" using 1:3 with lines linewidth 2 title "TCP HighSpeed", \
     "results/veno_cwnd.txt" using 1:3 with lines linewidth 2 title "TCP Veno", \
     "results/vegas_cwnd.txt" using 1:3 with lines linewidth 2 title "TCP Vegas"
