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
set term png
set output "plot_${filename}.png"

set key outside

plot filename every ::1 using 1:2 with points  title "Daten" \
     , f(x) with lines title sprintf("%.2f + %.2f * x", a, b) \


set output

EOF
rm fit.log

