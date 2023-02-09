

----

# Docker network

```bash
docker network create \
  --driver=bridge \
  --subnet="172.23.0.0/24" \
  --gateway="172.23.0.1" \
  cloud_manager

```

----

# Kafka


```bash
cd .docker/kafka
docker build -t kafka .
docker run -d --name kafka \
    --net=cloud_manager \
    --ip="172.23.0.7" \
    -p '9092:9092' \
    -p '29092:29092' \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ZOOKEEPER_CONNECT=172.23.0.5:2181 \
    -e KAFKA_LISTENERS=LISTENER_DOCKER://kafka:29092,LISTENER_HOST://172.23.0.7:9092 \
    -e KAFKA_ADVERTISED_LISTENERS=LISTENER_DOCKER://kafka:29092,LISTENER_HOST://172.23.0.7:9092 \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=LISTENER_DOCKER:PLAINTEXT,LISTENER_HOST:PLAINTEXT \
    -e KAFKA_INTER_BROKER_LISTENER_NAME=LISTENER_DOCKER \
    -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=100 \
    -e KAFKA_AUTO_CREATE_TOPICS_ENABLE="true" \
    -e KAFKA_LOG_RETENTION_MS=10000 \
    -e KAFKA_LOG_RETENTION_CHECK_INTERVAL_MS=5000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    kafka:latest

```

----

# Zookeeper

```bash
cd .docker/zookeeper
docker build -t zookeeper .
docker run -d --name zookeeper \
    --net=cloud_manager \
    --ip="172.23.0.5" \
    -p "2181:2181" \
    -e ZOOKEEPER_CLIENT_PORT=2181 \
    -e ZOOKEEPER_TICK_TIME=2000 \
    zookeeper:latest
```

----

# Media Server


```bash
cd .docker/media_server
export ZIP_FILE=ant-media-server-community-2.5.1.zip
docker build --network=host -t antmediaserver --build-arg AntMediaServer=$ZIP_FILE .
docker run -d -it --name antmedia --net=cloud_manager --ip=172.23.0.2 antmediaserver
docker exec -it antmedia bash
# ip address
$ hostname -I
172.23.0.2 
# Logs
root@d6588b4df374:/# ls /usr/local/antmedia/log 
0.0.0.0_access.2022-12-30.log  ant-media-server.log  antmedia-error.log
# View Streams (only after you've sent them from the Gstreamer docker container)
root@d6588b4df374:/# ls /usr/local/antmedia/webapps/WebRTCApp/streams
test-001.m3u8  test-001000000000.ts  test-001000000001.ts  test-001000000002.ts  test-001000000003.ts  test-001000000004.ts
```

- view the UI in your web browser: <ip-address>:5080
- e.g. 172.23.0.2:5080
- log in (create password for the 1st time)

----


# Gstreamer


```bash
docker build -t gstreamer .
docker run -d --name gstreamer --net=cloud_manager --ip=172.23.0.3 -w /start gstreamer
docker exec -it gstreamer bash
# send a stream to Ant Media Server
$ export VID=/start/sample.mp4
$ export AMS_URL='rtmp://172.23.0.2:1935/WebRTCApp/test-001'
$ gst-launch-1.0 filesrc location=$VID ! rtmpsink location=$AMS_URL
```

- view streams in AMS: http://172.23.0.2:5080/#/applications/WebRTCApp
- go into AMS docker container and view the files saved: `ls /usr/local/antmedia/webapps/WebRTCApp/streams`
