#!/bin/sh


root=""
if [ "$1" != "" ]
    then
        export root=$1
    else
        export root='C:\Users\omega\Desktop\Code\RAD_assessment\matmccann-media_server-2343a7b4e693\matmccann-media_server-2343a7b4e693\.docker\media_server'
fi

# Save the env var for use by manager/py
export MANAGER_ROOT="$root"

echo "Found root at $MANAGER_ROOT/manager/run.sh."
echo "Setting up environment . . . "

# Enable daemon processes
echo "Enabling Kafka-zookeeper"
sudo systemctl enable kafka-zookeeper.service

echo "Enabling Kafka"
sudo systemctl enable kafka.service

echo "Enabling Elasticsearch"
sudo systemctl enable elasticsearch.service

echo "Enabling Logstash"
sudo systemctl enable logstash.service

echo "Enabling Grafana Serer"
sudo systemctl enable grafana-server.service

# Start daemon processes
echo "Starting kafka-zookeeper"
sudo systemctl restart kafka-zookeeper
OUT=$?
if [ $OUT -ne 0 ]; then
    echo "kafka-zookeeper could not be started. Exiting . . . "
    exit $OUT
fi

echo "Starting Kafka"
sudo systemctl restart kafka.service
OUT=$?
if [ $OUT -ne 0 ]; then
    echo "kafka could not be started. Exiting . . . "
    exit $OUT
fi

echo "Starting Elasticsearch"
sudo systemctl restart elasticsearch.service
OUT=$?
if [ $OUT -ne 0 ]; then
    echo "elasticsearch could not be started. Exiting . . . "
    exit $OUT
fi

echo "Starting Logstash"
sudo systemctl restart logstash.service
OUT=$?
if [ $OUT -ne 0 ]; then
    echo "logstash could not be started. Exiting . . . "
    exit $OUT
fi

echo "Starting Grafana Server"
sudo systemctl restart grafana-server.service
OUT=$?
if [ $OUT -ne 0 ]; then
    echo "grafana-server could not be started. Exiting . . . "
    exit $OUT
fi

# Environment setup ok, start media server
echo "Starting media server . . . "
sh ./manager/run.sh $MANAGER_ROOT