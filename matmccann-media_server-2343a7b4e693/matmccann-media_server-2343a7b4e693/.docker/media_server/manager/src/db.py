#!/usr/bin/env python3

from pymongo import MongoClient, errors
from utils import ConfigUtil
from bson import ObjectId, json_util

class Db:
    def __init__(self):
        self.config = ConfigUtil().getConfig('/manager/config/db.json')

        try:
            mongoConnectUrl = f'mongodb://{self.config["username"]}:{self.config["password"]}@{self.config["host"]}:{self.config["port"]}/?authSource=admin'
            self.client = MongoClient(mongoConnectUrl, serverSelectionTimeoutMS = 10, connectTimeoutMS = 20000)
            self.db = self.client[self.config["db_name"]]
            self.filePathsCollection = self.db[self.config['file_paths_collection_name']]
        except errors.ConnectionFailure:
            print(f'Could not connec to server at: {mongoConnectUrl}')

    def listDatabaseNames(self):
        return self.client.list_database_names()

    def serverInfo(self):
        return self.client.server_info()

    def listAll(self):
        elems = []
        for elem in self.filePathsCollection.find({}):
            elems.append(elem)
        return elems
        return json_util.dumps(elems)

    def findById(self, id):
        return self.filePathsCollection.find_one({"_id": ObjectId(id)})
    
    def insertOne(self, dictElem):
        return self.filePathsCollection.insert_one(dictElem)

    def dropCollection(self):
        return self.filePathsCollection.drop()

    def clearCollection(self):
        return self.filePathsCollection.delete_many({})

    def insertOne(self, dictElem):
        return self.filePathsCollection.insert_one(dictElem)