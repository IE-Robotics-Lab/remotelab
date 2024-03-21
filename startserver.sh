#!/bin/bash

# Start roscore in the background
roscore &
ROSCORE_PID=$!
echo "Started roscore with PID $ROSCORE_PID"

# Wait a bit to ensure roscore is up
sleep 5

# Start the camera node
roslaunch avt_vimba_camera mono_camera.launch ip:="10.205.3.35" &
echo "Started camera node"

# Start rosbridge_server
roslaunch rosbridge_server rosbridge_websocket.launch &
echo "Started rosbridge_server"

# Start web_video_server
rosrun web_video_server web_video_server &
echo "Started web_video_server"

# Optionally, wait for any command to finish, then kill the others
wait -n
kill 0
