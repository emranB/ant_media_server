#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json
import requests
import os
from utils import ConfigUtil

ROUTER = Flask(__name__)

# Root directory - env var 'MANAGER_ROOT' is set in run.sh
ROOT_DIR = os.environ['MANAGER_ROOT']

# Load config params required for API calls
API_CONFIG = ConfigUtil().getConfig('/manager/config/api.json')

# Routes / Commands:
#   - create stream
#   - delete stream
#   - enable backup
#   - start play
#   - stop play
class Assistant:
    def __init__(self):
        # Test routes
        ROUTER.add_url_rule('/',        'default',  self.defaultFunc,   methods=['GET'])
        ROUTER.add_url_rule('/test',    'test',     self.test,          methods=['GET'])

        # Define commands, routes and type of requests
        self.commands = {
            'get_stream'    : { 
                'type'      : ['GET'],    
                'pattern'   : '/get_stream/<streamId>',
                'callback'  : self.getStream   
            },
            'create_stream' : { 
                'type'      : ['POST'],   
                'pattern'   : '/createStream',
                'callback'  : self.createStream 
            },
            'delete_stream' : { 
                'type'      : ['DELETE'], 
                'pattern'   : '/createStream/<streamId>',
                'callback'  : self.deleteStream 
            }, 
            'enable_backup' : { 
                'type'      : ['POST'],   
                'pattern'   : '/<streamId>/recording/<recordingState>',
                'callback'  : self.enableBackup 
            }, 
            'start_play'    : { 
                'type'      : ['POST'],   
                'pattern'   : '/<streamId>/start',
                'callback'  : self.startPlay    
            }, 
            'stop_play'     : { 
                'type'      : ['POST'],   
                'pattern'   : '/<streamId>/stop',
                'callback'  : self.stopPlay     
            }
        }

        # Add all core routes
        for (routeName, cfg) in self.commands.items():
            ROUTER.add_url_rule(cfg['pattern'], routeName, cfg['callback'], methods=cfg['type'])

    # Main loop serving API's
    def runRouter(self, setDebug=False):
        ROUTER.run(host='0.0.0.0', port=5000, debug=setDebug)

    # Test endpoint callback - check if "/" location is responding
    def defaultFunc(self):
        return 'default ok'

    # Test endpoint callback - check if "/test" location is responding
    def test(self):
        return 'test ok'

    # Endpoint callback - "/get_stream" - Get stream by streamId
    # Full endpoint     - IP:port/WebRTCApp/rest/v2/broadcasts/{{stream_id}} - GET
    def getStream(self, streamId=''):        
        suffix = f'/broadcasts/{API_CONFIG["stream_id"]}' 
        result = self.executeApiCall('GET', suffix)
        return json.loads(result.content)['rtmpURL'] if result.ok else result.content

    # Endpoint callback - "/create_stream" - Create a new stream to publish to
    # Full endpoint     - IP:port/WebRTCApp/rest/v2/broadcasts/create - POST
    def createStream(self):
        cfg = {}

        if request and request.data:
            cfg = jsonify(request.data)
        else:
            try:
                cfg = ConfigUtil().getConfig('/manager/config/createStream.json') 
            except IOError:
                print("Error config file not found: /manager/config/createStream.json")
                return {}

        # make post request with cfg
        suffix = '/broadcasts/create'  
        result = self.executeApiCall('POST', suffix, cfg)
        return json.loads(result.content)['rtmpURL'] if result.ok else result.content
    
    # Endpoint callback - "/delete_stream" - Delete stream by streamId
    # Full endpoint     - IP:port/WebRTCApp/rest/v2/broadcasts/{{stream_id}} - DELETE
    def deleteStream(self, streamId=''):
        id = streamId if streamId != '' else API_CONFIG["stream_id"]     
        suffix = f'/broadcasts/{id}' 
        result = self.executeApiCall('DELETE', suffix)
        return result.content if result else {}

    # Endpoint callback - "/enable_backup" - When enabled, stream videos are stored in location specified by 'sub-folder' field
    # Full endpoint     - IP:port/WebRTCApp/rest/v2/broadcasts/{{stream_id}}/recording/{{recording_state - TRUE | FALSE}}/?recordingType= - POST
    def enableBackup(self, streamId='', enable='', recordingType=''):
        streamId = streamId if streamId != '' else API_CONFIG["stream_id"]     
        enable = enable if enable != '' else 'true'     

        suffix = f'/broadcasts/{streamId}/recording/{enable}'
        
        getParam = None
        if request and request.args.get('recordType'):
            recordingType = request.args.get('recordType')
        if getParam != None:
            recordingType = getParam

        if recordingType != '': 
            suffix += "?recordType=" + recordingType    # Optional param, eg. mp4
        else:
            suffix += "?recordType=mp4"                 # Set mp4 by default

        url = self.generateApiEndpoint(suffix)
        result = self.executeApiCall('PUT', suffix)
        return result.content if result else {}
        
    # Endpoint callback - "/start_play" - Starts playing videos in an established stream by streamId
    # Full endpoint     - IP:port/WebRTCApp/rest/v2/broadcasts/{{stream_id}}/start - POST
    def startPlay(self, streamId=''):
        id = streamId if streamId != '' else API_CONFIG["stream_id"]     
        suffix = f'/broadcasts/{id}/start'
        result = self.executeApiCall('POST', suffix)
        return result.content if result else {}

    # Endpoint callback - "/stop_play" - Stop playing videos in an established stream by streamId
    # Full endpoint     - IP:port/WebRTCApp/rest/v2/broadcasts/{{stream_id}}/stop - POST
    def stopPlay(self):   
        suffix = f'/broadcasts/{API_CONFIG["stream_id"]}/stop'
        result = self.executeApiCall('POST', suffix)
        return result.content if result else {}

    # Generate path, given suffix
    def generateApiEndpoint(self, suffix=''):
        if suffix == '': return ''
        prefix = f'{API_CONFIG["media_url"]}/{API_CONFIG["rest_path"]}'
        return f'{prefix}{suffix}'

    # Compile full API endpoint, and make call to endpoint
    def executeApiCall(self, type='GET', suffix='', cfg={}):
        if suffix == '': return {}
        
        url = self.generateApiEndpoint(suffix)
        headers = API_CONFIG['headers']
        if      type == 'GET'    : return requests.get(url, headers=headers)
        elif    type == 'POST'   : return requests.post(url, data=json.dumps(cfg), headers=headers)
        elif    type == 'DELETE' : return requests.delete(url, headers=headers)
        elif    type == 'PUT'    : return requests.put(url, headers=headers)
        else:   return {}
