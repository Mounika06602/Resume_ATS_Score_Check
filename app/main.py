"""
FastAPI application initializer and middleware setup.

This module sets up the core FastAPI application configuration, handles cross-origin
resource sharing (CORS), registers sub-routers, and mounts static web directories for the
client-side dashboard UI.
"""

import os
import sys

# Add the project root directory to the python path to enable package-level imports
# when executing this file directly (e.g. 'python app/main.py')
if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api import routes

# Load key-value configuration variables from the root .env file
load_dotenv()

# Initialize the main FastAPI application configuration metadata
app = FastAPI(title="Resume ATS Checker API", version="1.0.0")

# Setup CORS middleware to allow cross-origin requests from the client dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the modular endpoint sub-router under the '/api' prefix
app.include_router(routes.router, prefix="/api")

# Mount the static directory to serve the frontend client HTML, CSS, and JS assets at '/'
# We resolve the static folder path relative to the root folder (two levels up from this file)
static_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"))
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    
    # Retrieve port from configurations
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Resume ATS Checker FastAPI server on port {port}...")
    
    # Run the uvicorn development server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_excludes=["venv", "venv/**/*", ".venv", ".venv/**/*"]
    )
