set terminal pdf 
set output 'graph.pdf'
set title 'Experiment A'
set xlabel 'Time [s]'
set ylabel 'Length [m]'
set key out top box
set style data histograms
set style fill solid
plot 'data.dat' using 2:xtic(1) title "Colors"
