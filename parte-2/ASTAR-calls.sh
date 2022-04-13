#!/bin/bash

path="./ASTAR-tests"
num_tests= 5
heuristic1="heuristic1"
heuristic2="heuristic2"
heuristic3="heuristic3"


for (( i = 1; i < num_tests+1; i++ )); do

    ./ASTARStowage.sh $path "map""$i" "containers""$i" "$heuristic1"
    ./ASTARStowage.sh $path "map""$i" "containers""$i" "$heuristic2"
    ./ASTARStowage.sh $path "map""$i" "containers""$i" "$heuristic3"
    echo $path "map""$i" "containers""$i"

done
