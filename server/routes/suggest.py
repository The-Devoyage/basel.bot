import logging
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from llama_index.core.agent.workflow import AgentOutput, ToolCall, ToolCallResult
from basel.agent_workflow import get_agent_workflow
from classes.user_claims import UserClaims
from utils.jwt import require_auth
from database.message import Message
from utils.responses import create_response
from utils.subscription import verify_subscription

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/suggest")
async def get_standups(
    user_claims: UserClaims = Depends(require_auth),
):
    try:
        message = (
            await Message.find(
                Message.user.id == user_claims.user.id,  # type:ignore
                Message.sender == "bot",
            )
            .sort("-created_at")
            .first_or_none()
        )

        logger.debug(f"RECENT MESSAGE: {message}")

        if not message:
            raise Exception("Failed to find most recent message.")

        subscription_status = await verify_subscription(user_claims.user)

        (handler, _) = await get_agent_workflow(
            is_candidate=True,
            chatting_with=user_claims.user,
            user_claims=user_claims,
            subscription_status=subscription_status,
            shareable_link=None,
        )

        await handler.run(
            user_msg=f"""
            - Use the candidate profile to answer the following question or prompt as if you were the candidate.
            - Respond in first person. 
            - Represent the user accuratly and do not pretend to know things they
            might not know. 
            - If the candidate profile does not contain an answer, politely respod a variation of "i dont know".

            Question/last message:
           {message}
           """
        )

        current_agent = None
        response = ""
        async for event in handler.stream_events():
            if (
                hasattr(event, "current_agent_name")
                and event.current_agent_name != current_agent
            ):
                current_agent = event.current_agent_name
                print(f"\n{'='*50}")
                print(f"🤖 Agent: {current_agent}")
                print(f"{'='*50}\n")

            elif isinstance(event, AgentOutput):
                if event.response.content:
                    print("📤 Output:", event.response.content)
                    response = event.response.content
                if event.tool_calls:
                    print(
                        "🛠️  Planning to use tools:",
                        [call.tool_name for call in event.tool_calls],
                    )
            elif isinstance(event, ToolCallResult):
                print(f"🔧 Tool Result ({event.tool_name}):")
                print(f"  Arguments: {event.tool_kwargs}")
                print(f"  Output: {event.tool_output}")
            elif isinstance(event, ToolCall):
                print(f"🔨 Calling Tool: {event.tool_name}")
                print(f"  With arguments: {event.tool_kwargs}")

        return create_response(success=True, data={"text": response})

    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500, detail="Something went wrong...")
