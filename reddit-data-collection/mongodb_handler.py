import pymongo
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

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

def check_post_exists(post_id):
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client[os.environ['MONGODB_DATABASE']]
        collection = db[os.environ['MONGODB_COLLECTION']]
        
        # Check if post exists by id
        exists = collection.count_documents({"id": post_id}) > 0
        return exists
        
    except Exception as e:
        print(f"Error checking post existence in MongoDB: {e}")
        return False
    finally:
        client.close()

def insert_reddit_post(post_data):
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client[os.environ['MONGODB_DATABASE']]
        collection = db[os.environ['MONGODB_COLLECTION']]
        
        # Insert the post data
        result = collection.insert_one(post_data)
        print(f"Successfully inserted post with ID: {result.inserted_id}")
        return result.inserted_id
        
    except Exception as e:
        print(f"Error inserting post to MongoDB: {e}")
        return None
    finally:
        client.close()

if __name__ == "__main__":
    '''use this file to test connection and database creation'''
    verify_connection()
    verify_database()