from typing import Optional, Union
from classes.response import Response


def create_response(
    success: bool,
    data: Optional[Union[dict, list]] = None,
    status: Optional[int] = None,
    message: Optional[str] = None,
    total: Optional[int] = None,
):
    response_status = status if status else 200 if success else 500
    response = Response(
        success=success, data=data, status=response_status, message=message, total=total
    )
    return response
