from llama_index.agent.openai.openai_assistant_agent import logging
from llama_index.core.tools import FunctionTool
from llama_index.core.vector_stores.types import (
    FilterOperator,
    MetadataFilter,
    MetadataFilters,
)
from pydantic import BaseModel, Field
from basel.indexing import get_index
from database.user import User

logger = logging.getLogger(__name__)


class ReadFileToolParams(BaseModel):
    file_uuid: str = Field(description="The UUID of the associated file to read.")
    prompt: str = Field(
        description="The question or prompt of what to extract from the file."
    )


async def read_file(file_uuid: str, user: User, prompt: str):
    logger.debug(f"READ FILE: {file_uuid}")
    index = get_index("file")

    filters = MetadataFilters(
        filters=[
            MetadataFilter(
                key="user_id", operator=FilterOperator.EQ, value=str(user.id)
            ),
            MetadataFilter(
                key="file_uuid", operator=FilterOperator.EQ, value=file_uuid
            ),
        ]
    )
    query_engine = index.as_query_engine(
        fiters=filters,
        similarity_top_k=5,
    )
    response = await query_engine.aquery(prompt)
    return response


def create_read_s3_tool(user: User):
    file_reader_tool = FunctionTool.from_defaults(
        name="read_file_tool",
        async_fn=lambda file_uuid, prompt: read_file(
            file_uuid=file_uuid, user=user, prompt=prompt
        ),
        description="""
            Read files that the user has uploaded in order to provide context to the conversation.
            """,
        fn_schema=ReadFileToolParams,
    )

    return file_reader_tool
