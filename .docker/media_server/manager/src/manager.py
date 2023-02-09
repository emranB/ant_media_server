#!/usr/bin/env python3

import time, signal, sys
from assistant import Assistant
from storageHandler import StorageHandler
from utils import MultiProcProcess, MultithreadingThread

assistant = Assistant()
storageHandler = StorageHandler()
processorType = 'multiprocessing'
# subProcs = []

# Signal handler
def signalHandler(signal, handler):
    shutdownSystem()
signal.signal(signal.SIGINT, signalHandler)

# Kill all subprocesses on exit
def shutdownSystem():
    match(processorType):
        case 'multiprocessing':
            MultiProcProcess.killAllProcesses()
        case 'multithreading':
            MultithreadingThread.killAllThreads()
            pass
        case _:
            MultiProcProcess.killAllProcesses()
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
        
def mainMultiProc():
    # Create sub proc to periodically backup saved files
    storageHandlerSubProc = MultiProcProcess.addProcess(updateStorageHandler)

    # Create sub proc to serve APIs through router
    assitantSubProc = MultiProcProcess.addProcess(assistant.runRouter)

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

def mainMultiThread():
    # Create sub proc to periodically backup saved files
    storageHandlerThread = MultithreadingThread.addThread(updateStorageHandler)

    # Create sub proc to serve APIs through router
    assitantThread = MultithreadingThread.addThread(assistant.runRouter)

    storageHandlerThreadIsAlive = storageHandlerThread.is_alive()
    if storageHandlerThreadIsAlive: print("Storage handler running ok.")

    assitantThreadIsAlive = assitantThread.is_alive()
    if assitantThreadIsAlive: print("Assistant running ok.")

    try:
        while True:
            if (storageHandlerThreadIsAlive and assitantThreadIsAlive): # Keep reading user input until subprocesses are running and alive
                readUserInput()     
                time.sleep(1)
    except KeyboardInterrupt:
        print("Exitting...")

# Main loop
if __name__ == '__main__':
    match(processorType):
        case 'multiprocessing':
            mainMultiProc()
        case 'multithreading':
            mainMultiThread()
        case _:
            mainMultiProc()

    shutdownSystem()
