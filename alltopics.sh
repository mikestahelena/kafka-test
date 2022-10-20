#!/bin/bash
topics=`docker exec broker1 kafka-topics --bootstrap-server localhost:9092 --list`

while read -r line; do lines+=("$line"); done <<<"$topics"
echo '{"version":1,
 "topics":['
 for t in $topics; do
     echo -e '     { "topic":' \"$t\" '},'
done

echo '  ]
}'

