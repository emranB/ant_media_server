#!/usr/bin/env python3

import sys, os, shutil

inputPath = "./_in_dir"
outputPath = "./test"

os.chmod(inputPath, 777)

try:
    while True:
        inp = input("$ ")

        if (inp == "backup_files" or inp == "b"):
            print("backing up files....")
            if not os.path.exists(outputPath): os.makedirs(outputPath)
            for file in os.listdir(inputPath): shutil.copy(f'{inputPath}/{file}', outputPath)

        if (inp == "delete" or inp == "d"):
            shutil.rmtree(outputPath)
except KeyboardInterrupt:
    print("Shutting down . . . ")
