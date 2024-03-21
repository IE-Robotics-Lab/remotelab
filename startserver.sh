#!/bin/bash

# Put script in its own process group
set -m

# Start roscore
roscore &
ROSCORE_PID=$!
echo "roscore started with PID: $ROSCORE_PID"
sleep 5 # Wait a bit to ensure roscore is fully up

# Start the AVT Vimba camera node
roslaunch avt_vimba_camera mono_camera.launch ip:="10.205.3.35" &
CAMERA_PID=$!
echo "AVT Vimba camera node launched"
sleep 5 # Wait a bit to ensure the camera node has started

# Start the rosbridge server
roslaunch rosbridge_server rosbridge_websocket.launch &
ROSBRIDGE_PID=$!
echo "Rosbridge server launched"
sleep 5 # Wait a bit to ensure the rosbridge server has started

# Start the web video server
rosrun web_video_server web_video_server &
WEB_VIDEO_SERVER_PID=$!
echo "Web video server started with PID: $WEB_VIDEO_SERVER_PID"

echo "All services started. Press Ctrl+C to exit and stop all services."

# Function to kill all started services
cleanup() {
    echo "Stopping all services..."
    kill -9 $ROSCORE_PID $CAMERA_PID $ROSBRIDGE_PID $WEB_VIDEO_SERVER_PID
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup function
trap cleanup SIGINT

# Wait indefinitely until a signal is received
wait
