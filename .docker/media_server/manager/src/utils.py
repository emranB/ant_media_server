#!/usr/bin/env python3

import time, os, json
from multiprocessing import Process as MultiProcProcess
from threading import Thread as MultithreadingThread

# Root directory - env var 'MANAGER_ROOT' is set in run.sh
ROOT_DIR = os.environ['MANAGER_ROOT']

class Timer:
    def __init__(self):
        self.startTime = 0

    def start(self):
        self.startTime = time.time()            # "restart timer" -> set start time to now

    def elapsed(self):
        timeNow = time.time()
        elapsedTime = timeNow - self.startTime  # in seconds x 10^-6
        return elapsedTime

class ConfigUtil:
    def __init__(self):
        pass

    def getConfig(self, cfgPathFromProjectRoot):
        data = {}

        with open(SystemPath().getFilePath(cfgPathFromProjectRoot)) as cfgFile:
            if cfgFile:
                data = json.load(cfgFile)
                cfgFile.close()

        return data

class SystemPath:
    def __init__(self):
        pass

    def getFilePath(self, filePathEndFragment):
        return f'{ROOT_DIR}{filePathEndFragment}'

class MultiprocProcess:
    def __init__(self):
        self.procs = []

    def addProcess(self, targetHandler):
        newProc = MultiProcProcess(target=targetHandler)
        self.procs.append(newProc)
        newProc.start()
        time.sleep(1)   # Allow a moment for service to startup ok during init
        return newProc

    def killAllProcesses(self):
        for proc in self.procs:
            proc.terminate()
            proc.join()

class MultithreadingThread:
    def __init__(self):
        self.threads = []

    def addThread(self, targetHandler):
        newThread = MultithreadingThread(target=targetHandler)
        newThread.setDaemon(True)
        self.threads.append(newThread)
        newThread.start()
        time.sleep(1)   # Allow a moment for service to startup ok during init
        return newThread

    def killAllThreads(self):
        for thread in self.newThread:
            thread.terminate()
            thread.join()
            
