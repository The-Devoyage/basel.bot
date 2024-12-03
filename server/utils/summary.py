import json
import logging
from datetime import datetime
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, Field


from basel.indexing import (
    add_to_index,
    get_documents,
)
from classes.user_claims import UserClaims
from database.message import MessageModel
from database.user_meta import UserMetaModel

logger = logging.getLogger(__name__)

# Database
user_meta_model = UserMetaModel("basel.db")
message_model = MessageModel("basel.db")


class MetaSummary(BaseModel):
    user_summary: str = Field(
        description="""
        - Summary of topics and details that the user brings up in the conversation between the bot and the user.
        - Excludes topics and details that the bot brings up or seems to have a previous knowledge of.
        - Includes details about the user's career, hobbies, personal interest.
        """
    )


def create_summary(user_claims: UserClaims, chat_start_time: datetime):
    conn = user_meta_model._get_connection()
    cursor = conn.cursor()

    logs = message_model.get_messages(cursor, user_claims.user.id, chat_start_time)

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
        user_meta_model.create_user_meta(
            cursor=cursor,
            user_id=user_claims.user.id,
            data=summary.text,
            tags="",  # TODO: Populate tags if available
            current_user_id=user_claims.user.id,
        )
        conn.commit()
        conn.close()
        # Update Index
        documents = get_documents(user_claims.user.id, chat_start_time)
        add_to_index(documents)
    else:
        conn.close()
