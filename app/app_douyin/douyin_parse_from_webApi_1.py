import http.client
import re
from models.BussinessException import BussinessException
from core.logger import logger

def regix_share_url(douyin_share_url: str) -> str:
    share_url = re.search(r'https?://\S+', douyin_share_url)
    if share_url == None:
        logger.error("抖音api接口2分享链接提取失败")
        raise BussinessException("抖音api接口2分享链接提取失败")
    return share_url.group()

def douyin_webApi_1(douyin_web_url: str) -> dict:
    conn = http.client.HTTPSConnection("api.tsyinpin.com")

    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"link\"\r\n\r\n\r\n-----011000010111000001101001--\r\n\r\n"

    headers = {'content-type': "multipart/form-data; boundary=---011000010111000001101001"}

    conn.request("POST", "/douyin_video.php?url={}".format(douyin_web_url), payload, headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8").replace("\/", "/").replace("null", "''")
    logger.debug(f"抖音api接口2返回的信息是：{data}")
    if data==None:
        logger.error("抖音api接口2信息返回失败")
        raise BussinessException("抖音api接口2信息返回失败")

    title = eval(data)["music"]["title"]  # 标题
    logger.debug(f"抖音api接口2视频标题：{title}")
    desc = eval(data)["video"]["desc"]  # 文案
    logger.debug(f"抖音api接口2视频文案：{desc}")
    mp3 = eval(data)["music"]["music"]  # 音频
    logger.debug(f"抖音api接口2视频音频：{mp3}")
    video_url = eval(data)["video"]["realUrl"]  # 无水印视频链接
    logger.debug(f"抖音api接口2视频无水印链接：{video_url}")
    if video_url == "":
        logger.error("抖音api接口2提取信息失败")
        raise BussinessException("抖音api接口2提取信息失败")
    # 无音频的视频文件，接口里面没有，返回空
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": [], "music": mp3, "video_without_mp3": "", "real_video_url": video_url, "link_type": 1, "method_code": 1})
    logger.debug(f"抖音api接口2的视频返回数据：{detail_dict}")
    return detail_dict

def webApi1_return_message(douyin_share_url: str):
    logger.info(f"抖音传入的url是：{douyin_share_url}")
    web_url = regix_share_url(douyin_share_url)
    return douyin_webApi_1(web_url)