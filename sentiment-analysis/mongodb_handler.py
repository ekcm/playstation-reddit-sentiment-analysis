import pymongo
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
import json

load_dotenv("../.env")

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
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client[os.environ['MONGODB_DATABASE']]
        collection = db[os.environ['MONGODB_COLLECTION']]
        
        cursor = collection.find({}, {'_id': 0})  
        data = list(cursor)
        
        # Create output directory if it doesn't exist
        output_dir = '../data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create filename with timestamp
        filename = f"{output_dir}/reddit_data_2025_01_19.json"
        
        # Write to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully exported {len(data)} documents to {filename}")
        return filename
        
    except Exception as e:
        print(f"Error exporting MongoDB data to JSON: {e}")
        return None
    finally:
        client.close()

if __name__ == "__main__":
    # verify_connection()
    # verify_database()
    # retrieved_posts = retrieve_reddit_posts()
    # print(retrieved_posts)

    export_mongodb_as_json()