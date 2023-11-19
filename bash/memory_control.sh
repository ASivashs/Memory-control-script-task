#!/bin/bash


usage_limit=80
url="http://127.0.0.1:8080/alarm"

if [[ "$1" =~ ^[0-9]+$ && $1 -le 100 ]]; then
    usage_limit=$1
fi

if [[ -n $2 ]]; then
    url=$2
fi

memory_usage=($(free -m | tail -n +2 | head -1 | tr -s " "))

total=${memory_usage[1]}
used=${memory_usage[2]}
free=${memory_usage[3]}
shared=${memory_usage[4]}
cache=${memory_usage[5]}
available=${memory_usage[6]}

used_perentage=($(echo "$used / $total * 100" | bc -l))
used_perentage=$(printf '%.*f\n' 0 $used_perentage)

if [[ $usage_limit -le $used_perentage ]]; then
    echo "Memory usage is: $used_perentage"

    message="{\"total\": \"$total\", \
        \"used\": \"$used\", \
        \"used_percentage\": \"$usage_percentage\", \
        \"free\": \"$free\", \
        \"shared\": \"$shared\", \
        \"cache\": \"$cache\"}"

    curl -H "Content-Type: application/json" \
        -X POST \
        --data "$message" \
        $url
fi
