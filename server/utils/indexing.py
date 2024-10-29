import logging

from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.readers.database import DatabaseReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from utils.environment import get_env_var

logger = logging.getLogger(__name__)

DATABASE_URL = get_env_var("DATABASE_URL")
GOOGLE_API_KEY = get_env_var("GOOGLE_API_KEY")
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")

logger.debug(f"OPENAIKEY: {OPENAI_API_KEY}")

gemini_embedding_model = GeminiEmbedding(
    model_name="models/embedding-001", api_key=GOOGLE_API_KEY
)
llm = Gemini(
    model_name="models/gemini-1.5-flash-latest",
)

# Settings.llm = llm
# Settings.embed_model = gemini_embedding_model
Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


def get_documents(user_id):
    # Initialize DatabaseReader with the SQL database connection details
    reader = DatabaseReader(
        uri="sqlite:///basel.db",
    )

    # Load data from the database using a query
    documents = reader.load_data(
        query=f"SELECT data, created_at FROM user_meta WHERE user_id = {user_id};"
    )

    logger.info(f"GET DOCS: {documents}")
    return documents


def get_query_engine(documents) -> BaseChatEngine:
    index = VectorStoreIndex.from_documents(
        documents,
    )
    return index.as_chat_engine(verbose=True)


def query_candidate_profile(prompt: str, query_engine: BaseChatEngine):
    """
    This function allows you to ask the users bot questions about their career, job search, etc.

    args:
        prompt: str
            The prompt to ask the bot representing the user you are chatting with.
    """
    logger.info(f"Prompt: {prompt}")
    response = query_engine.chat(prompt)
    logger.info(f"Response: {response}")
    return response.response
