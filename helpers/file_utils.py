
import hashlib
import os


def UploadPartToMinio(fileContent, s3,bucket, PartId):
    s3.put_object(
        Bucket=bucket,
        Key=PartId,
        Body=fileContent,
        ContentType='text/plain'
    )
    

    
def GetFileProperties(filePath):
    hashMd5 = hashlib.md5()
    fileSize = os.path.getsize(filePath)
    lineCount = 0
    with open(filePath, 'rb') as f:
        for chunk in iter(lambda: f.read(65000), b""):
            hashMd5.update(chunk)
            lineCount += chunk.count(b'\n')

    #get the root directory of the file
    return hashMd5.hexdigest(), lineCount, fileSize
    

# This function returns a list of locations where the file is divided into parts
def DivideFile(FilePath,maxSizeBytes=100*1024*1024):
    #First get the size of the file
    fileSize = os.path.getsize(FilePath)
    #Then calculate the number of parts
    partCount = fileSize//maxSizeBytes + 1
    parts = []
    # get the closest newline charater to the every part divide point
    for i in range(1,partCount):
        with open(FilePath, 'rb') as infile:
            infile.seek(i*maxSizeBytes)
            line = infile.read(1000)
            newline = line.find(b'\n')
            if newline != -1:
                parts.append(i*maxSizeBytes+newline)
            else:
                parts.append(i*maxSizeBytes)
    return parts

    
    