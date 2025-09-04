set terminal pdf
set output "e_output.pdf"
set title "Piechart"
set key out top box
set style fill solid 1.0 border -1
a1 = 0.123*360
a2 = a1+0.066*360
a3 = a2+0.249*360
a4 =a3+0.406*360
a5= a4+0.091*360
a6 = 360
set angles degree
set xrange[-1.5:1.5]
set yrange[-1.5:1.5]
set size square
set obj 1 circle arc [0:a1] fc rgb "red"
set obj 2 circle arc [a1:a2] fc rgb "orange"
set obj 3 circle arc [a2:a3] fc rgb "yellow"
set obj 4 circle arc [a3:a4] fc rgb "green"
set obj 5 circle arc [a4:a5] fc rgb "brown"
set obj 6 circle arc [a5:a6] fc rgb "blue"
set obj 1 circle at 0,0 size 1 front
set obj 2 circle at 0,0 size 1 front
set obj 3 circle at 0,0 size 1 front
set obj 4 circle at 0,0 size 1 front
set obj 5 circle at 0,0 size 1 front
set obj 6 circle at 0,0 size 1 front
plot NaN title 'Facecream' with lines lc rgb "red", \
     NaN title 'Facewash' with lines lc rgb "orange", \
     NaN title 'Toothpaste' with lines lc rgb "yellow", \
     NaN title 'Bathingsoap' with lines lc rgb "green", \
     NaN title 'Shampoo' with lines lc rgb "brown", \
     NaN title 'Moisturizer' with lines lc rgb "blue"




