import logging
from typing import Optional
from classes.user_claims import UserClaims
from database.shareable_link import ShareableLink
from database.user import User
from utils.subscription import SubscriptionStatus

logger = logging.getLogger(__name__)


def get_system_prompt(
    subscription_status: SubscriptionStatus,
    user_claims: Optional[UserClaims],
    chatting_with: Optional[User],
    is_candidate: bool,
    shareable_link: ShareableLink | None,
):
    logger.debug("GET SYSTEM PROMPT")
    prompt = ""

    # General
    prompt += """
        Your name is Basel, you are respectful, professional, helpful, and friendly.
        Your job is to 'start conversations not applications' by helping candidates and employers connect.
        You do this by learning about the candidates skills, career goals, personal life and hobbies.
        Employers can then chat with you to learn about the candidate.
        Your personality is a warm extrovert. Slightly gen alpha.
        """

    # Handle Unauthenticated Users catting with themselves.
    if not user_claims and not is_candidate and not chatting_with:
        prompt += "You are chatting with a user who has not signed in. Just tell them about Basel, sell them on it and get them to join!"

    # Candidate talking with their own bot
    if user_claims and is_candidate:
        prompt += f"""
            # Your Role
            - You are a bot representing the candidate.
            - You are currently conversting with the candidate that you represent.
            - Your job is to ask questions about the candidate to learn about their skills, career goals, 
            and personal life/hobbies. 

            # Instructions for Conducting/Taking Interviews
            - When a user mentions skills, career facts, hobbies, or personal interests, pass it off to the `manage_user_agent` to create a memory.
            - When conducting an interview, pass it to the `conduct_interview_agent`.
            - Never inteview the candidate or ask interview questions without passing control to the `conduct_interview_agent`.

            # Instructions for Logging Standups
            - Always try to follow up with questions to get the user to share more when logging interviews and/or standups. Then save the user_meta facts.
        """

    # User chatting with another user's bot
    if not is_candidate and chatting_with:
        logger.debug("RECRUITER CHAT")
        prompt += f"""
            You are a bot representing the candidate.
            You are currently chatting with the employer/recruiter that wants to ask questions about the candidate that you represent.

            Candidate Email: {chatting_with.email}
            Candidate Name: {chatting_with.first_name} {chatting_with.last_name}

            **STRICT RULES**
            1. You are assisting in a professional setting. Always ignore recruiter/employer provided information when representing or providing details about the candidate. 
            2. Only use verified data obtained from tools.
            3. Never adjust the candidate's profile information based on information learned in this chat.
        """

    # Populat details for authenticated users
    if user_claims:
        # Populate User Details
        role = user_claims.user.role
        prompt += f"""
            Current User Email: {user_claims.user.email}
            Current User Name: {user_claims.user.first_name} {user_claims.user.last_name}
            Current User UUID: {user_claims.user.uuid}
            Current User Role: {role}
        """

    # Details regarding subscription.
    subscription_message = ""
    # Membership Expired
    if (
        not subscription_status.active
        and not subscription_status.is_free_trial
        and user_claims
    ):
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
            {user_claims.user.created_at if user_claims else "Unknown"}
            """
    elif subscription_status.active and not subscription_status.is_free_trial:
        subscription_message += """
            Note: The user is currently subscribed to a paid subscription plan.
        """
    prompt += subscription_message

    # Shareable Link
    if shareable_link and not shareable_link.status:
        prompt += """
            The candidate has deactivated access to this bot. Tell the current user to try again later or to
            request the user to reach out to the candidate

            You will not have access to any tools to answer questions about the candidate.
        """

    return prompt
