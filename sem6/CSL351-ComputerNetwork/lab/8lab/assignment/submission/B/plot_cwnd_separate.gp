# Set terminal for a larger, high-quality PNG
set terminal pngcairo size 1200,800 enhanced font 'Verdana,10'
set output 'results/cwnd_comparison_improved.png'

# Create a 2x2 grid for the plots
set multiplot layout 2,2 title "TCP Congestion Window Dynamics (cwnd vs Time)" font ",16" offset 0,-1

# Common settings for all subplots to ensure fair comparison
set xlabel "Time (Seconds)"
set ylabel "Congestion Window (Bytes)"
set grid

# Set static ranges so all 4 graphs share the exact same scale
set xrange [0:20]
set yrange [0:30000]

# --- Plot 1: NewReno ---
set title "TCP NewReno" font ",12"
plot "results/newreno_cwnd.txt" using 1:3 with lines linecolor rgb "purple" linewidth 1.5 notitle

# --- Plot 2: HighSpeed ---
set title "TCP HighSpeed" font ",12"
plot "results/highspeed_cwnd.txt" using 1:3 with lines linecolor rgb "web-green" linewidth 1.5 notitle

# --- Plot 3: Veno ---
set title "TCP Veno" font ",12"
plot "results/veno_cwnd.txt" using 1:3 with lines linecolor rgb "royalblue" linewidth 1.5 notitle

# --- Plot 4: Vegas ---
set title "TCP Vegas" font ",12"
plot "results/vegas_cwnd.txt" using 1:3 with lines linecolor rgb "dark-orange" linewidth 1.5 notitle

unset multiplot
