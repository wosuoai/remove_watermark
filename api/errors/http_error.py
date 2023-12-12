from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from models.BaseResult import Response

# http 异常处理句柄. 包含返回内容、状态码、响应头
async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content=Response(code=exc.status_code, data={}, message=exc.detail),
        status_code=exc.status_code,
        headers=exc.headers if hasattr(exc, "headers") else None
    )
