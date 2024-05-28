#!/bin/bash

SERVER_IP=""
DATA_ENDPOINT="http://$(SERVER_ip):5001/video"

ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -f mpegts -codec:v mpeg1video -s 640x480 -b:v 1000k -bf 0 $DATA_ENDPOINT &
python3 ./input_client.py -i $SERVER_IP -p 7070
