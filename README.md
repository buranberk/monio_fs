# Monio_fs

Monio_fs (MongoDB Minio Filesystem) is a custom filesystem designed to manage and store file data using MongoDB for metadata and Minio for file parts storage. This project provides an interface to add folders to a database, store file parts in Minio, and manage the filesystem efficiently.

## Features

- **MongoDB Integration**: Store folder and file metadata in a MongoDB database.
- **Minio Integration**: Utilize Minio's S3-compatible APIs to store and retrieve file parts.
- **Customizable**: Configure MongoDB and Minio connections through command-line arguments.
- **Database Management**: Optionally clear the database before adding new data to avoid duplication or outdated entries.

## Installation

### Prerequisites

Before running Monio_fs, ensure you have the following installed:

- Python 3.x
- MongoDB
- Minio
- pip (Python package installer)

### Install Dependencies

To install the required Python libraries, run the following command:

```bash
pip install pymongo boto3
```
Usage
Monio_fs is executed through the monio_fs.py script. The script allows you to specify various options to control how folders are added to the database and how file parts are handled in Minio.

Command-Line Arguments
--folder (-f): Specify the root folder to add to the database.
--mongo (-mo): MongoDB connection string (default: mongodb://localhost:27017/).
--clear (-c): Clear the database before adding the folder.
--minio (-mi): Minio connection string (default: http://localhost:9000).
--accesskey (-ak): Minio access key (required).
--secretkey (-sk): Minio secret key (required).
--bucket (-b): Minio bucket name (default: monio).
--dbname (-db): MongoDB database name (default: Monio).
Example Usage
Here’s an example of how to use the script:
```bash
python monio_fs.py --folder /path/to/your/folder \
                   --mongo mongodb://localhost:27017/ \
                   --minio http://localhost:9000 \
                   --accesskey YOUR_MINIO_ACCESS_KEY \
                   --secretkey YOUR_MINIO_SECRET_KEY \
                   --bucket your-bucket-name \
                   --dbname Monio \
                   --clear
```
