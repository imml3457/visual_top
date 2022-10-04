#! /bin/bash

function get_cpu_usage () {
    head -n $((1 + $(nproc))) < /proc/stat | tail -n $(nproc)
}

for i in 1 2 3 4 5
do
    cpu_usage_before=$(get_cpu_usage)
    sleep 5
    cpu_usage_after=$(get_cpu_usage)
    printf "%s\n%s" "$cpu_usage_before" "$cpu_usage_after" | awk '{total_time = $2+$3+$4+$5+$6+$7+$8; user_time = $2; nice_time = $3; system_time = $4;\
    idle_time = $5 + $6; total_times[$1] = total_time - total_times[$1]; i_times[$1] = idle_time - i_times[$1]; u_times[$1] = user_time - u_times[$1]; n_times[$1] = nice_time - n_times[$1]; \
    s_times[$1] = system_time - s_times[$1]; } \
    END {for(key in total_times){printf("%s %f %f %f %f %f\n", key, u_times[key], n_times[key], s_times[key], total_times[key], i_times[key]);}}' > cpu_times.txt

    ps aux > ps_snapshot.txt

    python visual_top.py | ../jgraph/jgraph -P -L | ps2pdf - | convert -density 300 -  -quality 100 "temp$i.jpg"
done
