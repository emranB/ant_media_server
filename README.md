Instructions to run and deploy app:

1. Make sure you're starting at the root of the project, or navigate to to location where .docker directory is located.

2. From a terminal (running in admin mode if running from windows OS), use:
        cd .docker

3. To build docker services, use:
    docker-compose -f docker-compose.yml build
Note: this will navigate the terminal to open run the manager python app

4. Navigate to media server, use:
    docker exec -it media_server bash
Note: this will open up a terminal in the location:
    /usr/local

5. Run media server services, use:
    sh start_media_server_and_create_stream.sh /usr/local
Note: this will start all required services (kafka, zookeeper, ant media server, gstreamer, mongodb, manager)

6. To create a stream in AMS, use (in the python shell):
    create_stream
Note: this will create a stream and send back a rtmp url to publish videos to

7. Verify that the rtmp url (received from the previous step) matches the value of the param:
    AMS_URL
in the file:
    /.docker/gstreamer/play.sh

8. Open up a separate terminal and navigate to the publishing source (gstreamer in this context), use:
    docker exec -it gstreamer bash
Note: this will open up a terminal in the location:
    /start

9. Publish gstreamer stream, use:
    sh play.sh
Now you should have a stream running in ant media server

10. To kill the stream, from the terminal interfacing with the manager app, use:
    delete_stream
Alternatively, you can kill the terminal running the gstreamer service
Note: this will only stop the stream, but the AMS channel will not be delete if you use this alternative


Quicklinks:
- Ant Media Server online interface: http://localhost:5080/#/pages/login
- Grafana server: http://localhost:3000/
- Elastic search server: http://localhost:9200/
- Kafka server: http://localhost:9092/
- Access media server from terminal - docker exec -it media_server bash
- Access gstreamer from terminal - docker exec -it gstreamer bash
