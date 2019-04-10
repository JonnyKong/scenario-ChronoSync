#!/bin/bash
# Run a number of simulations in parallel 

set -e

RUN_TIMES=12

./waf

for (( TIME=1; TIME<=$RUN_TIMES; TIME++ )); do
    ./build/chronosync-mobile >> results/result_${TIME}.txt &
    pids="$pids $!"
done
wait $pids
