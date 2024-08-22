from helpers.folderHandler import HandleFolder

if __name__ == "__main__":
    from pymongo import MongoClient
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="Root folder to add to the database")
    parser.add_argument("--mongo", help="MongoDB connection string",default="mongodb://localhost:27017/")
    parser.add_argument("--dbname", help="Database name",default="Monio")

    args = parser.parse_args()

    client = MongoClient(args.mongo)
    db = client[args.dbname]
    folderCollection = db["folders"]
    filesCollection = db["files"]
    partsCollection = db["parts"]


    if args.folder:
        HandleFolder(args.folder,folderCollection,filesCollection,partsCollection,recursive=True)
    else:
        print("Please provide a folder to add to the database")