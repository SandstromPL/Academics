set terminal pdf
set output "d_ouput.pdf"


set title "Monthly Sales of Top Product"
set xlabel "Month Number"
set ylabel "Sales"


set grid
set key out top box
plot "temp1.dat" using 1:2 with linespoints title "Bathing Soap"
