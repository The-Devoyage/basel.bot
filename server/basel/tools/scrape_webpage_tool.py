from enum import Enum
from llama_index.core import VectorStoreIndex
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.vector_stores.types import (
    FilterOperator,
    MetadataFilter,
    MetadataFilters,
)
from llama_index.readers.web import FireCrawlWebReader
from llama_index.readers.web.async_web.base import logging
from basel.indexing import add_index, get_index, remote_db

from utils.environment import get_env_var

logger = logging.getLogger(__name__)

# Constants
FIRE_CRAWL_API_KEY = get_env_var("FIRE_CRAWL_API_KEY")


class ScrapeModeParam(str, Enum):
    SCRAPE = "scrape"
    CRAWL = "crawl"


class ScrapeWebpageToolParams(BaseModel):
    url: str = Field(description="A url or webpage to scrape.")
    prompt: str = Field(
        description="Prompt or question to answer about the scraped URL Data."
    )
    mode: ScrapeModeParam = Field(
        description="""
        Scrape a single page or crawl all nested pages. Default to scrape unless requested to crawl.
        """
    )


async def scrape_webpage(url: str, prompt: str, mode: ScrapeModeParam):
    chroma_collection = remote_db.get_or_create_collection("scraped_webpages")
    docs = chroma_collection.get(where={"url": str(url)})
    logger.debug(f"CHROMA DOCS COUNT: {len(docs)}")
    logger.debug(f"CHROMA DOCS: {docs}")

    if docs and "documents" in docs and len(docs["documents"]) > 0:  # type:ignore
        logger.debug("USING EXISTING SCRAPED DATA")
        index = get_index("scraped_webpages")
        filters = MetadataFilters(
            filters=[
                MetadataFilter(key="url", operator=FilterOperator.EQ, value=str(url))
            ]
        )
        query_engine = index.as_query_engine(filters=filters)
    else:
        logger.debug("CREATING NEW SCRAPED DATA")
        params = None

        if mode == ScrapeModeParam.CRAWL:
            params = {"limit": 20}
        firecrawl_reader = FireCrawlWebReader(
            api_key=FIRE_CRAWL_API_KEY, mode=mode, params=params
        )
        # Load documents from a single page URL
        documents = firecrawl_reader.load_data(url=url)

        for document in documents:
            document.metadata = {"url": str(url)}

        add_index(documents, "scraped_webpages")

        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()

    response = query_engine.query(prompt)
    return response


scrape_webpage_tool = FunctionTool.from_defaults(
    name="scrape_webpage_tool",
    description="""
        Useful to scrape webpages submitted by user. Returns scraped data.
        """,
    async_fn=scrape_webpage,
    fn_schema=ScrapeWebpageToolParams,
)
