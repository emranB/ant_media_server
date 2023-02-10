NOTE: This script assumes that the host machine has docker compose installed.
Docker compose is installed by default on Windows and MAC machines when docker is installed.
For Linux machines, you can run the script 

        docker_compose_install_ubuntu.sh
to install docker compose.


Make sure you're starting at the root of the project, or navigate to to location where .docker directory is located.


STEP 1: Build and deploy
--------------------------------------------------------------------------------------
Option 1: Run the `build_and_run.sh` script using:

        sh build_and_run.sh
This will build all docker compose dependencies and deploy them on the worker machine


OR


Option 2: Manually build and deploy:
1. Build all dependencies using:

        docker-compose -f docker-compose.yml build --progress plain
2. Deploy and start all containers using:

        docker-compose -f docker-compose.yml up -d
--------------------------------------------------------------------------------------


STEP 2: Create Ant Media Server stream (sink):
--------------------------------------------------------------------------------------
1. Navigate to media server, use:
    
        docker exec -it media_server bash
Note: this will open up a terminal in the location:
    
        /usr/local

2. Run media server services, use:
    
        sh start_media_server_and_create_stream.sh /usr/local
Note: this will start all required services (kafka, zookeeper, ant media server, gstreamer, mongodb, manager)

3. To create a stream in AMS, use (in the python shell):
    
        create_stream
Note: this will create a stream and send back a rtmp url to publish videos to


Verify that the rtmp url (received from the previous step) matches the value of the param:
    
        AMS_URL
in the file:
    
        /.docker/gstreamer/play.sh
--------------------------------------------------------------------------------------


STEP 3: Start gstreamer video publishing service (source):
--------------------------------------------------------------------------------------
1. Open up a separate terminal and navigate to the publishing source (gstreamer in this context), use:
    
        docker exec -it gstreamer bash
Note: this will open up a terminal in the location:
    
        /start

2. Publish gstreamer stream, use:
    
        sh play.sh
Now you should have a stream running in ant media server


To kill the stream, from the terminal interfacing with the manager app, use:
    
        delete_stream
Alternatively, you can kill the terminal running the gstreamer service
Note: this will only stop the stream, but the AMS channel will not be delete if you use this alternative
--------------------------------------------------------------------------------------


Quicklinks:
- Ant Media Server online interface: http://localhost:5080/#/pages/login
- Grafana server: http://localhost:3000/
- Elastic search server: http://localhost:9200/
- Kafka server: http://localhost:9092/
- Access media server from terminal - docker exec -it media_server bash
- Access gstreamer from terminal - docker exec -it gstreamer bash
