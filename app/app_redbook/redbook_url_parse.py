import re
import random
import requests
import lxml.etree
from models.BussinessException import BussinessException

headers = {
        "Referer": "https://www.xiaohongshu.com/",
    }

def redbook_real_weburl(share_url: str) -> str:
    """
        处理及判断用户传入的url
    """
    if "www.xiaohongshu.com" in share_url:
        return share_url
    else:
        url_match = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',share_url)
        if url_match == []:
            raise BussinessException("小红书分享链接提取失败")

        return url_match[0]

def get_real_html(target_url: str) -> str:
    """
        调接口先拿到html，方便后续判断是图文链接还是视频链接
    """
    img_html = requests.get(target_url, headers=headers).text  # 调取静态接口
    return img_html

def redbook_real_imgurl(html: str) -> dict:
    """
        提取无水印的img_url
    """
    title = lxml.etree.HTML(html).xpath("//title/text()")[0] #标题
    html = html.replace("\\u002F", "/").replace("\n", "").replace(" ", "").replace("[话题]#", "")
    desc = re.search(r'"desc":"(.*?)"', html).group(1) #文案
    tags = re.findall(r"#(\w+)", desc) #标签
    url_pattern = re.compile(r'"url":"(.*?)"')
    imgurl_list = url_pattern.findall(html)
    real_imgs = list(set([url for url in imgurl_list if 'wm_1' in url])) #无水印图片链接
    plant_imgs = list(set([url for url in imgurl_list if 'prv_1' in url])) #有水印图片链接
    if plant_imgs == []:
        raise BussinessException("小红书图文接口信息提取失败")
    detail_dict = {} #定义一个字典 以字典的格式返回数据
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "first_img": real_imgs[0], "plant_imgs": plant_imgs, "real_imgs": real_imgs})
    return detail_dict


def format_url(url: str) -> str:
    """
        把html转换成二进制
    """
    return bytes(url, "utf-8").decode("unicode_escape")


def get_video_link(html: str) -> dict:
    """
        提取无水印得video_url
    """
    title = lxml.etree.HTML(html).xpath("//title/text()")[0]  # 标题
    html = html.replace("\\u002F", "/").replace("\n", "").replace(" ", "").replace("[话题]#", "")
    desc = re.search(r'"desc":"(.*?)"', html).group(1)  # 文案
    tags = re.findall(r"#(\w+)", desc)  # 标签
    pattern = r'"originVideoKey":"([^"]*)"'
    match = re.search(pattern, html)
    if match.group(1) == "":
        raise BussinessException("小红书视频接口请求失败")
    video_url = format_url(f"https://sns-video-hw.xhscdn.com/{match.group(1)}")
    # 音频文件，无音频的视频文件，接口里面没有，返回空
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "mp3": "", "video_without_mp3": "", "real_video_url": video_url})
    return detail_dict


def parse_real_videoUrl(url: str) -> dict:
    html = get_real_html(url)
    return get_video_link(html)

def analyze_redbook(redbook_share_url: str):
    # 传入参数 --> 小红书分享的url
    user_input_url = redbook_share_url

    html = get_real_html(redbook_real_weburl(user_input_url))
    if "originVideoKey" in html:
        real_video_detail = parse_real_videoUrl(redbook_real_weburl(redbook_share_url))
        return real_video_detail
    else:
        real_img_detail = redbook_real_imgurl(html)
        return real_img_detail