from fake_useragent import UserAgent
import requests
from models.BussinessException import BussinessException
from core.logger import logger
from core.set_proxy import useable_ip
from typing import Any
from bs4 import BeautifulSoup

headers = {
        'user-agent': UserAgent().random
    }

def zuiyou_real_weburl(share_url: str) -> str:
    """
        处理及判断用户传入的url
    """
    real_url = share_url.split('>>')[-1]
    logger.debug(f"正则提取最右分享后的链接：{real_url}")

    return real_url

def get_real_html(target_url: str, proxied: Any) -> str:
    """
        调接口先拿到html，方便后续判断是图文链接还是视频链接
    """
    logger.debug(f"最右请求url:{target_url} 最右请求头：{headers}")
    img_html = requests.get(target_url,headers=headers, proxies=proxied).text  # 调取静态接口
    logger.debug("最右静态接口请求成功")

    return img_html

def zuiyou_real_imgurl(html: str) -> dict:
    """
        提取抖音图文的有效信息
    """
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("title").text
    logger.debug(f"最右图文标题：{title}")
    imgurl_list = []
    for img in soup.find("div", class_="ResponsiveList__inner").find_all("img"):
        imgurl_list.append(img.get("src"))
    logger.debug(f"最右图文无水印图片链接：{imgurl_list}")
    detail_dict = {} #定义一个字典 以字典的格式返回数据
    detail_dict.update({"title": title, "desc": "", "tags": "", "first_img": imgurl_list[0], "plant_imgs": imgurl_list, "real_imgs": "", "link_type": 0, "method_code": 0})
    logger.debug(f"最右图文返回信息：{detail_dict}")
    return detail_dict


def get_video_link(html: str) -> dict:
    """
        提取抖音视频所有的有效信息
    """
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("title").text
    logger.debug(f"最右视频标题：{title}")
    try:
        first_img = soup.find("div",class_="ImageBoxII__imgWrap").find("img").get("src")
    except Exception as error:
        first_img = ""
    logger.debug(f"最右视频封面图：{first_img}")
    video_url = soup.find("video",preload="metadata").get("src") #无水印视频链接
    logger.debug(f"最右视频链接：{video_url}")
    # 音频文件，无音频的视频文件，接口里面没有，返回空
    detail_dict = {}
    detail_dict.update({"title": title, "desc": "", "tags": "", "music": "", "video_without_mp3": "", "first_img": first_img,"real_video_url": video_url, "link_type": 1, "method_code": 0})
    logger.debug(f"最右视频信息：{detail_dict}")
    return detail_dict

def analyze_zuiyou(zuiyou_share_url: str, proxies_status: int):
    logger.info(f"最右传入的url是：{zuiyou_share_url}，代理IP状态：{proxies_status}")
    if proxies_status == 1:
        proxied = useable_ip()
    else:
        proxied = None
    logger.info(f"此次解析拿到的代理IP是：{proxied}")
    html = get_real_html(zuiyou_real_weburl(zuiyou_share_url),proxied)
    if "SharePostCard__video" in html:
        real_video_detail = get_video_link(html)
        return real_video_detail
    else:
        real_img_detail = zuiyou_real_imgurl(html)
        return real_img_detail