from datetime import datetime
import logging
from typing import Optional
from beanie import PydanticObjectId
import chromadb
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    Settings,
)
from llama_index.readers.database import DatabaseReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from database.user import User

from utils.environment import get_env_var

logger = logging.getLogger(__name__)
remote_db = chromadb.HttpClient(port=8080)

DATABASE_URL = get_env_var("DATABASE_URL")
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
PERSIST_DIR = get_env_var("PERSIST_DIR")

Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


def get_documents(user: User, chat_start_time: Optional[datetime] = None):
    logger.debug("GETTING DOCUMENTS")
    # if not user_id:
    #     return

    # # Initialize DatabaseReader with the SQL database connection details
    # reader = DatabaseReader(
    #     uri="sqlite:///basel.db",
    # )

    # query = f"""
    #     SELECT 'Summary: '|| data ||'" on ' || strftime('%Y-%m-%d', created_at) AS sentence
    #         FROM user_meta WHERE deleted_at IS NULL AND user_id = {user_id} AND created_by = {user_id}
    # """

    # if chat_start_time:
    #     query += f' AND created_at > "{str(chat_start_time)}"'

    # # Load data from the database using a query
    # documents = reader.load_data(query=query)

    # for document in documents:
    #     document.metadata = {"user_id": user_id}

    # return documents


def add_to_index(documents):
    logger.debug("CREATING INDEX")
    chroma_collection = remote_db.get_or_create_collection("user_meta")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(documents, storage_context, show_progress=True)


def reset_index(user_id: PydanticObjectId):
    logger.debug("RESETTING INDEX")
    chroma_collection = remote_db.get_or_create_collection("user_meta")
    chroma_collection.delete(where={"user_id": str(user_id)})


def get_index():
    logger.debug("GETTING INDEX")
    chroma_collection = remote_db.get_or_create_collection("user_meta")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index
