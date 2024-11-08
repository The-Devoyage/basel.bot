import logging

from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.core.tools.types import ToolMetadata
from llama_index.readers.database import DatabaseReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent

from utils.environment import get_env_var

logger = logging.getLogger(__name__)

DATABASE_URL = get_env_var("DATABASE_URL")
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")

Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


def get_documents(user_id: int | None):
    if not user_id:
        return

    # Initialize DatabaseReader with the SQL database connection details
    reader = DatabaseReader(
        uri="sqlite:///basel.db",
    )

    # Load data from the database using a query
    documents = reader.load_data(
        # query=f"SELECT data, created_at FROM user_meta WHERE user_id = {user_id};"
        # query=f"""
        #     SELECT ''|| sender ||' said "' || text || '" on ' || strftime('%Y-%m-%d', created_at) AS sentence
        #     FROM message WHERE user_id = {user_id};
        # """
        query=f"""
        SELECT 'Summary: '|| data ||'" on ' || strftime('%Y-%m-%d', created_at) AS sentence
            FROM user_meta WHERE user_id = {user_id} AND created_by = {user_id};
        """
    )

    logger.info(f"GET DOCS: {documents}")
    return documents


def get_agent(documents, is_candidate) -> OpenAIAgent:
    index = VectorStoreIndex.from_documents(
        documents,
    )
    tool = QueryEngineTool(
        query_engine=index.as_query_engine(similarity_top_k=5),
        metadata=ToolMetadata(
            name="candidate_profile",
            description="Provides information about you, the bot representing the candiate. Useful to answer questions about the candidate's career, job search, etc.",
        ),
    )

    prompt = """
       You are a bot representing the candidate.

       You are currently conversting with the candidate that you represent.

       Your name is Basel, you are respectful, professional, helpful, and friendly.
       You help match candidates with employers by learning about the candidates skills, career goals, personal life and hobbies.
       Your personality is a warm extrovert. Slightly gen alpha.

       Your job is to ask questions about the candidate to learn about their skills, career goals, 
       and personal life/hobbies. As you progress through the conversation, try to ask more technical questions
       to get an idea of the users skill level.

       Call the candidate_profile tool to get historical information about the candidate.
    """

    if is_candidate is False:
        prompt = """
            You are a bot representing the candidate.

            You are currently conversting with the employer or recruiter that wants to ask questions about the candidate that you represent.

            Your name is Basel, you are respectful, professional, helpful, and friendly.
            You help match candidates with employers by learning about the candidates skills, career goals, personal life and hobbies.
            Your personality is a warm extrovert. Slightly gen alpha.

            Your job is to call and use the candidate_profile tool to get historical information about the candidate in order
            to answer questions that the recruiter asks you.

            Call the candidate_profile tool to get historical information about the candidate.
        """

    agent = OpenAIAgent.from_tools([tool], verbose=True, system_prompt=prompt)
    return agent
