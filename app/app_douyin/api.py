from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from core.logger import logger
from .schema import DouyinUrlDto
from .douyin_url_parse import analyze_douyin
from .douyin_parse_from_webApi_1 import webApi1_return_message
from models.BaseResult import Response,KownedException

router = APIRouter()


"""
接口：DouyinVideo 表增删改查
 
POST   /api/douyin_videos            ->  create_douyin_video  ->  创建 douyin_video
GET    /api/douyin_videos            ->  get_douyin_videos    ->  获取所有 douyin_video
GET    /api/douyin_videos/{douyin_video_id}   ->  get_douyin_video     ->  获取单个 douyin_video
PUT    /api/douyin_videos/{douyin_video_id}   ->  update_douyin_video  ->  更新单个 douyin_video
DELETE /api/douyin_videos/{douyin_video_id}   ->  delete_douyin_video  ->  删除单个 douyin_video
"""

def create_douyin_realUrl(douyin_url_dto: DouyinUrlDto):
    try:
        logger.info("使用抖音自定义算法解析")
        douyin_url_dto = analyze_douyin(douyin_url_dto.url)
        return Response(code=200,data=douyin_url_dto)
    except Exception as error:
        logger.error(f"douyin_url_parse::create_douyin_realUrl: 抖音自定义算法解析异常：{str(error)}")
        return False

def create_douyin_realUrl_api1(douyin_url_dto: DouyinUrlDto):
    try:
        logger.info("使用抖音api接口1解析")
        douyin_url_dto = webApi1_return_message(douyin_url_dto.url)
        return Response(code=200,data=douyin_url_dto)
    except Exception as error:
        logger.error(f"douyin_url_parse::create_douyin_realUrl_api1: 抖音api接口1解析异常：{str(error)}")
        return False

@router.post("/real_parse", name="抖音视频或图文链接解析")
async def main(douyin_url_dto: DouyinUrlDto):
    douyin_detail = create_douyin_realUrl(douyin_url_dto)
    if douyin_detail is not False:
        return douyin_detail
    douyin_detail_api1 = create_douyin_realUrl_api1(douyin_url_dto)
    if douyin_detail_api1 is not False:
        return douyin_detail_api1
    return KownedException(code=400, data={}, message="所有接口返回数据失败")