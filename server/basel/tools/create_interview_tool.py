from functools import partial
import logging
from typing import List, Optional
from uuid import UUID
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool
from llama_index.core.workflow import Context, HumanResponseEvent, InputRequiredEvent
from database.interview import Interview, InterviewType
from database.organization import Organization
from database.subscription import SubscriptionFeature
from database.user import User
from utils.subscription import SubscriptionStatus, check_subscription_permission


logger = logging.getLogger(__name__)


class CreateInterviewParams(BaseModel):
    description: str = Field(description="The description of the interview.")
    position: str = Field(
        description="The position associated with the application or interview.",
        default=None,
    )
    url: Optional[str] = Field(
        description="The URL of the job posting associated with the interview you are creating.",
        default=None,
    )
    organization_uuid: Optional[str] = Field(
        description="The organization UUID, if provided, of which the interview belongs.",
        default=None,
    )
    tags: List[str] = Field(
        description="Tags, categories, and descriptors of the organziation, position, and interview.",
        default=[],
    )


async def validate_access(
    subscription_status: SubscriptionStatus,
    organization_uuid: Optional[str] = None,
):
    try:
        allow_create = check_subscription_permission(
            subscription_status, SubscriptionFeature.CREATE_INTERVIEW
        )
        if not allow_create:
            logger.warn("User does not have permission to create interview.")
            raise Exception(
                "User does not have permission to create an interview and needs to upgrade membership."
            )

        if organization_uuid:
            allow_organization = check_subscription_permission(
                subscription_status, SubscriptionFeature.MANAGE_ORGANIZATION
            )
            if not allow_organization:
                raise Exception(
                    "User does not have permission to create an organization interview and needs to upgrade membership."
                )
            organization = await Organization.find_one(
                Organization.uuid == UUID(organization_uuid),
                Organization.users.user._id == current_user.id,  # type:ignore
                fetch_links=True,
            )
            if not organization:
                raise Exception("Failed to find organization.")
    except Exception as e:
        logger.error(f"Validation Failed: {str(e)}")
        raise e


async def create_interview(
    ctx: Context,
    current_user: User,
    description: str,
    position: str,
    subscription_status: SubscriptionStatus,
    url: Optional[str] = None,
    organization_uuid: Optional[str] = None,
    tags: List[str] = [],
):
    try:
        organization = None
        interview_type = InterviewType.GENERAL

        await validate_access(
            subscription_status=subscription_status, organization_uuid=organization_uuid
        )

        if organization_uuid:
            interview_type = InterviewType.APPLICATION

        pending_confirm_create_interview = await ctx.get(
            "pending_confirm_create_interview", False
        )

        if not pending_confirm_create_interview:
            logger.debug("PENDING CONFIRM CREATE INTERVIEW")
            await ctx.set("pending_confirm_create_interview", True)
            ctx.write_event_to_stream(
                InputRequiredEvent(
                    prefix=f"""
Confirm that you want to create the following interview:
- **Position**: {position}
- **Description**: {description}

Respond with **yes** to create the interview.
                    """,
                )
            )
            return None

        event = await ctx.wait_for_event(HumanResponseEvent)
        await ctx.set("pending_confirm_create_interview", False)

        if event.response.lower() == "yes":
            logger.debug("CONFIRMED CREATE INTERVIEW")
            interview = await Interview(
                description=description,
                created_by=current_user,  # type:ignore
                organization=organization,  # type:ignore
                url=url,
                interview_type=interview_type,
                position=position,
                tags=tags,
            ).create()
            if not interview:
                raise Exception("Failed to create interview.")
            return f"""
                The interview has been created. Use the `create_interview_questions_tool` to proceed with creating interview questions.
                Interview UUID: {interview.uuid}
            """
        else:
            logger.debug("REJECT CREATE INTERVIEW")
            return """
                The user has decided not to create the interview for now. Ask them if they want to modify any of the details.
            """
    except Exception as e:
        logger.error(e)
        raise e


def init_create_interview_tool(
    current_user: User, subscription_status: SubscriptionStatus
):
    create_interview_tool = FunctionTool.from_defaults(
        async_fn=partial(
            create_interview,
            current_user=current_user,
            subscription_status=subscription_status,
        ),
        name="create_interview_tool",
        description=(
            "Useful to insert an interview into the database by the request of a user."
            "Once created interview questions may be created and associated with the interview."
            "Always confirm before creating."
        ),
        fn_schema=CreateInterviewParams,
    )

    return create_interview_tool
