from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.core.tools.types import ToolMetadata
from llama_index.core.vector_stores.types import (
    FilterOperator,
    MetadataFilter,
    MetadataFilters,
)

from basel.indexing import get_index
from database.user import User


def create_candidate_profile_tool(chatting_with_id: User):
    index = get_index()

    filters = MetadataFilters(
        filters=[
            MetadataFilter(
                key="user_id",
                operator=FilterOperator.EQ,
                value=str(chatting_with_id.id),
            )
        ]
    )

    candidate_profile_tool = QueryEngineTool(
        query_engine=index.as_query_engine(similarity_top_k=5, filters=filters),
        metadata=ToolMetadata(
            name="candidate_profile",
            description="""
            Provides information about the candidate that you represent. 
            Useful to answer questions about the candidate's career, job search, etc.
            Note, this already filters the index by the candidate user.
            """,
        ),
    )

    return candidate_profile_tool
