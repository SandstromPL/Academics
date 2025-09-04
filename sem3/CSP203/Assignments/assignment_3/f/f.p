set datafile separator ","
set term pdf
set output 'f_ouput.pdf'
set title 'All sales data product-wise'
set xlabel 'Products'
set ylabel 'Sales'
set key out top box
set style histogram columnstacked gap 2
set style data histogram
set boxwidth 0.6
set style fill solid
set xtics 1
set xtics rotate by -90
plot 'company_sales_data.csv' using 2:xtic(1) title columnheader(2),\
     ''using 3 title columnheader(3),\
     ''using 4 title columnheader(4),\
     ''using 5 title columnheader(5),\
     ''using 6 title columnheader(6),\
     ''using 7 title columnheader(7)
