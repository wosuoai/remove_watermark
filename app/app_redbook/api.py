from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import RedbookDto
from core.logger import logger
from .redbook_url_parse import analyze_redbook
from models.BaseResult import Response,KownedException
router = APIRouter()

#@router.post("/real_parse", name="小红书图片或视频链接解析")
def create_redbook_image(redbook_dto: RedbookDto):
    try:
        logger.info("使用小红书自定义算法解析")
        redbook_url_dto = analyze_redbook(redbook_dto.url)
        return Response(code=200,data=redbook_url_dto)
    except Exception as error:
        logger.error(f"redbook_url_parse::create_redbook_image: 小红书自定义算法解析异常：{str(error)}")
        return False

@router.post("/real_parse", name="小红书图片或视频链接解析")
async def main(redbook_dto: RedbookDto):
    redbook_detail = create_redbook_image(redbook_dto)
    if redbook_detail is not False:
        return redbook_detail
    return KownedException(code=400, data={}, message="所有接口返回数据失败")