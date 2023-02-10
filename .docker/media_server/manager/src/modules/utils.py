#!/usr/bin/env python3

import time, os, json

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