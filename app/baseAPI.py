from fastapi import APIRouter, Depends, HTTPException
from core.logger import logger
from models.BaseResult import Response

router = APIRouter()


@router.post("/health", name="健康检查")
@router.get("/health", name="健康检查")
async def health():
    return Response()
