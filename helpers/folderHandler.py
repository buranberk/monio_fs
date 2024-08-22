from helpers.fileHandler import HandleFile
import os

def HandleFolder(folderPath,folderCollection,filesCollection,partsCollection,rootDirId="root",recursive=False):
    # Check if the folder exists
    if not os.path.exists(folderPath):
        return "Folder does not exist"
    
    # inster the folder to the database
    rootId = folderCollection.insert_one({
        "folderPath": folderPath,
        "rootDir": rootDirId
    }).inserted_id
    # Get the list of files and folders in the folder
    # If recursive is true, get the list of all files and folders in the folder
    # but not the subfolders
    # Add the files and folders to the database



    if recursive:
        folders = [f for f in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, f))]
        for folder in folders:
            HandleFolder(os.path.join(folderPath,folder),folderCollection,filesCollection,partsCollection,rootId,True)
    # get all the files in the folder and add them to the database

    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]
    for file in files:
        filePath = os.path.join(folderPath,file)
        HandleFile(filePath,filesCollection,partsCollection,rootId)
        
    return rootId

