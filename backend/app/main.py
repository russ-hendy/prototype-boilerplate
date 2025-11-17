from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import connect_to_mongo, close_mongo_connection
from .security import require_auth

# Read environment variable to decide whether to expose documentation
EXPOSE_DOCS = os.getenv("EXPOSE_DOCS", "true").lower() == "true"
DOCS_URL = "/docs" if EXPOSE_DOCS else None
REDOC_URL = "/redoc" if EXPOSE_DOCS else None

# Create the FastAPI app instance
app = FastAPI(
    title="Prototype Boilerplate API",
    version="0.1.0",
    # Pass the variables to FastAPI
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
)

# -------------------------------------------------------------
# 1. CORS Configuration
# -------------------------------------------------------------

# Read the allowed origin from the environment variable
allowed_origin = os.getenv("CORS_ORIGIN", "http://localhost:5173") # Default for safety

origins = [allowed_origin]

app.add_middleware(
    CORSMiddleware,
    # Allow all origins for simplicity in this prototype. 
    # Use 'origins' list above for a tighter setup.
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# 2. Startup/Shutdown Events
# -------------------------------------------------------------

@app.on_event("startup")
def startup_db_client():
    """Connect to MongoDB when the API starts."""
    # The connect function now returns the client and db objects
    mongo_client, mongo_db = connect_to_mongo() 
    
    # --- CRITICAL CHANGE: Attach objects to the FastAPI app instance ---
    app.mongodb_client = mongo_client
    app.database = mongo_db 
    
    if app.database is None:
        print("FATAL: Database object is None after connection attempt.")

@app.on_event("shutdown")
def shutdown_db_client():
    """Close MongoDB connection using the client attached to the app."""
    if hasattr(app, "mongodb_client"):
        app.mongodb_client.close()
        print("🔌 MongoDB Connection Closed.")


# -------------------------------------------------------------
# 3. Basic Endpoint
# -------------------------------------------------------------

@app.get("/")
def read_root():
    """
    Root endpoint for a simple health check.
    """
    return {"message": "Hello from the FastAPI Backend! Dockerized and Ready."}


@app.get("/items")
def get_items():
    """
    Example endpoint to fetch data from the MongoDB 'items' collection.
    """
    mongo_db = app.database 
    
    if mongo_db is None:
        return {"error": "Database not connected. (Check startup logs!)"}, 500
        
    items_collection = mongo_db.items
    
    # Find all documents (returning as a list)
    items_cursor = items_collection.find({})
    
    # Convert MongoDB BSON objects to JSON-serializable dictionaries
    items_list = []
    for item in items_cursor:
        # Convert the MongoDB ObjectID to a string for JSON serialization
        item['_id'] = str(item['_id'])
        items_list.append(item)
        
    return {"count": len(items_list), "data": items_list}

@app.get("/secure-items", dependencies=[Depends(require_auth)])
def get_items_secure():
    """
    This endpoint requires a valid Firebase token in the Authorization header.
    """
    # If the function is reached, the user is authenticated (or auth is disabled)
    # The logic here is identical to /items, but protected.
    mongo_db = app.database 
    items_collection = mongo_db.items
    items_cursor = items_collection.find({})
    
    # Convert MongoDB BSON objects to JSON-serializable dictionaries
    items_list = []
    for item in items_cursor:
        # Convert the MongoDB ObjectID to a string for JSON serialization
        item['_id'] = str(item['_id'])
        items_list.append(item)
        
    return {"count": len(items_list), "data": items_list}