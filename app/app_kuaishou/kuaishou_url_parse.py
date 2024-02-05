import requests
from fake_useragent import UserAgent
import lxml.etree
import re
from models.BussinessException import BussinessException
from core.logger import logger
from typing import Any
from core.set_proxy import useable_ip

cookies = {
    'did': '',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': UserAgent().random,
}

def get_real_html(share_url: str, proxied: Any) -> str:
    """
    调取快手静态接口
    :param share_url:
    :return:
    """
    kuaishou_html = requests.get(share_url, cookies=cookies, headers=headers, proxies=proxied).text.replace("\n","").replace(" ","").replace("\\u002F","/")
    logger.debug(f"快手静态接口返回数据成功")
    return kuaishou_html

def get_video_link(html_body: str) -> dict:
    """
    正则需要的有效信息
    :param html_body:
    :return:
    """
    title = lxml.etree.HTML(html_body).xpath("//title/text()")[0]  # 标题
    logger.debug(f"快手视频标题：{title}")
    tags = re.findall(r"#(\w+)", title.replace(" ",""))  # 标签
    logger.debug(f"快手视频标签：{tags}")
    first_img = re.search(r'"coverUrl":\s*"([^"]*)"', html_body).group(1) # 视频封面图
    logger.debug(f"快手视频封面图链接：{first_img}")
    video_link = re.search(r'"photoUrl":\s*"([^"]*)"', html_body).group(1) # 视频无水印链接
    logger.debug(f"快手视频无水印链接：{video_link}")
    if video_link == "":
        logger.debug("快手视频信息提取失败")
        raise BussinessException("快手视频信息提取失败")
    detail_dict = {}
    detail_dict.update({"title": title, "desc": "", "tags": tags, "music": "", "video_without_mp3": "", "first_img": first_img, "real_video_url": video_link, "link_type": 1, "method_code": 0})
    logger.debug(f"快手视频返回信息：{detail_dict}")
    return detail_dict

def get_imgs_link(html_body: str) -> dict:
    """
    正则需要的有效信息
    :param html_body:
    :return:
    """
    title = lxml.etree.HTML(html_body).xpath("//title/text()")[0]  # 标题
    logger.debug(f"快手图文标题：{title}")
    tags = re.findall(r"#(\w+)", title.replace(" ",""))  # 标签
    logger.debug(f"快手图文标签：{tags}")
    first_img = re.search(r'"coverUrl":\s*"([^"]*)"', html_body).group(1) # 视频封面图
    logger.debug(f"快手图文封面图链接：{first_img}")
    video_link = re.search(r'"photoUrl":\s*"([^"]*)"', html_body).group(1) # 视频无水印链接
    logger.debug(f"快手图文视频链接：{video_link}")
    if video_link == "":
        logger.debug("快手图文信息提取失败")
        raise BussinessException("快手图文信息提取失败")
    detail_dict = {}
    detail_dict.update({"title": title, "desc": "", "tags": tags, "music": "", "video_without_mp3": "", "first_img": first_img, "real_video_url": video_link, "link_type": 0, "method_code": 0})
    logger.debug(f"快手图文返回信息：{detail_dict}")
    return detail_dict

def get_photoId(html_body: str) -> str:
    """
    photoId是评论接口的一个必要参数
    :param html_body:
    :return:
    """
    VisionVideoDetailPhoto = re.search(r'VisionVideoDetailPhoto:([^:]*):', html_body).group(1)
    logger.debug(f"提取出快手的photoId是：{VisionVideoDetailPhoto}")
    return VisionVideoDetailPhoto

def analyze_kuaishou(share_url: str, proxies_status: int):
    logger.info(f"快手传入的url是：{share_url}，代理IP状态：{proxies_status}")
    if proxies_status == 1:
        proxied = useable_ip()
    else:
        proxied = None
    logger.info(f"此次解析拿到的代理IP是：{proxied}")
    kuaishou_html = get_real_html(share_url,proxied)
    if "图文" in kuaishou_html:
        logger.debug("该分享链接是：快手图文链接")
        return get_imgs_link(kuaishou_html)
    else:
        logger.debug("该分享链接是：快手视频链接")
        return get_video_link(kuaishou_html)