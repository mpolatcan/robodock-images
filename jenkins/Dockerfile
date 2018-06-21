FROM jenkins/jenkins

MAINTAINER Mutlu Polatcan <mutlupolatcan@gmail.com>

USER root

ADD docker-latest.sh /

RUN apt-get update && \
    apt-get -y install --no-install-recommends apt-transport-https software-properties-common maven && \
    rm -rf /var/lib/apt/lists/* && \
    chmod +x docker-latest.sh && \
    ./docker-latest.sh