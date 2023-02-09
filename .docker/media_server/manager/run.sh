#!/bin/sh

# Set ROOT_DIR, needed by manager to fetch files
# Usage:
#   eg. sh run.sh 
#       -> executes manager.py by using default location as root
#
#   eg. sh run.sh <PATH_TO_ROOT>
#       -> executes manager.py by using <PATH_TO_ROOT> as root

root=""
if [ "$1" != "" ]
    then
        export root=$1
    else
        export root='C:\Users\omega\Desktop\Code\RAD_assessment\matmccann-media_server-2343a7b4e693\matmccann-media_server-2343a7b4e693\master'
fi

# Save the env var for use by manager/py
export MANAGER_ROOT="$root"

# Execute manager.py using root location
python3 "$root"/manager/src/manager.py