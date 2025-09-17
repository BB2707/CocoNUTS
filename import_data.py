import os
import json
from pymongo import MongoClient

def import_plant_data():
    """
    Connects to MongoDB Atlas and imports plant data from a local JSON file.
    """
    # --- Configuration ---
    # IMPORTANT: Replace this with your actual MongoDB connection string
    # It's recommended to use an environment variable for this in production.
    MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING", "YOUR_MONGODB_CONNECTION_STRING_HERE")
    DB_NAME = "CocoNUTbase"
    COLLECTION_NAME = "plants"
    JSON_FILE_PATH = "plant_data.json"

    # --- Validation ---
    if "YOUR_MONGODB" in MONGO_CONNECTION_STRING:
        print("FATAL ERROR: MongoDB connection string has not been set.")
        print("Please edit this script and replace 'YOUR_MONGODB_CONNECTION_STRING_HERE' with your actual connection string from Atlas.")
        return

    if not os.path.exists(JSON_FILE_PATH):
        print(f"FATAL ERROR: The data source file '{JSON_FILE_PATH}' was not found.")
        return

    # --- Connection and Import ---
    try:
        print("Connecting to MongoDB Atlas...")
        client = MongoClient(MONGO_CONNECTION_STRING)
        
        # Verify the connection
        client.admin.command('ping')
        print("MongoDB connection successful.")
        
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Check if the collection already has data
        if collection.count_documents({}) > 0:
            print(f"Collection '{COLLECTION_NAME}' already contains data. Clearing it first.")
            collection.delete_many({})

        # Load data from the JSON file
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)

        # Insert data into the collection
        print(f"Inserting {len(data)} documents into '{COLLECTION_NAME}'...")
        collection.insert_many(data)
        
        print("\nData import successful!")
        print(f"Total documents in collection: {collection.count_documents({})}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")


if __name__ == '__main__':
    import_plant_data()

