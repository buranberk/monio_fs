from helpers.folderHandler import HandleFolder

if __name__ == "__main__":
    from pymongo import MongoClient
    import boto3
    from botocore.client import Config
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder","-f", help="Root folder to add to the database")
    parser.add_argument("--mongo","-mo", help="MongoDB connection string (default is mongodb://localhost:27017/)",default="mongodb://localhost:27017/")
    parser.add_argument("--clear","-c", help="Clear the database before adding the folder",action="store_true")
    parser.add_argument("--minio","-mi",help="Minio connection string (default is http://localhost:9000)",default="http://localhost:9000")
    parser.add_argument("--accesskey","-ak",help="Minio access key (required)")
    parser.add_argument("--secretkey","-sk",help="Minio secret key (required)")
    parser.add_argument("--bucket","-b",help="Minio bucket name (default is monio)",default="monio")
    parser.add_argument("--dbname","-db", help="Database name (default is Monio)",default="Monio")


    

    args = parser.parse_args()
    
    if not args.accesskey or not args.secretkey:
        print("Please provide access key and secret key for minio")
        print("Use -h for help")
        exit()

    s3 = boto3.client('s3',
                  endpoint_url=args.minio,
                  aws_access_key_id=args.accesskey,
                  aws_secret_access_key=args.secretkey,
                  config=Config(signature_version='s3v4'))
    
    # chech if bucekt exists
    try:
        s3.head_bucket(Bucket=args.bucket)
    except:
        print(f"Bucket {args.bucket} does not exist")
        exit()
    

    client = MongoClient(args.mongo)
    db = client[args.dbname]
    folderCollection = db["folders"]
    filesCollection = db["files"]
    partsCollection = db["parts"]
    # clear the database
    if args.clear:
        folderCollection.delete_many({})
        filesCollection.delete_many({})
        partsCollection.delete_many({})
        s3.delete_objects(Bucket=args.bucket,Delete={"Objects":[{"Key":obj["Key"]} for obj in s3.list_objects(Bucket=args.bucket)["Contents"]]})
    # list buckets 


    if args.folder:
        HandleFolder(args.folder,folderCollection,filesCollection,partsCollection,s3=s3,recursive=True)
    else:
        print("Please provide a folder to add to the database")
        print("Use -h for help")