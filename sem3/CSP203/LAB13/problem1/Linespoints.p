set terminal png
set output 'Linespoint.png'
set title 'Marks of Students in Various Courses'
set xlabel "Courses"
set ylabel "Marks"
set xtics rotate by 0
set grid
set style data linespoints

plot 'data.dat' using 2:xtic(1) title "Student1", \
     'data.dat' using 3:xtic(1) title "Student2", \
     'data.dat' using 4:xtic(1) title "Student3"

