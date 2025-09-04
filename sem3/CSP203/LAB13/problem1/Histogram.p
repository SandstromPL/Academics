set terminal png
set output 'Histogram.png'
set title "Marks of Students in Various Courses"
set style data histogram
set style histogram cluster gap 1
set style fill solid 
set boxwidth 0.9
set xlabel "Courses"
set ylabel "Marks"
set key out top box
set xtics rotate by -45

plot 'data.dat' using 2:xtic(1) title "Student1", \
     'data.dat' using 3:xtic(1) title "Student2", \
     'data.dat' using 4:xtic(1) title "Student3"

