set datafile separator ","
set terminal pdf
set output "b_output.pdf"
set title "All Products"
set xlabel "Months"
set ylabel "Product"
set style data linespoints
set key out top box
plot 'company_sales_data.csv' u 1:2 title "Facecream" lt 5 lc "orange", \
     'company_sales_data.csv' u 1:3 title "Facewash" lt 5 lc "red", \
     'company_sales_data.csv' u 1:4 title "Toothpaste" lt 5 lc "green", \
     'company_sales_data.csv' u 1:5 title "Bathingsoap" lt 5 lc "blue", \
     'company_sales_data.csv' u 1:6 title "Shampoo" lt 5 lc "black", \
     'company_sales_data.csv' u 1:7 title "Moisturizer" lt 5 lc "pink"



