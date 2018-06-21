FROM python:3.6.5-stretch

MAINTAINER Mutlu Polatcan <mutlupolatcan@gmail.com>

USER root 

RUN apt-get update && \
    apt-get -y install --no-install-recommends gcc python-tk nano && \
    rm -rf /var/lib/apt/lists/* && \
    pip install pystan fbprophet scipy scikit-learn colorama bpython pyyaml setuptools