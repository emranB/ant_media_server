# This docker file can be used in kubernetes. 
# It accepts all cluster related parameters at run time. 
# It means it's very easy to add new containers to the cluster 

FROM ubuntu:20.04

ARG AntMediaServer

ARG BranchName=master

# Needed to suppress hanging calls made by ubuntu installation
ARG DEBIAN_FRONTEND=noninteractive  


################# INSTALL ALL LIBS AND DEPENDENCIES ###################
RUN apt-get update && apt-get install -y \
    curl wget iproute2 cron logrotate \
    gawk openjdk-8-jdk \
    sudo curl gnupg systemd \
    nmap vim net-tools \
    python3 python3-pip ffmpeg 

# INSTALL SYSTEMCTL REDIRECTION SCRIPT FOR DOCKER DAEMON PROCESSES
RUN wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl3.py \
    -O /usr/local/bin/systemctl \
    && cp /usr/local/bin/systemctl /usr/bin/systemctl

# REGISTER DOCKER PROCESSES AS SYSTEMD SERVICES - NEEDED FOR WSL2
COPY ./systemd_daemon/docker.service /etc/systemd/system
COPY ./systemd_daemon/docker.socket /etc/systemd/
#######################################################################




###################### INSTALL ANT MEDIA SERVER #######################
ADD ./${AntMediaServer} /home

RUN cd home \
    && pwd \
    && wget https://raw.githubusercontent.com/ant-media/Scripts/${BranchName}/install_ant-media-server.sh \
    && chmod 755 install_ant-media-server.sh

RUN cd home \
    && pwd \
    && ./install_ant-media-server.sh -i ${AntMediaServer} -s false
#######################################################################




##################### INSTALL AMS MONITORING TOOLS #####################
RUN cd home \
    && pwd \
    && wget https://raw.githubusercontent.com/ant-media/Scripts/master/install-monitoring-tools.sh \
    && chmod +x install-monitoring-tools.sh

RUN cd home \
    && pwd \
    && sudo ./install-monitoring-tools.sh -y

# Stop all services before overriding config files
# RUN sudo systemctl stop elasticsearch.service
# RUN sudo systemctl stop logstash.service
# RUN sudo systemctl stop kafka-zookeeper.service
# RUN sudo systemctl stop kafka.service
# RUN sudo systemctl stop grafana-server.service

# Copy logstash config
COPY ./performance_monitor/logstash.conf /etc/logstash/conf.d/logstash.conf

# Expose elastic search to localhost:9200 - edit network.host & http.port params in /etc/elasticsearch/elasticsearch.yml
RUN awk '/#network.host:/ \
{ print "\
transport.host: localhost \n\
transport.tcp.port: 9300 \n\
http.port: 9200 \n\
network.host: 0.0.0.0 \n\
bootstrap.memory_lock: true\
"; next; }; { print; }' \
    /etc/elasticsearch/elasticsearch.yml > tmp1.yml \
    && cat tmp1.yml > /etc/elasticsearch/elasticsearch.yml \
    && rm tmp1.yml
RUN awk '/#discovery.seed_hosts:/ \
{ print "discovery.seed_hosts: [\"0.0.0.0\", \"[::0]\"]"; next; }; { print; }' \
    /etc/elasticsearch/elasticsearch.yml > tmp2.yml \
    && cat tmp2.yml > /etc/elasticsearch/elasticsearch.yml \
    && rm tmp2.yml

# Edit server.properties - /opt/kafka/config/server.properties - as: listeners=PLAINTEXT://your_server_ip:9092
RUN awk '/#listeners=/ \
{ print "listeners=PLAINTEXT://172.23.0.7:9092"; next; }; { print; }' \
    /opt/kafka/config/server.properties > tmp3.yml \
    && cat tmp3.yml > /opt/kafka/config/server.properties \
    && rm tmp3.yml

# Edit kafka brokers - /usr/local/antmedia/conf/red5.properties - as: server.kafka_brokers=ip_address:port_number
RUN awk '/server.kafka_brokers=/ \
{ print "server.kafka_brokers=172.23.0.7:9092"; next; }; { print; }' \
    /usr/local/antmedia/conf/red5.properties > tmp4.yml \
    && cat tmp4.yml > /usr/local/antmedia/conf/red5.properties \
    && rm tmp4.yml

# Enable all services before restarting
RUN sudo systemctl enable elasticsearch.service \
    && sudo systemctl enable logstash.service \
    && sudo systemctl enable kafka-zookeeper.service \
    && sudo systemctl enable kafka.service \
    && sudo systemctl enable grafana-server.service

# Restart all services
RUN sudo systemctl restart elasticsearch.service \
    && sudo systemctl restart logstash.service \
    && sudo systemctl restart kafka-zookeeper.service \
    && sudo systemctl restart kafka.service \
    && sudo systemctl restart grafana-server.service
#####################################################################








# ##################### Install elastic search ######################
# # RUN wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl.py \
# #     -O /usr/local/bin/systemctl
# #     && cp /usr/local/bin/systemctl /usr/bin/systemctl

# # 1. Import GPG key and Repo
# RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
#     && apt-get install apt-transport-https \
#     && echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list

# # 2. Update package lists and install elastic search
# RUN apt-get update && apt-get install elasticsearch && chmod 777 /etc/systemd/system

# # 3. Enable and start elasticsearch service
# RUN sudo systemctl enable elasticsearch
# RUN sudo systemctl start elasticsearch 
# ####################################################################

# ######################### Install logstash #########################
# # 1. Update package lists, then install logstash with the following command
# RUN sudo apt-get update && sudo apt-get install -y logstash sudo gnupg systemd

# # 2. Configure logstash. Create /etc/logstash/conf.d/logstash.conf file
# COPY ./performanceMonitor/logstash.conf /etc/logstash/conf.d/logstash.conf

# # 2. Enable logstash service
# RUN sudo systemctl enable logstash.service 

# # Restart logstash service
# # RUN sudo systemctl start logstash.service
# RUN /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d
# #####################################################################








###################### Install and deploy manager #######################
# Copy manager to /home directory
COPY manager /usr/local/manager

# Install python dependencies
RUN cd /usr/local/manager \
    && pwd \
    && pip install -r requirements.txt \
    && chmod 755 run.sh

WORKDIR /usr/local/manager
####################################################################

####################### Run services #######################
# CMD ["sh", "/usr/local/manager/run.sh", "/usr/local"]
ENTRYPOINT ["/usr/local/antmedia/start.sh"]

