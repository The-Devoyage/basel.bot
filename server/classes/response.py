from typing import Optional, Union
from pydantic import BaseModel


class Response(BaseModel):
    success: bool
    data: Optional[Union[dict, list]]
    status: int
    message: Optional[str]
