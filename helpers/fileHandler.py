from helpers.file_utils import GetFileProperties, DivideFile, UploadPartToMinio
import os

def HandleFile(FilePath, FilesCollection,PartsCollection,s3=None,bucket=None,rootDirId=".",maxSizeBytes=100*1024*1024):
    #First get the properties of the file
    HashMd5, LineCount, FileSize = GetFileProperties(FilePath)
    FileName = os.path.basename(FilePath)
    #Dividing the file into parts
    Parts = DivideFile(FilePath,maxSizeBytes)
    part_list = []
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
        part_list.append({"PartId":PartId.__str__(),"StartByte":StartByte,"SizeBytes":PartSize})
    if s3 is not None and bucket is not None:
        with open(FilePath, 'rb') as infile:
            for part in part_list:
                infile.seek(part["StartByte"])
                partContent = infile.read(part["SizeBytes"])
                UploadPartToMinio(partContent,s3,bucket,part["PartId"])


    return FileId