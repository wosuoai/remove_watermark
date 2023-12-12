from typing import Union

from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from models.BaseResult import Response

async def http422_error_handler( _: Request, exc: Union[RequestValidationError, ValidationError],) -> JSONResponse:
    return JSONResponse(
        content=Response(code=HTTP_422_UNPROCESSABLE_ENTITY, data={}, message=str(exc.errors())),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )

# validation_error_response_definition["properties"] = {
#     "errors": {
#         "title": "Errors",
#         "type": "array",
#         "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
#     },
# }
