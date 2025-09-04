set terminal png
set output 'Stacked_Histogram.png'
set title "Stacked Histogram of Marks"
set style data histogram
set style histogram rowstacked
set style fill solid border -1
set boxwidth 0.9
set xlabel "Courses"
set ylabel "Marks"
set key out top box
set xtics rotate by -45

plot 'data.dat' using 2:xtic(1) title "Student1", \
     'data.dat' using 3:xtic(1) title "Student2", \
     'data.dat' using 4:xtic(1) title "Student3"

