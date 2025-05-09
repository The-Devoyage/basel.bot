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
from routes.notification import router as notification_router
from routes.suggest import router as suggest_router
from routes.file import router as file_router
from routes.user import router as user_router
from routes.organization import router as organization_router
from routes.interview_question import router as interview_question_router
from routes.interview_assessment import router as interview_assessment_router
from routes.message import router as message_router

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
app.include_router(interview_router, prefix="/interview")
app.include_router(onboarding_router)
app.include_router(mailer_router, prefix="/mailer")
app.include_router(standup_router)
app.include_router(notification_router)
app.include_router(suggest_router)
app.include_router(file_router, prefix="/file")
app.include_router(user_router, prefix="/user")
app.include_router(organization_router, prefix="/organization")
app.include_router(interview_question_router, prefix="/interview-question")
app.include_router(interview_assessment_router, prefix="/interview-assessment")
app.include_router(message_router, prefix="/message")

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
    return {"version": "0.0.10"}
