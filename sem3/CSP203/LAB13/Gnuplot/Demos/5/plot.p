set terminal pdf 
set output 'graph.pdf'
set title 'Experiment A'
set xlabel 'Time [s]'
set ylabel 'Length [m]'

set key out top box
set xrange [0:7]
set yrange [0:8]
set xtics 2
set ytics 3
plot 'data.dat' with linespoints lt 5 lc "blue"
