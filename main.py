from helpers.folderHandler import HandleFolder
from helpers.handle import MonioHandle

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--folder","-f", help="Root folder to add to the database (required)")
    parser.add_argument("--mongo","-mo", help="MongoDB connection string (default is mongodb://localhost:27017/)",default="mongodb://localhost:27017/")
    parser.add_argument("--clear","-c", help="Clear the database before adding the folder",action="store_true")
    parser.add_argument("--minio","-mi",help="Minio connection string (default is http://localhost:9000)",default="http://localhost:9000")
    parser.add_argument("--accesskey","-ak",help="Minio access key (required)",default=None)
    parser.add_argument("--secretkey","-sk",help="Minio secret key (required)",default=None)
    parser.add_argument("--bucket","-b",help="Minio bucket name (default is monio)",default="monio")
    parser.add_argument("--dbname","-db", help="Database name (default is monio)",default="monio")


    

    args = parser.parse_args()
    mongocreds={"url":args.mongo,"dbName":args.dbname}
    miniocreds={"url":args.minio,"accesskey":args.accesskey,"secretkey":args.scretkey,"bucket":args.bucket}
    handle=MonioHandle(mongocreds,miniocreds)
    
    # chech if bucekt exists
    if not handle.check_bucket(args.bucket):
        print(f"Bucket {args.bucket} does not exist")
        exit()
    

    # clear the database if -c
    if args.clear:
        handle.clear_dbs()


    if args.folder:
        handle.add_folder(args.folder,recursive=True)
    else:
        print("Please provide a folder to add to the database")
        print("Use -h for help")