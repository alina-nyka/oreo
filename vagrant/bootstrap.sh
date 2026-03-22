#!/bin/bash

apt-get update -y
apt-get install -y docker.io curl git net-tools htop

systemctl enable docker
systemctl start docker

usermod -aG docker vagrant
