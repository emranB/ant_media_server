
----

# Media Server

- ant media server for video management of streams from edge devices

----

## Setup

- download dockerfile and community version of AMS
```bash
cd .docker/media_server
wget https://raw.githubusercontent.com/ant-media/Scripts/master/docker/Dockerfile_Process -O Dockerfile
wget https://github.com/ant-media/Ant-Media-Server/releases/download/ams-v2.5.1/ant-media-server-community-2.5.1.zip
```

- build container

```bash
cd .docker/media_server
export ZIP_FILE=ant-media-server-community-2.5.1.zip
docker build --network=host -t antmediaserver --build-arg AntMediaServer=$ZIP_FILE .
```
- run container

```bash

docker network create \
  --driver=bridge \
  --subnet="172.23.0.0/24" \
  --gateway="172.23.0.1" \
  cloud_manager

docker run -d -it --name antmedia --net=cloud_manager --ip=172.23.0.2 antmediaserver
docker exec -it antmedia bash
$ hostname -I
172.23.0.2 

```

- view the UI in your web browser: <ip-address>:5080
- e.g. 172.23.0.2:5080

----

## Logs

```bash
root@d6588b4df374:/# ls /usr/local/antmedia/log 
0.0.0.0_access.2022-12-30.log  ant-media-server.log  antmedia-error.log

```

----

# View Streams 


```bash
root@d6588b4df374:/# ls /usr/local/antmedia/webapps/WebRTCApp/streams
test-001.m3u8  test-001000000000.ts  test-001000000001.ts  test-001000000002.ts  test-001000000003.ts  test-001000000004.ts
```


