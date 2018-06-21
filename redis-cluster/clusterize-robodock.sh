#!/usr/bin/env bash
chmod +x /usr/local/bin/redis-trib.rb

sleep 30

redis-trib.rb create --replicas ${REDIS_REPLICAS} ${REDIS_CONTAINERS}
