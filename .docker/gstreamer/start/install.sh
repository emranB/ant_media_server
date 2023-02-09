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


echo "${NAME} pre-flight check for exiting folder $WORKDIR from docker COPY "
export INSTALL_DIR_EXISTS="$(test -d $WORKDIR && echo 'yes' || echo 'no')"
if [[ "$INSTALL_DIR_EXISTS" == "no" ]]; then
  echo "--(fail)-- install directory exists: ${WORKDIR}"
  exit 1;
else
  echo "--(pass)-- install directory exists: ${WORKDIR}"
fi

apt-get update -y && \
apt-get install -y -qq \
    python3-pip wget

python3 -m pip install -r /start/requirements.txt


wget https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4 -O /start/sample.mp4

echo "${NAME} Finished "
