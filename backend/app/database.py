# backend/app/database.py

import os
from pymongo import MongoClient

# Fetch connection details from environment variables
MONGO_HOST = os.getenv("MONGO_HOST", "db") 
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USERNAME")
MONGO_PASS = os.getenv("MONGO_PASSWORD")
DATABASE_NAME = "prototype_db"

# Construct the MongoDB Connection URI
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"

# Global database client and database object
client = None
db = None

def connect_to_mongo():
    """Initializes the MongoDB client and database connection."""
    global client, db
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        
        # Select the database
        db = client[DATABASE_NAME]
        
        # Test connection by listing databases (optional)
        print(f"✅ MongoDB Connection Successful. Using database: {DATABASE_NAME}")

        # --- Return the connected objects ---
        return client, db
    
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")
        return None, None # Return Nones on failure


def close_mongo_connection():
    """Closes the MongoDB client connection."""
    global client
    if client:
        client.close()
        print("🔌 MongoDB Connection Closed.")