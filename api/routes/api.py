from fastapi import APIRouter

import app.app_douyin.douyin_api as douyin # 注册抖音图文或视频解析路由
import app.app_redbook.redbook_api as redbook # 注册小红书图文或视频解析路由
import app.app_kuaishou.kuaishou_api as kuaishou # 注册快手图文或视频解析路由
import app.app_bilibili.bilibili_api as bilibili # 注册B站图文或视频解析路由
import app.app_zuiyou.zuiyou_api as zuiyou # 注册最右图文或视频解析路由
import app.app_remove_watermark.RemoveWatermark_api as remove_watermark # 注册视频去水印路由
import app.baseAPI as baseAPI
router = APIRouter()

router.include_router(baseAPI.router, tags=["健康检查"]) # 注册抖音视频链接
router.include_router(douyin.router, tags=["抖音图文或视频链接提取"], prefix="/douyin") # 注册抖音图文或视频链接
router.include_router(redbook.router, tags=["小红书图文或视频链接提取"], prefix="/redbook") # 注册小红书图文或视频链接
router.include_router(kuaishou.router, tags=["快手图文或视频链接提取"], prefix="/kuaishou") # 注册快手图文或视频链接
router.include_router(bilibili.router, tags=["B站图文或视频链接提取"], prefix="/bilibili") # 注册B站图文或视频链接
router.include_router(zuiyou.router, tags=["最右图文或视频链接提取"], prefix="/zuiyou") # 注册最右图文或视频链接
router.include_router(remove_watermark.router, tags=["视频去水印"], prefix="/remove_watermark") # 注册视频去水印