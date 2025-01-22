import pymongo
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
import json
from pathlib import Path
from bson import ObjectId

# Get the backend directory path
backend_dir = Path(__file__).resolve().parents[2]
load_dotenv(backend_dir / ".env")

# Custom JSON encoder to handle ObjectId
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def verify_connection():
    try: 
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
    except Exception as e:
        print("Exception occurred: %s" % e)

def verify_database():
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        existing_databases = client.list_database_names()

        database_name = os.environ['MONGODB_DATABASE']
        if database_name in existing_databases:
            print(f"Database '{database_name}' already exists.")
        else:
            print(f"Database '{database_name}' does not exist. Creating...")
            database = client[database_name]
            collection_name = os.environ['MONGODB_COLLECTION']
            database.create_collection(collection_name)
            print(f"Database '{database_name}' created successfully. Collection '{collection_name}' created successfully.")
    
    except Exception as e:
        print("Exception occurred: %s" % e)

def retrieve_reddit_posts():
    retrieved_posts = []
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client[os.environ['MONGODB_DATABASE']]
        collection = db[os.environ['MONGODB_COLLECTION']]
        cursor = collection.find({})
        for document in cursor:
            retrieved_posts.append(document)
    except Exception as e:
        print(f"Error retrieving posts from MongoDB: {e}")
    finally:
        client.close()
    return retrieved_posts

def export_mongodb_as_json():
    try:
        # Get data directories
        data_dir = backend_dir / "data"
        raw_dir = data_dir / "raw"
        
        # Create directories if they don't exist
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Get posts from MongoDB
        posts = retrieve_reddit_posts()
        
        if posts:
            # Save to JSON file using custom encoder
            output_file = raw_dir / "reddit_data.json"
            with open(output_file, 'w') as f:
                json.dump(posts, f, indent=2, cls=MongoJSONEncoder)
            print(f"Successfully exported {len(posts)} posts to {output_file}")
        else:
            print("No posts found to export")
            
    except Exception as e:
        print(f"Error exporting data: {str(e)}")

if __name__ == "__main__":
    export_mongodb_as_json()