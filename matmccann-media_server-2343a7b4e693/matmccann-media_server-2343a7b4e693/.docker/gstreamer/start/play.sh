#!/bin/sh

export VID=/start/sample.mp4
export AMS_URL='rtmp://172.23.0.2:1935/WebRTCApp/test-001'
gst-launch-1.0 videotestsrc ! videoconvert ! x264enc ! flvmux ! rtmpsink location=$AMS_URL