from helpers.fileHandler import HandleFile
import os

def HandleFolder(folderPath,folderCollection,filesCollection,partsCollection,s3=None,rootDirId="root",recursive=False,bucket="monio"):
    # Check if the folder exists
    if not os.path.exists(folderPath):
        return Exception("Folder does not exist")
    
    rootId = folderCollection.insert_one({
        "folderPath": folderPath,
        "rootDir": rootDirId
    }).inserted_id



    if recursive:
        folders = [f for f in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, f))]
        for folder in folders:
            HandleFolder(os.path.join(folderPath,folder),folderCollection,filesCollection,partsCollection,s3,rootId,True,bucket)
    # get all the files in the folder and add them to the database

    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
    for file in files:
        filePath = os.path.join(folderPath,file)
        HandleFile(filePath,filesCollection,partsCollection,s3,bucket,rootId)
        
    return rootId

