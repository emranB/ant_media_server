#!/bin/bash

# Example usage: ./install.sh

export WORKDIR="/start"
export NAME="[install.sh]: "
echo "${NAME} STARTING "

# Bash failure reporting for the script
set -eE -o functrace
failure() {
  local lineno=$1
  local msg=$2
  echo "${NAME} Failed at $lineno: $msg"
}
trap '${NAME} failure ${LINENO} "$BASH_COMMAND"' ERR

echo "${NAME} Installing apt packages "
apt-get update -y -qq
apt-get install -y -qq \
  unzip openjdk-11-jre-headless wget supervisor openssh-server \
  apt-transport-https ca-certificates curl gnupg-agent software-properties-common \
  iputils-ping \
  tmux

echo "${NAME} FINISHED "
