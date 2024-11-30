from datetime import datetime, timedelta, timezone
import logging
from typing import List, Optional
from llama_index.agent.openai import OpenAIAgent
from llama_index.agent.openai.openai_assistant_agent import MessageRole
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.tools import BaseTool
from basel.candidate_profile_tool import create_candidate_profile_tool
from basel.create_interview_tool import create_create_interview_tool
from basel.get_interviews_tool import (
    create_get_interviews_tool,
)
from classes.user import User
from database.message import MessageModel

from utils.subscription import SubscriptionStatus

logger = logging.getLogger(__name__)

message_model = MessageModel("basel.db")


def get_agent(
    is_candidate,
    chatting_with_id: int,
    current_user: Optional[User],
    subscription_status: SubscriptionStatus,
) -> OpenAIAgent:
    logger.debug(f"GETTING AGENT FOR USER {chatting_with_id}")
    candidate_profile_tool = create_candidate_profile_tool(chatting_with_id)

    prompt = f"""
       You are a bot representing the candidate.

       You are currently conversting with the candidate that you represent.

       Your name is Basel, you are respectful, professional, helpful, and friendly.
       You help match candidates with employers by learning about the candidates skills, career goals, personal life and hobbies.
       Your personality is a warm extrovert. Slightly gen alpha.

       Your job is to ask questions about the candidate to learn about their skills, career goals, 
       and personal life/hobbies. As you progress through the conversation, try to ask more technical questions
       to get an idea of the users skill level.

       Call the candidate_profile tool to get historical information about the candidate.\n
    """

    subscription_message = ""

    # Membership Expired
    if not subscription_status.active and not subscription_status.is_free_trial:
        subscription_message += """
            Note: This candidate is currently not subscribed to the platform and their free trial
            has expired. Remind them every so often  that while they can interact with you as 
            normal, nothing will be saved and their profile will not receive updates based on 
            the current conversation.
        """
    # Membership Free Trial
    elif not subscription_status.active and subscription_status.is_free_trial:
        subscription_message += f"""
            Note: This user is currently subscribed on a free trial that expires soon. Remind them
            every so often that they are on the free plan and to subscribe for $3.99 a month in order
            to keep ability to update the bot. The free trial last for 30 days. You started your trial on
            {current_user.created_at if current_user else "Unknown"}
            """
    elif subscription_status.active and not subscription_status.is_free_trial:
        subscription_message += """
            Note: The user is currently subscribed to a paid subscription plan.
        """

    prompt += subscription_message

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

    # Get Tools
    tools: List[BaseTool] = [candidate_profile_tool]

    chat_history: List[ChatMessage] = []
    if current_user:
        # Get Authenticated Tools
        get_interviews_tool = create_get_interviews_tool()
        tools.append(get_interviews_tool)

        create_interview_tool = create_create_interview_tool(current_user.id)
        tools.append(create_interview_tool)

        # Populate Recent Chat History
        conn = message_model._get_connection()
        cursor = conn.cursor()
        messages = message_model.get_messages(cursor, current_user.id, limit=40)
        for message in messages:
            logger.debug(f"MESSAGE: {message}")
            history = ChatMessage(
                role=MessageRole.ASSISTANT
                if message.sender == "bot"
                else MessageRole.USER,
                content=message.text,
            )
            chat_history.append(history)

        # Populate User Details
        prompt += f"""
            Current User Email: {current_user.email}
            Current User ID (Private, never share): {current_user.id}
        """

    agent = OpenAIAgent.from_tools(
        tools=tools, verbose=True, system_prompt=prompt, chat_history=chat_history
    )
    return agent
