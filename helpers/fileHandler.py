from helpers.file_utils import GetFileProperties, DivideFile
import os

def HandleFile(FilePath, FilesCollection,PartsCollection,rootDirId=".",maxSizeBytes=100*1024*1024):
    #First get the properties of the file
    HashMd5, LineCount, FileSize = GetFileProperties(FilePath)
    FileName = os.path.basename(FilePath)
    #Dividing the file into parts
    Parts = DivideFile(FilePath,maxSizeBytes)
    # Add the file to the database
    FileId = FilesCollection.insert_one({
        "FileName": FileName,
        "FileHash": HashMd5,
        "LineCount": LineCount,
        "FileSize": FileSize,
        "RootDir": rootDirId
    }).inserted_id
    
    # Add the parts to the database
    for i in range(0,len(Parts)+1):
        if len(Parts) == 0:
            PartSize = FileSize
            StartByte = 0
        elif i == len(Parts):
            PartSize = FileSize - Parts[i-1]
            StartByte = Parts[i-1]
        elif i == 0:
            PartSize = Parts[i]
            StartByte = 0
        else:
            PartSize = Parts[i] - Parts[i-1]
            StartByte = Parts[i-1]
        PartId = PartsCollection.insert_one({
            "FileId": FileId,
            "PartNumber": i,
            "SizeBytes": PartSize,
            "StartByte": StartByte
        }).inserted_id
    return FileId