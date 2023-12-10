from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import RedbookDto
from core.logger import logger
from .redbook_url_parse import analyze_redbook
from models.BaseResult import Response
router = APIRouter()

@router.post("/real_parse", name="小红书图片或视频链接解析")
async def create_redbook_image(redbook_dto: RedbookDto):
    redbook_url_dto = analyze_redbook(redbook_dto.url)
    return Response(code=200,data=redbook_url_dto,method_code=0)