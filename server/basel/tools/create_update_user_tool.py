from typing import Optional
from llama_index.core.bridge.pydantic import BaseModel, Field
from llama_index.core.tools.function_tool import FunctionTool

from database.user import User


class UpdateUserArgs(BaseModel):
    first_name: Optional[str] = Field(
        default=None, description="The first name of the user."
    )
    last_name: Optional[str] = Field(
        default=None, description="The last name of the user."
    )


async def update_user(
    user: User, first_name: Optional[str] = None, last_name: Optional[str] = None
):
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    await user.save()
    return await user.to_public_dict()


def create_update_user_tool(user: User):
    create_update_user_tool = FunctionTool.from_defaults(
        async_fn=lambda first_name=None, last_name=None: update_user(
            user, first_name, last_name
        ),
        name="update_user_tool",
        description="""
        Useful to update user profile information such as first name and last name.
        """,
        fn_schema=UpdateUserArgs,
    )

    return create_update_user_tool
