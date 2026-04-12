# Set terminal for a larger, high-quality PNG
set terminal pngcairo size 1200,800 enhanced font 'Verdana,10'
set output 'results/rtt_comparison_improved.png'

# Create a 2x2 grid for the plots
set multiplot layout 2,2 title "Round Trip Time (RTT) Dynamics per Algorithm" font ",16" offset 0,-1

# Common settings for all subplots
set xlabel "Time (Seconds)"
set ylabel "RTT (Seconds)"
set grid
set xrange [0:20]
set yrange [0:*]

# --- Plot 1: NewReno ---
set title "TCP NewReno" font ",12"
plot "results/newreno_rtt.txt" using 1:3 with lines linecolor rgb "purple" linewidth 1.5 notitle

# --- Plot 2: HighSpeed ---
set title "TCP HighSpeed" font ",12"
plot "results/highspeed_rtt.txt" using 1:3 with lines linecolor rgb "web-green" linewidth 1.5 notitle

# --- Plot 3: Veno ---
set title "TCP Veno" font ",12"
plot "results/veno_rtt.txt" using 1:3 with lines linecolor rgb "royalblue" linewidth 1.5 notitle

# --- Plot 4: Vegas ---
set title "TCP Vegas" font ",12"
plot "results/vegas_rtt.txt" using 1:3 with lines linecolor rgb "dark-orange" linewidth 1.5 notitle

unset multiplot
