#!/bin/bash

# Parameterübergabe: Dateiname
filename="$1"

# Gnuplot:
gnuplot << EOF


# Setzen des Trennzeichens für die Daten
set datafile separator ";"

# Definition der Funktion
f(x) = a + b * x**c

# Einlesen des Dateinamens als Parameter
filename = "${filename}"


# Anpassung der Funktionen an die Daten
fit f(x) filename every ::1 using 1:2 via a, b, c


# Plotten der Daten und der Funktion
fontsize = 16
set term png
set output "plot_${filename}.png"
set ylabel "Laufzeit [s]" font sprintf(",%d", fontsize)
set xlabel "Permutationgsgruppe (Eingabe)" font sprintf(",%d", fontsize)

set terminal png size 800,500 font ",fontsize"

set key inside left top box spacing 1.5

plot filename every ::1 using 1:2 with points pt 2 ps 2 linewidth 3 \
      title "Mittelwerte versch. Messungen und Rechner" \
     , f(x) with lines linewidth 3 title sprintf("%.3f + %.3f * x^{%.3f}", a, b, c) \


set output

EOF
rm fit.log

