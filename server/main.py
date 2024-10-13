import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from routes.ws import router as ws_router

app = FastAPI()

app.include_router(ws_router)

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.get("/")
def describe_api():
    """
    # Describe the API
    Basel's is a job search platform that helps users with job search and job application.

    Returns
    - version: str

    """
    return {"version": "0.0.0"}
