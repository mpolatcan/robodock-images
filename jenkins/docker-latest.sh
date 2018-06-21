#!/bin/bash

# Install Docker Engine
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

apt-add-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"

apt-get update

apt-cache policy docker-ce

apt-get install -y docker-ce

# Install docker-compose orchestration tool for Docker
# sudo apt-get install python-pip
# sudo pip install -U docker-compose
