import requests
from fake_useragent import UserAgent
import re
from models.BussinessException import BussinessException
from core.logger import logger
from typing import Any
from core.set_proxy import useable_ip

def bilibili_real_weburl(share_url: str) -> str:
    """
    正则提取用户的分享链接
    :param share_url:
    :return:
    """
    if "【" in share_url:
        url_value = re.search(r'https://[^?]+\?', share_url)
        if url_value.group(0)[:-1] == "":
            logger.error("B站分享链接提取失败")
            raise BussinessException("B站分享链接提取失败")
        logger.debug(f"正则提取B站分享后的链接：{url_value.group(0)[:-1]}")
        return url_value.group(0)[:-1]
    else:
        logger.debug(f"正则提取B站分享后的链接：{share_url}")
        return share_url

def get_real_html(real_url: str, proxied: Any) -> str:
    """
    调取B站静态接口
    :param real_url:
    :return:
    """
    headers = {
        'authority': 'www.bilibili.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': UserAgent().random,
    }

    bilibili_html = requests.get(real_url, headers=headers, proxies=proxied).text.replace("\n","").replace(" ","")
    logger.debug(f"B站静态接口返回数据成功")
    return bilibili_html

def get_video_link(html_body: str) -> dict:
    """
    正则提取需要的有效信息
    注意：这里解析拿到的B站视频链接是有水印的！！！
    :param html_body:
    :return:
    """
    author = re.search(r'name="author"content="(.*?)">', html_body).group(1)  # 作者
    logger.debug(f"B站视频的作者：{author}")
    title = re.search(r'name="title"content="(.*?)">', html_body).group(1).replace("_哔哩哔哩_bilibili","")  # 标题
    logger.debug(f"B站视频标题：{title}")
    desc = re.search(r'name="description"content="(.*?)">', html_body).group(1).split(",视频播放量")[0]  # 正文
    logger.debug(f"B站视频的正文：{desc}")
    tags = re.search(r'name="keywords"content="(.*?)">', html_body).group(1).split(",")[1:-4]  # 标签
    logger.debug(f"B站视频标签：{tags}")
    real_video_url = re.search(r'"base_url":"(.*?)"', html_body).group(1)  # B站视频链接
    logger.debug(f"B站视频无水印链接：{real_video_url}")
    if real_video_url == "":
        logger.debug("B站视频信息提取失败")
        raise BussinessException("B站视频信息提取失败")
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "music": "", "video_without_mp3": "", "first_img": "", "real_video_url": real_video_url, "link_type": 1, "method_code": 0})
    logger.debug(f"B站视频返回信息：{detail_dict}")
    return detail_dict

def get_oid(html_body: str) -> str:
    """
    aid是评论接口的一个必要参数
    :param html_body:
    :return:
    """
    oid = re.search(r'"aid":(\d+)', html_body).group(1)
    logger.debug(f"提取出B站的oid是：{oid}")
    return oid

def analyze_bilibili(share_url: str, proxies_status: int):
    logger.info(f"B站传入的url是：{share_url}，代理IP状态：{proxies_status}")
    if proxies_status == 1:
        proxied = useable_ip()
    else:
        proxied = None
    logger.info(f"此次解析拿到的代理IP是：{proxied}")
    return get_video_link(get_real_html(bilibili_real_weburl(share_url),proxied))