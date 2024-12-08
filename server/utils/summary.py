import logging
from datetime import datetime
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, Field
from database.message import Message


from basel.indexing import (
    add_to_index,
    get_documents,
)
from classes.user_claims import UserClaims
from database.user_meta import UserMeta

logger = logging.getLogger(__name__)


class MetaSummary(BaseModel):
    user_summary: str = Field(
        description="""
        - Summary of topics and details that the user brings up in the conversation between the bot and the user.
        - Excludes topics and details that the bot brings up or seems to have a previous knowledge of.
        - Includes details about the user's career, hobbies, personal interest.
        """
    )


async def create_summary(user_claims: UserClaims, chat_start_time: datetime):
    logs = await Message.find(Message.user == user_claims.user).to_list()

    if not logs:
        return

    logs_story = "\n".join(
        f"{message.sender} at {message.created_at}: {message.text}" for message in logs
    )
    logger.debug(f"LOGS: {logs_story}")

    llm = OpenAI(model="gpt-4o")
    summary = llm.complete(
        f"""
        Objective: Generate a concise summary of new career-related information provided by the user in today’s conversation.

        Instructions:
        - Focus only on facts explicitly shared by the user that relate to their career, skills, goals, qualifications, or personal hobbies/interests.
        - Use the bot's responses as context and do not include information that the bot introduces.
        - Exclude suggestions, questions, or comments made by the bot.
        - Do not repeat information already known or redundant. If there are no new details provided by the user, respond with "None" (without punctuation).
        - Use third person statements, for example: "The user is interested in...."

        # Conversation
        {logs_story}
        """
    )

    logger.debug(f"SUMMARY: {summary}")

    if summary.text and summary.text != "None":
        user_meta = UserMeta(
            user=user_claims.user, data=summary.text  # type:ignore
        ).create()
        # Update Index
        # documents = get_documents(user_claims.user, chat_start_time)
        # add_to_index(documents)
