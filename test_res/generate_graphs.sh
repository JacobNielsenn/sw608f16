#!/usr/bin/env bash
rm ../graphics/test_graphs/*.eps
for file in *
do
    if [ ${file: -4} == ".gpi" ]
    then
        echo $file
        gnuplot $file
    fi
done

for file in *
do
    if [ ${file: -4} == ".eps" ]
    then
        mv $file ../graphics/test_graphs/
    fi
done
