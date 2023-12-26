import re
from fake_useragent import UserAgent
import requests
import lxml.etree
from models.BussinessException import BussinessException
from core.logger import logger
import json
from core.set_proxy import useable_ip
from typing import Any

cookies = {
    'web_session': '040069b54d2fd867c1ce4e0269374b50013583',
}

headers = {
        'user-agent': UserAgent().random
    }

def redbook_real_weburl(share_url: str) -> str:
    """
        处理及判断用户传入的url
    """
    if "www.xiaohongshu.com" in share_url:
        logger.debug(f"正则提取小红书分享后的链接：{share_url}")
        return share_url
    else:
        url_match = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',share_url)
        if url_match == []:
            logger.error("小红书分享链接提取失败")
            raise BussinessException("小红书分享链接提取失败")
        logger.debug(f"正则提取小红书分享后的链接：{url_match}")

        return url_match[0]

def get_real_html(target_url: str, proxied: Any) -> str:
    """
        调接口先拿到html，方便后续判断是图文链接还是视频链接
    """
    logger.debug(f"小红书请求url:{target_url} 小红书请求头：{headers}")
    img_html = requests.get(target_url,headers=headers, cookies=cookies, proxies=proxied).text  # 调取静态接口
    logger.debug("小红书静态接口请求成功")
    title = lxml.etree.HTML(img_html).xpath("//title/text()")[0]  # 标题
    # if "你访问的页面不见了" in title:
    #     logger.error("小红书自定义算法调取小红书接口失败——因IP被风控")
    #     raise BussinessException("小红书自定义算法调取小红书接口失败——因IP被风控")
    return img_html

def redbook_real_imgurl(html: str) -> dict:
    """
        提取抖音图文的有效信息
    """
    title = lxml.etree.HTML(html).xpath("//title/text()")[0] #标题
    logger.debug(f"小红书图文标题：{title}")
    html = html.replace("\\u002F", "/").replace("\n", "").replace(" ", "").replace("[话题]#", "")
    desc = re.search(r'"desc":"(.*?)"', html).group(1) #文案
    logger.debug(f"小红书图文文案：{desc}")
    tags = re.findall(r"#(\w+)", desc) #标签
    logger.debug(f"小红书图文标签：{tags}")
    url_pattern = re.compile(r'"url":"(.*?)"')
    imgurl_list = url_pattern.findall(html)
    real_imgs = [url for url in imgurl_list if 'wm_1' in url]#无水印图片链接
    logger.debug(f"小红书图文无水印图片链接：{real_imgs}")
    plant_imgs = [url for url in imgurl_list if 'prv_1' in url] #有水印图片链接
    logger.debug(f"小红书图文有水印图片链接：{plant_imgs}")
    if plant_imgs == []:
        logger.debug("小红书图文信息提取失败")
        raise BussinessException("小红书图文信息提取失败")
    detail_dict = {} #定义一个字典 以字典的格式返回数据
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "first_img": real_imgs[0], "plant_imgs": plant_imgs, "real_imgs": real_imgs, "link_type": 0, "method_code": 0})
    logger.debug(f"小红书图文返回信息：{detail_dict}")
    return detail_dict


def format_url(url: str) -> str:
    """
        把html转换成二进制
    """
    return bytes(url, "utf-8").decode("unicode_escape")


def get_video_link(html: str) -> dict:
    """
        提取抖音视频所有的有效信息
    """
    title = lxml.etree.HTML(html).xpath("//title/text()")[0]  # 标题
    logger.debug(f"小红书视频标题：{title}")
    html = html.replace("\\u002F", "/").replace("\n", "").replace(" ", "").replace("[话题]#", "")
    desc = re.search(r'"desc":"(.*?)"', html).group(1)  # 文案
    logger.debug(f"小红书视频文案：{desc}")
    tags = re.findall(r"#(\w+)", desc)  # 标签
    logger.debug(f"小红书视频标签：{tags}")
    try:
        first_img = re.search(r'"urlDefault":"(.*?)"', html).group(1)  # 视频封面图
    except Exception as error:
        first_img = ""
    logger.debug(f"小红书视频封面图：{first_img}")
    pattern = r'"originVideoKey":"([^"]*)"'
    match = re.search(pattern, html)
    video_url = format_url(f"https://sns-video-hw.xhscdn.com/{match.group(1)}") #无水印视频链接
    logger.debug(f"小红书视频链接：{video_url}")
    if match.group(1) == "":
        logger.error(f"小红书视频链接提取失败")
        raise BussinessException("小红书视频链接提取失败")
    # 音频文件，无音频的视频文件，接口里面没有，返回空
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "music": "", "video_without_mp3": "", "first_img": first_img,"real_video_url": video_url, "link_type": 1, "method_code": 0})
    logger.debug(f"小红书视频信息：{detail_dict}")
    return detail_dict

def parse_real_videoUrl(url: str, proxied: Any) -> dict:
    html = get_real_html(url,proxied)
    return get_video_link(html)

def analyze_redbook(redbook_share_url: str, proxies_status: int):
    logger.info(f"小红书传入的url是：{redbook_share_url}，代理IP状态：{proxies_status}")
    if proxies_status == 1:
        proxied = useable_ip()
    else:
        proxied = None
    logger.info(f"此次解析拿到的代理IP是：{proxied}")
    html = get_real_html(redbook_real_weburl(redbook_share_url),proxied)
    if "originVideoKey" in html:
        real_video_detail = parse_real_videoUrl(redbook_real_weburl(redbook_share_url),proxied)
        return real_video_detail
    else:
        real_img_detail = redbook_real_imgurl(html)
        return real_img_detail