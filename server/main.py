import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.init import init_db
from routes.ws import router as ws_router
from routes.role import router as role_router
from routes.auth import router as auth_router
from routes.shareable_link import router as shareable_links_router
from routes.subscription import router as subscription_router
from routes.index import router as index_router
from routes.user_meta import router as user_meta_router
from routes.interview import router as interview_router
from routes.onboarding import router as onboarding_router
from routes.mailer import router as mailer_router
from routes.standup import router as standup_router

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Init DB
@asynccontextmanager
async def lifespan(_: FastAPI):
    client = await init_db()
    yield
    client.close()


# Configure App
app = FastAPI(lifespan=lifespan)
app.include_router(ws_router)
app.include_router(role_router)
app.include_router(auth_router)
app.include_router(shareable_links_router)
app.include_router(subscription_router)
app.include_router(index_router)
app.include_router(user_meta_router)
app.include_router(interview_router)
app.include_router(onboarding_router)
app.include_router(mailer_router, prefix="/mailer")
app.include_router(standup_router)

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
    return {"version": "0.0.3"}
