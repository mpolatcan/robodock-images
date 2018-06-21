FROM python:alpine

MAINTAINER Mutlu Polatcan <mutlupolatcan@gmail.com>

COPY RobodockHealthChecker.py Config.py ./

RUN apk --update add --no-cache gnupg ca-certificates netcat-openbsd curl docker && \
    pip install pyyaml colorama
