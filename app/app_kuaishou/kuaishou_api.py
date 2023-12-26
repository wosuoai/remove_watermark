from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from .schema import KuaishouDto
from core.logger import logger
from .kuaishou_url_parse import analyze_kuaishou
from models.BaseResult import Response,KownedException
router = APIRouter()

def create_kuaishou_image(kuaishou_dto: KuaishouDto):
    try:
        logger.info("使用快手自定义算法解析")
        kuaishou_url_dto = analyze_kuaishou(kuaishou_dto.url,kuaishou_dto.proxies_status)
        return Response(code=200,data=kuaishou_url_dto)
    except Exception as error:
        logger.error(f"kuaishou_url_parse::create_kuaishou_image: 快手自定义算法解析异常：{str(error)}")
        return False

@router.post("/real_parse", name="快手图片或视频链接解析")
async def main(kuaishou_dto: KuaishouDto):
    kuaishou_detail = create_kuaishou_image(kuaishou_dto)
    if kuaishou_detail is not False:
        return kuaishou_detail
    return KownedException(code=400, data={}, message="所有接口返回数据失败")