set terminal pdf 
set output 'graph.pdf'
set title 'Experiment A'
set xlabel 'Time [s]'
set ylabel 'Length [m]'
plot 'data.dat' with linespoints lt 15 lc "black" 
