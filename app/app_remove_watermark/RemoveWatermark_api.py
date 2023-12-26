from typing import List, Any, Union
from fastapi import APIRouter
from .schema import RemoveWatermarkDto
from core.logger import logger
from .remove_watermark import deal_video_watermark,deal_video_subtitle
from models.BaseResult import Response,KownedException
router = APIRouter()

@router.post("/deal_video_watermark/", name="去除视频水印")
async def remove_video_watermark(RemoveWatermark_dto: RemoveWatermarkDto):
    try:
        logger.info("使用去视频水印方法处理水印")
        watermark_remove = await deal_video_watermark(RemoveWatermark_dto.roi_list,RemoveWatermark_dto.threshold,RemoveWatermark_dto.kernel_size,RemoveWatermark_dto.video_path,RemoveWatermark_dto.save_path)
        return Response(code=200, data=watermark_remove)
    except Exception as error:
        logger.error(f"remove_watermark::remove_video_watermark: 视频水印处理解析异常：{str(error)}")
        return KownedException(code=400, data={}, message="视频水印处理失败")

@router.post("/deal_video_subtitle/", name="去除视频字幕")
async def remove_video_subtitle(RemoveWatermark_dto: RemoveWatermarkDto):
    try:
        logger.info("使用去视频字幕方法处理字幕")
        subtitle_remove = await deal_video_subtitle(RemoveWatermark_dto.roi_list, RemoveWatermark_dto.threshold, RemoveWatermark_dto.kernel_size, RemoveWatermark_dto.video_path, RemoveWatermark_dto.save_path)
        return Response(code=200, data=subtitle_remove)
    except Exception as error:
        logger.error(f"remove_watermark::remove_video_subtitle: 视频字幕处理解析异常：{str(error)}")
        return KownedException(code=400, data={}, message="视频字幕处理失败")