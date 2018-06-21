# TODO Travis CI Integration for building Docker images

#!/usr/bin/env bash

# Build images
sudo docker build -t robodockdev/beakerx ./beakerx/
sudo docker build -t robodockdev/clickhouse-client ./clickhouse-client/
sudo docker build -t robodockdev/grafana ./grafana/
sudo docker build -t robodockdev/h2o ./h2o/
sudo docker build -t robodockdev/healthchecker ./healthchecker/
sudo docker build -t robodockdev/jenkins ./jenkins/
sudo docker build -t robodockdev/kafka ./kafka/
sudo docker build -t robodockdev/presto ./presto/
sudo docker build -t robodockdev/prophet ./prophet/
sudo docker build -t robodockdev/redis-cluster ./redis-cluster/

sudo docker login --username robodockdev --password 00190300

# Push images
sudo docker push robodockdev/beakerx
sudo docker push robodockdev/clickhouse-client
sudo docker push robodockdev/grafana
sudo docker push robodockdev/h2o
sudo docker push robodockdev/healthchecker
sudo docker push robodockdev/jenkins
sudo docker push robodockdev/kafka
sudo docker push robodockdev/presto
sudo docker push robodockdev/prophet
sudo docker push robodockdev/redis-cluster