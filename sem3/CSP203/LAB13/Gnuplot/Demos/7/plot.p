set terminal pdf 
set output 'graph.pdf'
set title 'Immigration Data'
set xlabel 'Year Range'
set ylabel 'Population'
set key out top box
set style data histograms
set style fill solid
set xtics rotate 90
plot 'immigration.dat' using 2:xtic(1) ti col lc "blue" ,'' using 3:xtic(1) lc "green" ti col ,'' using 4:xtic(1) ti col lc "red"
