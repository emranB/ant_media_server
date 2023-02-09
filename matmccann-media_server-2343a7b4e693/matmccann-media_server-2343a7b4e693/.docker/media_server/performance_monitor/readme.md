Instal Elasticseach
1. Import GPG key and Repo

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

2. Update package lists and install elastic search

sudo apt-get update && sudo apt-get install elasticsearch

3. Enable and start elasticsearch service

sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service

----------------------------------------------------------------------------------------------------------------

Install Logstash
Logstash is a server‑side data processing pipeline that ingests data from multiple sources simultaneously, transforms it and then sends it to a “stash” like Elasticsearch

1. Update your package lists, then install logstash with the following command

sudo apt-get update && sudo apt-get install logstash
2. Enable logstash service

sudo systemctl enable logstash.servic

----------------------------------------------------------------------------------------------------------------

Configure logstash. Create /etc/logstash/conf.d/logstash.conf file and add below content. Please don't forget to replace kafka_server_ip and make sure elasticsearch_ip is correct.

#kafka
input {
  kafka {
    bootstrap_servers => "kafka_server_ip:9092"
    client_id => "logstash"
    group_id => "logstash"
    consumer_threads => 3
    topics => ["ams-instance-stats","ams-webrtc-stats","kafka-webrtc-tester-stats"]
    codec => "json"
    tags => ["log", "kafka_source"]
    type => "log"
  }
}

#elasticsearch
output {
  elasticsearch {
     hosts => ["127.0.0.1:9200"] #elasticsearch_ip
     index => "logstash-%{[type]}-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}