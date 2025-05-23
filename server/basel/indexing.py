from datetime import datetime
import logging
from typing import List, Optional
from beanie import PydanticObjectId
import chromadb
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    Settings,
)
from llama_index.readers.mongodb import SimpleMongoReader

from llama_index.readers.s3 import S3Reader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from database.user import User
from database.file import File

from utils.environment import get_env_var

logger = logging.getLogger(__name__)
remote_db = chromadb.HttpClient(port=8080)

# Constants
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
DB_URI = get_env_var("DB_URI")
DB_DATABASE = get_env_var("DB_DATABASE")
DB_HOST = get_env_var("DB_HOST")
DB_PORT = get_env_var("DB_PORT")
VULTR_S3_SECRET_KEY = get_env_var("VULTR_S3_SECRET_KEY")
VULTR_S3_ACCESS_KEY = get_env_var("VULTR_S3_ACCESS_KEY")
VULTR_S3_BUCKET = get_env_var("VULTR_S3_BUCKET")
VULTR_S3_HOSTNAME = get_env_var("VULTR_S3_HOSTNAME")

Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(
    model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.3, streaming=True
)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


def create_s3_documents(user: User, files: List[File]):
    logger.debug("INDEX S3 DOCUMENTS")

    if not files:
        return

    file_collection = remote_db.get_or_create_collection("file")

    file_documents = []

    for file in files:
        docs = file_collection.get(where={"file_uuid": str(file.uuid)})
        if docs and "documents" in docs and len(docs["documents"]) > 0:  # type:ignore
            logger.debug("FILE ALREADY INDEXED")
            continue
        else:
            logger.debug(f"INDEXING NEW FILE: {file}")
            loader = S3Reader(
                bucket=VULTR_S3_BUCKET,
                key=file.key,
                aws_access_id=VULTR_S3_ACCESS_KEY,
                aws_access_secret=VULTR_S3_SECRET_KEY,
                s3_endpoint_url="https://" + VULTR_S3_HOSTNAME,
            )
            documents = loader.load_data()
            for document in documents:
                document.metadata = {
                    "user_id": str(user.id),
                    "file_uuid": str(file.uuid),
                }
            file_documents.extend(documents)

    if file_documents:
        add_index(file_documents, "file")


def get_documents(user: User, chat_start_time: Optional[datetime] = None):
    logger.debug("GETTING DOCUMENTS")
    if not user:
        return

    reader = SimpleMongoReader(host=DB_HOST, port=int(DB_PORT), uri=DB_URI)

    query_dict = {
        "user": {"$ref": "User", "$id": user.id},
        "status": True,
        "deleted_at": None,
    }
    if chat_start_time:
        query_dict["created_at"] = {"$gt": chat_start_time}

    # Get Meta from DB
    meta_documents = reader.load_data(
        db_name=DB_DATABASE,
        collection_name="UserMeta",  # Name of the collection
        field_names=[
            "data",
            "created_at",
        ],
        # separator="",  # Separator between fields (default: "")
        query_dict=query_dict,
        # max_docs=0,  # Maximum number of documents to load (default: 0)
        # metadata_names=None,  # Names of the fields to add to metadata attribute (default: None)
    )

    # Add meta index
    for document in meta_documents:
        document.metadata = {"user_id": str(user.id)}

    return meta_documents


def add_index(documents, collection: str):
    logger.debug("CREATING INDEX")
    chroma_collection = remote_db.get_or_create_collection(collection)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(documents, storage_context, show_progress=True)


def reset_index(user_id: PydanticObjectId):
    logger.debug("RESETTING INDEX")
    chroma_collection = remote_db.get_or_create_collection("user_meta")
    chroma_collection.delete(where={"user_id": str(user_id)})


def get_index(collection: str):
    chroma_collection = remote_db.get_or_create_collection(collection)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index
