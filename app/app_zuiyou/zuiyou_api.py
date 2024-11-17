from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import ZuiyouDto
from core.logger import logger
from .zuiyou_url_parse import analyze_zuiyou
from models.BaseResult import Response,KownedException
router = APIRouter()

def create_zuiyou_image(zuiyou_dto: ZuiyouDto):
    try:
        logger.info("使用最右自定义算法解析")
        zuiyou_url_dto = analyze_zuiyou(zuiyou_dto.url,zuiyou_dto.proxies_status)
        return Response(code=200,data=zuiyou_url_dto)
    except Exception as error:
        logger.error(f"zuiyou_url_parse::create_zuiyou_image: 最右自定义算法解析异常：{str(error)}")
        return False

@router.post("/real_parse", name="最右图片或视频链接解析")
async def main(zuiyou_dto: ZuiyouDto):
    zuiyou_detail = create_zuiyou_image(zuiyou_dto)
    if zuiyou_detail is not False:
        return zuiyou_detail
    return KownedException(code=400, data={}, message="所有接口返回数据失败")