from helpers.folderHandler import HandleFolder
from helpers.fileHandler import HandleFile
from pymongo import MongoClient
import boto3
from botocore.client import Config

class MonioHandle:

    def __init__(self,MongoCreds,MinioCreds) -> None:
        self.mongo=MongoClient(MongoCreds["url"])
        self.db=self.mongo[MongoCreds["dbName"]]

        self.foldersCollection=self.db["folders"]
        self.filesCollection=self.db["files"]
        self.partsCollection=self.db["parts"]

        if MongoCreds["accessKey"] is not None and MongoCreds["accessKey"] is not None:
            self.minio=boto3.client('s3',
                    endpoint_url=MinioCreds["url"],
                    aws_access_key_id=MinioCreds["accessKey"],
                    aws_secret_access_key=MinioCreds["secretKey"],
                    config=Config(signature_version='s3v4'))
            self.bucket=MongoCreds["bucket"]
        else:
            self.minio=None
            self.bucket=None

    
    def set_bucket(self,bucketname) -> None:
        if self.check_bucket(bucketname):
            self.bucket=bucketname

    def check_bucket(self,bucketname) -> bool:
        try:
            self.minio.head_bucket(Bucket=bucketname)
            return True
        except:
            return False
        
    def clear_dbs(self) -> None:
        if self.foldersCollection is not None:
            self.foldersCollection.delete_many({})
        if self.filesCollection is not None:
            self.filesCollection.delete_many({})
        if self.partsCollection is not None:
            self.partsCollection.delete_many({})
        if self.check_bucket(self.bucket):
            objects={"Objects":[{"Key":obj["Key"]} for obj in self.minio.list_objects(Bucket=self.bucket)["Contents"]]}
            if len(objects["Objects"])>0:
                self.minio.delete_objects(Bucket=self.bucket,Delete=objects)

    def add_folder(self,folderPath,recursive=True) -> str:
        res=HandleFolder(folderPath,self.foldersCollection,self.filesCollection,self.partsCollection,self.minio,recursive=recursive,bucket=self.bucket)
        return res



