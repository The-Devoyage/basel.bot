import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ws import router as ws_router
from routes.role import router as role_router
from routes.auth import router as auth_router

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure App
app = FastAPI()
app.include_router(ws_router)
app.include_router(role_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains if necessary
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # This allows all headers (including Content-Type, etc.)
)


@app.get("/")
def describe_api():
    """
    # Describe the API
    Basel's is a job search platform that helps users with job search and job application.

    Returns
    - version: str

    """
    return {"version": "0.0.0"}
