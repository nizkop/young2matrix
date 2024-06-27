#!/bin/bash

# Parameterübergabe: Dateiname
filename="$1"

# Gnuplot:
gnuplot << EOF


# Setzen des Trennzeichens für die Daten
set datafile separator ";"

# Definition der Funktion
f(x) = a + b * x

# Einlesen des Dateinamens als Parameter
filename = "${filename}"


# Anpassung der Funktionen an die Daten
fit f(x) filename every ::1 using 1:2 via a, b


# Plotten der Daten und der Funktion
fontsize = 16
set term png
set output "plot_${filename}.png"
set ylabel "benötigte Breite in Pixeln" font sprintf(",%d", fontsize)
set xlabel "Breite x der Gleichung in Zeichen" font sprintf(",%d", fontsize)

set terminal png size 800,500 font ",fontsize"

set key inside left top box spacing 1.5

plot filename every ::1 using 1:2 with points pt 2 ps 2 linewidth 3 \
      title "Beispielgleichungen" \
     , f(x) with lines linewidth 3 title sprintf("%.2f + %.2f * x", a, b) \


set output

EOF
rm fit.log

