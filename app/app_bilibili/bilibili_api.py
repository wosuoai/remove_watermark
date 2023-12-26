from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from .schema import BilibiliDto
from core.logger import logger
from .bilibili_url_parse import analyze_bilibili
from models.BaseResult import Response,KownedException
router = APIRouter()

def create_bilibili_image(bilibili_dto: BilibiliDto):
    try:
        logger.info("使用B站自定义算法解析")
        bilibili_url_dto = analyze_bilibili(bilibili_dto.url)
        return Response(code=200,data=bilibili_url_dto)
    except Exception as error:
        logger.error(f"bilibili_url_parse::create_bilibili_image: B站自定义算法解析异常：{str(error)}")
        return False

@router.post("/real_parse", name="B站图片或视频链接解析")
async def main(bilibili_dto: BilibiliDto):
    bilibili_detail = create_bilibili_image(bilibili_dto)
    if bilibili_detail is not False:
        return bilibili_detail
    return KownedException(code=400, data={}, message="所有接口返回数据失败")