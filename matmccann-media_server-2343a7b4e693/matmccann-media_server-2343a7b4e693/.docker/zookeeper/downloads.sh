#!/bin/bash

# Example usage: ./downloads <installation_dir> <version>
# Example usage: ./downloads '/zookeeper' '3.6.3'

export NAME="[downloads.sh]  "
echo "${NAME} STARTING "
export WORK_DIR=$1
export ZK_VERSION=$2
export PATH=$WORK_DIR/bin:$PATH
export now=$(date)

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
apt-get install -y -qq wget

echo "${NAME} Starting downloads for zookeeper"
cd /; wget "https://downloads.apache.org/zookeeper/zookeeper-${ZK_VERSION}/apache-zookeeper-${ZK_VERSION}-bin.tar.gz"
tar -xzf "/apache-zookeeper-${ZK_VERSION}-bin.tar.gz" --
rm -rf "/apache-zookeeper-${ZK_VERSION}-bin.tar.gz" --
mv "/apache-zookeeper-${ZK_VERSION}-bin" "${WORK_DIR}" --

echo "${NAME} Setting base configs for zookeeper"
cd "$WORK_DIR";
mv "${WORK_DIR}/conf/zoo_sample.cfg" "${WORK_DIR}/conf/zoo.cfg";
sed  -i "s|/tmp/zookeeper|${WORK_DIR}/data|g" "${WORK_DIR}/conf/zoo.cfg";
mkdir -p "${WORK_DIR}/data"
sed -i -r 's|#(log4j.appender.ROLLINGFILE.MaxBackupIndex.*)|\1|g' "${WORK_DIR}/conf/log4j.properties"
sed -i -r 's|#autopurge|autopurge|g' "${WORK_DIR}/conf/zoo.cfg"
chmod +x "${WORK_DIR}" -R

echo "${NAME} Storing zookeeper version: ${WORK_DIR}/version.txt"
echo "${now}  |  https://apache.claz.org/zookeeper/stable/apache-zookeeper-${ZK_VERSION}-bin.tar.gz" >> "${WORK_DIR}/version.txt"

echo "${NAME} Finished setting up zookeeper: ${WORK_DIR}"
echo "${NAME} View the available commands for zookeeper: ${WORK_DIR}/bin/zkServer.sh --help"
echo "${NAME} Common command: ${WORK_DIR}/bin/zkServer.sh start-foreground"

echo "${NAME} FINISHED "
