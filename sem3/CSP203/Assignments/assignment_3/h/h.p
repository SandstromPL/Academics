set datafile separator ","
set terminal pdf
set output "h_output.pdf"
set title "Top 3 Products with Highest Sales"
set xlabel "Month"
set ylabel "Sales"
set key left top
set grid
set style data linespoints

# Plot the sales data for the top 3 products: Bathing Soap, Toothpaste, and Shampoo
plot "company_sales_data.csv" using 1:5 title "Bathing Soap", \
     "" using 1:4 title "Toothpaste", \
     "" using 1:6 title "Shampoo"

