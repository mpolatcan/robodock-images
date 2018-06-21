#!/bin/bash

chmod +x /usr/local/bin/redis-trib.rb

VALID_REDIS_CONTAINERS=()

for i in `docker ps -q`; do
    FIRST_ALIAS=`docker inspect --format '{{range .NetworkSettings.Networks}}{{(index (index .Aliases 0))}}{{end}}' "$i"`
	SECOND_ALIAS=`docker inspect --format '{{range .NetworkSettings.Networks}}{{(index (index .Aliases 1))}}{{end}}' "$i"`

	if [[ $FIRST_ALIAS == "redis-cluster" || $SECOND_ALIAS == "redis-cluster" ]]; then
		IP=`docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$i"`
		VALID_REDIS_CONTAINERS+=($IP":6379");
	fi
done

echo "Valid Redis containers:" ${VALID_REDIS_CONTAINERS[*]}

redis-trib.rb create --replicas 1 ${VALID_REDIS_CONTAINERS[*]}
