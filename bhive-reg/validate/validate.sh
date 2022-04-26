#! /bin/bash

# rm -r newlogs
# rm -r newout

count=$1

mkdir validate_result
mkdir validate_result/logs
mkdir validate_result/out

event_bbs=$(find ./processed_app_bb/merged -type f -name '*.txt')
for event_bb in $event_bbs
do

event=`basename ${event_bb}`
event=$(echo $event | sed 's/\.[^.]*$//')

n=`awk '{print NR}' ${event_bb}|tail -n1`
for((i=1;i<=$n;i+=1))
do
    out=`./main ${event_bb} $i $event $count >> validate_result/logs/${event}.log`
done
python3 analyze_out.py validate_result/logs/${event}.log > validate_result/out/${event}.log
done
