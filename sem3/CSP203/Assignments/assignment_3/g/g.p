set datafile separator ","
set terminal pdf
set output "g_output.pdf"
set title "shampoo VS moisturizer"
set style data histogram
set style histogram cluster gap 1
set style fill solid
set key out top box
set boxwidth 0.9
set xlabel "Month"
set ylabel "Sales"
plot "company_sales_data.csv" using 6:xtic(1) title "Shampoo" lt 5 lc "red",\
     "" using 7 title "Moisturizer" lt 5 lc "blue" 
