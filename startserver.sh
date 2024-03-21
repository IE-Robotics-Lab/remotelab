#!/bin/bash

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
roslaunch rosbridge_server rosbridge_websocket.launch port:=9092 &
ROSBRIDGE_PID=$!
echo "Rosbridge server launched"
sleep 5 # Wait a bit to ensure the rosbridge server has started

# Start the web video server
rosrun web_video_server web_video_server &
WEB_VIDEO_SERVER_PID=$!
echo "Web video server started with PID: $WEB_VIDEO_SERVER_PID"

echo "All services started. Type 'stop' to exit and stop all services."

# Function to kill all started services
cleanup() {
    echo "Stopping all services..."

    # Kill processes by PID
    kill -9 $ROSCORE_PID $CAMERA_PID $WEB_VIDEO_SERVER_PID

    # Specifically find and kill rosbridge_server listening on port 9090
    ROSBRIDGE_PID=$(lsof -ti:9092)
    if [[ ! -z $ROSBRIDGE_PID ]]; then
        echo "Killing rosbridge_server on port 9090 with PID $ROSBRIDGE_PID"
        kill -9 $ROSBRIDGE_PID
    fi

    echo "All services stopped."
    exit 0
}


# Loop waiting for the user to type 'stop'
while : ; do
    read -r -p "Enter command: " cmd
    if [[ $cmd == "stop" ]]; then
        cleanup
        break
    fi
done
