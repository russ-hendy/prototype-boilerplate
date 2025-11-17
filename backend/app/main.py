from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create the FastAPI app instance
app = FastAPI(
    title="Prototype Boilerplate API",
    version="0.1.0",
)

# -------------------------------------------------------------
# 1. CORS Configuration (Crucial for Local Development)
# -------------------------------------------------------------

# For local development, the frontend (http://localhost:5173) is different 
# from the backend (http://localhost:8000), which requires CORS.
# In production with Caddy/subdomains, this might change, but for now, 
# allowing all origins is safest for development.

origins = [
    # Allows requests from your local Vue development server (port 5173)
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    # Allow all origins for simplicity in this prototype. 
    # Use 'origins' list above for a tighter setup.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# 2. Basic Endpoint
# -------------------------------------------------------------

@app.get("/")
def read_root():
    """
    Root endpoint for a simple health check.
    """
    return {"message": "Hello from the FastAPI Backend! Dockerized and Ready."}


# -------------------------------------------------------------
# 3. MongoDB Connection Stub (Placeholder)
# -------------------------------------------------------------
# You can use this to quickly test environment variables loaded from .env/docker-compose
@app.get("/db-check")
def db_check():
    """
    Endpoint to confirm the database environment variables are loaded.
    """
    # These variables are pulled from your docker-compose.yml environment block
    mongo_host = os.getenv("MONGO_HOST")
    mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    
    return {
        "status": "DB config loaded",
        "host": mongo_host,
        "user": mongo_user,
        "note": "Actual connection logic (e.g., using pymongo) would go here."
    }