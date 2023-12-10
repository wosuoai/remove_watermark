from typing import List, Any, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schema import DouyinVideoDto,DouyinUrlDto
from .douyin_parse_from_webApi import webApi1_return_message
from .douyin_url_parse import analyze_douyin
from models.BaseResult import Response

router = APIRouter()


"""
接口：DouyinVideo 表增删改查
 
POST   /api/douyin_videos            ->  create_douyin_video  ->  创建 douyin_video
GET    /api/douyin_videos            ->  get_douyin_videos    ->  获取所有 douyin_video
GET    /api/douyin_videos/{douyin_video_id}   ->  get_douyin_video     ->  获取单个 douyin_video
PUT    /api/douyin_videos/{douyin_video_id}   ->  update_douyin_video  ->  更新单个 douyin_video
DELETE /api/douyin_videos/{douyin_video_id}   ->  delete_douyin_video  ->  删除单个 douyin_video
"""

@router.post("/real_parse", name="抖音视频或图文链接解析")
async def create_douyin_video(douyin_video_dto: DouyinVideoDto):
    douyin_video_dto = analyze_douyin(douyin_video_dto.url)
    return Response(code=200,data=douyin_video_dto,method_code=0)


@router.post("/real_freeApi1_parse", name="抖音免费链接解析1")
async def create_douyin_realUrl(douyin_url_dto: DouyinUrlDto):
    douyin_url_dto = webApi1_return_message(douyin_url_dto.url)
    return Response(code=200,data=douyin_url_dto,method_code=1)