#!/bin/sh


root=""
if [ "$1" != "" ]
    then
        export root=$1
    else
        export root='C:\Users\omega\Desktop\Code\RAD_assessment\matmccann-media_server-2343a7b4e693\matmccann-media_server-2343a7b4e693\.docker\media_server'
fi

# Save the env var for use by manager/py
export MANAGER_ROOT="$root"


echo "Found root at $MANAGER_ROOT/manager/run.sh."
echo "Starting media server . . . "

