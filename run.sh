#!/bin/bash
# Run a number of simulations in parallel 

set -e

RUN_TIMES=12
LOSS_RATE=0.0
if [ $# -eq 1 ]; then
    LOSS_RATE=$1
fi

rm -f results/*.txt
./waf

for (( TIME=1; TIME<=$RUN_TIMES; TIME++ )); do
    ./build/chronosync-mobile \
        --lossRate=${LOSS_RATE} \
        >> results/result_${TIME}.txt &
    pids="$pids $!"
done
wait $pids
