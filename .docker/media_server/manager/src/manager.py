#!/usr/bin/env python3

import time, signal, sys, multiprocessing
from modules.assistant import Assistant
from modules.storageHandler import StorageHandler
from modules.db import Db
from modules.utils import ConfigUtil

assistant = Assistant(ConfigUtil().getConfig('/manager/config/api.json'))
database = Db(ConfigUtil().getConfig('/manager/config/db.json'))
storageHandler = StorageHandler(ConfigUtil().getConfig('/manager/config/storageHandler.json'), database)

subProcs = []

# Signal handler
def signalHandler(signal, handler):
    shutdownSystem()
signal.signal(signal.SIGINT, signalHandler)

# Kill all subprocesses on exit
def shutdownSystem():
    print('Shutting down...')
    for proc in subProcs:
        proc.terminate()
        proc.join()
    sys.exit(0)

# Read user input and redirect to cmds, if avaiable 
def readUserInput():
    # Reading user input
    userInp = input("> Enter command or type 'help' for support. \r\n")

    # Support commnands - get available commands from sub procs
    if (userInp == 'help' or userInp == 'list_commands'):
        print('Available commands: ')
        for [name, func] in dict(assistant.commands, **storageHandler.commands).items():
            print(f'- {name}')

    # If input string matches any of Assistant's cmds, call its callback
    elif (userInp in assistant.commands): 
        result = assistant.commands[userInp]['callback']()
        print(result)

    # If input string matches any of StorageHandler's cmds, call its callback
    elif (userInp in storageHandler.commands): 
        result = storageHandler.commands[userInp]['callback']()
        print(result)


def updateStorageHandler():
    while True:
        storageHandler.update()

# Main loop
if __name__ == '__main__':
    # Create sub proc to periodically backup saved files
    storageHandlerSubProc = multiprocessing.Process(target=updateStorageHandler)
    subProcs.append(storageHandlerSubProc)
    storageHandlerSubProc.start()
    time.sleep(1)

    # Create sub proc to serve APIs through router
    assitantSubProc = multiprocessing.Process(target=assistant.runRouter)
    subProcs.append(assitantSubProc)
    assitantSubProc.start()
    time.sleep(1)

    storageHandlerSubProcIsAlive = storageHandlerSubProc.is_alive()
    if storageHandlerSubProcIsAlive: print("Storage handler running ok.")

    assistantSubProcIsAlive = assitantSubProc.is_alive()
    if assistantSubProcIsAlive: print("Assistant running ok.")

    try:
        while True:
            if (storageHandlerSubProcIsAlive and assistantSubProcIsAlive): # Keep reading user input until subprocesses are running and alive
                readUserInput()     
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exitting...")

    shutdownSystem()
