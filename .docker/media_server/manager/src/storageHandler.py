#!/usr/bin/env python3

import os, time, calendar, shutil, ffmpeg, json
from utils import Timer, ConfigUtil, SystemPath
from db import Db

class StorageHandler:
    def __init__(self):
        self.backupTimer = Timer()
        self.config = ConfigUtil().getConfig('/manager/config/storageHandler.json')
        self.db = Db()
        self.backedUpFiles = []
        self.supportedVideoFormats = ['.mp4', '.avi', '.ts']

        # Define commands
        self.commands = {
            'list_all_backups'   : { 'callback' : self.listAllBackups   },
            'clear_all_backups'  : { 'callback' : self.clearAllBackups  },
            'drop_backups_table' : { 'callback' : self.dropBackupsTable }, 
            'list_all_tables'    : { 'callback' : self.listAllTables    },
            'force_backup'       : { 'callback' : self.backupFiles      }
        }

        self.timeElapsedSinceLastBackup = 0
        self.backupTimer.start()

    # def listAllBackups(self)    : return json.dumps(json.loads(self.db.listAll()), indent=4)
    def listAllBackups(self)    : return self.db.listAll()
    def clearAllBackups(self)   : return self.db.clearCollection()
    def dropBackupsTable(self)  : return self.db.dropCollection()
    def listAllTables(self)     : return self.db.listDatabaseNames()

    def update(self):
        dt = self.backupTimer.elapsed()
        self.step(dt)
    
    def step(self, dt):
        self.timeElapsedSinceLastBackup += dt

        enableBackup = self.config['enable_backup']
        if enableBackup and self.isBackupTime():
            self.backupFiles()
            self.timeElapsedSinceLastBackup = 0
            self.backupTimer.start()

    def isBackupTime(self) -> bool:
        storageBackupTimeElapsed = self.config['storage_backup_time'] * 1000000
        return (self.timeElapsedSinceLastBackup >= storageBackupTimeElapsed)

    def backupFiles(self):
        backedUpFiles = []
        try:
            # If source dir does not exist, do nothing
            inputDirPath  = SystemPath().getFilePath(self.config['input_files_dir'])
            if not os.path.exists(inputDirPath): return [f'{inputDirPath} - does not exist. Exiting.']
            
            # If there are no files to copy, do nothing
            inputFiles = os.listdir(inputDirPath)
            if len(inputFiles) == 0: return [f'{inputFiles} - files to copy. Exiting']
            
            # Generate path of back up directory - Path: ROOT_DIR/<path_to_backup_dir>/timestamp
            currTimeStamp = calendar.timegm(time.gmtime())
            outputDirPath = SystemPath().getFilePath(self.config['output_files_dir'])
            currIterationOutputDirPath = f'{outputDirPath}/{currTimeStamp}'

            # Copy each file to its own dir, named with time stamp
            # Save name of each copied file, to prevent duplicate copies
            for file in os.listdir(inputDirPath):
                # Backup only files with supported extension 
                if not file.endswith(tuple(self.supportedVideoFormats)): return [f'Unsupported file ext: {file}']

                # If file has not been backed up yet, create output directories and backup files
                if (file not in self.backedUpFiles):    
                    # If output dir or sub-dir does not exist, create dirs
                    if not os.path.exists(outputDirPath): os.makedirs(outputDirPath)
                    if not os.path.exists(currIterationOutputDirPath): os.makedirs(currIterationOutputDirPath)

                    # Copy each input file to output location
                    inputFilePath = f'{inputDirPath}/{file}'
                    shutil.copy(inputFilePath, currIterationOutputDirPath)
                    self.backedUpFiles.append(file)

                    # Save details of file in db
                    fileDetails = {
                        'time_stamp'     : currTimeStamp,
                        'file_name'      : file,
                        'base_path'      : outputDirPath.replace('\\', '/'),
                        'length_seconds' : self.config['storage_backup_time']
                    }

                    # ffmpeg.probe can only be run on video files
                    if self.isVideoFile(file):
                        try:
                            videoCfg = json.loads(json.dumps(ffmpeg.probe(inputFilePath)))

                            fileDetails['duration'] = videoCfg['format']['duration']
                            fileDetails['size']     = videoCfg['format']['size']
                            fileDetails['bit_rate'] = videoCfg['format']['bit_rate']
                            fileDetails['streams']  = []

                            for stream in videoCfg['streams']:
                                fileDetails['streams'].append(stream)
                        except Exception as e:
                            print(f'Error probing file: {file}', e)

                    # Save backed up video details to db
                    self.db.insertOne(fileDetails)
                    backedUpFiles.append(fileDetails)
            return backedUpFiles
        except Exception as e:
            return {"Error backing up files.", e}


    # Populate 'formats' with all formats supported by ffmpeg.probe
    def isVideoFile(self, fileName):
        for format in self.supportedVideoFormats:
            if (fileName.endswith(format)): return True
        return False

