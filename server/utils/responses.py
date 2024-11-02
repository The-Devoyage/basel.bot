from typing import Optional, Union
from classes.response import Response


def create_response(success: bool, data: Optional[Union[dict, list]]):
    response = Response(success=success, data=data)
    return response
