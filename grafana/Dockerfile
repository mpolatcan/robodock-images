FROM grafana/grafana:latest 

MAINTAINER Mutlu Polatcan <mutlupolatcan@gmail.com>

USER root

COPY grafana.sh /usr/local/bin

RUN chmod +x /usr/local/bin/grafana.sh && \
    apt-get update && \
    apt-get install --no-install-recommends less && \
    rm -rf /var/lib/apt/lists/* && \
    grafana.sh plugin install grafana-worldmap-panel && \
    grafana.sh plugin install grafana-piechart-panel