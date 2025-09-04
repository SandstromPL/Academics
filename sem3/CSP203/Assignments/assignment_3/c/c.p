set datafile separator ","
set terminal pdf
set output "c_output.pdf"
set title "Facecream"
set xlabel "Months"
set ylabel "Sales"
set style data histograms
set style histogram cluster gap 1
set style fill solid
set key out top box
plot 'company_sales_data.csv' using 2:xtic(1) title "Facecream" lt 5 lc "red"
