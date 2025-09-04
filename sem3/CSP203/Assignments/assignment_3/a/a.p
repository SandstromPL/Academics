set datafile separator ","
set terminal pdf
set output "a_output.pdf"
set title "Total Monthly Profit"
set xlabel "Months"
set ylabel "Profit"
set style data linespoints
set grid
set key out top box
set xrange [0:12]
set yrange [0:500000]
plot 'company_sales_data.csv' u 9:xtic(1) lt 5 lc "blue" title "TP"

