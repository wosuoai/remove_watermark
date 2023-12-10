import http
from starlette.requests import Request
from starlette.responses import JSONResponse
from models.BaseResult import Response


async def general_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content=Response(code=http.HTTPStatus.INTERNAL_SERVER_ERROR, data={},message=str(e),method_code=0),
    )
