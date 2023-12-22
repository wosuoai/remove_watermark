import re
from core.logger import logger
import requests
import http.client
from fake_useragent import UserAgent
from models.BussinessException import BussinessException
from core.set_proxy import useable_ip

proxies = useable_ip()

def parse_share_id(share_url: str) -> str:
    """
        解析分享的url指向的网页视频url
    """
    headers = {
        'Host': 'v.douyin.com',
        'user-agent': UserAgent().random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }
    response_text = requests.get(share_url, headers=headers, allow_redirects=False, proxies=proxies).text
    # 使用正则表达式提取href属性
    href_match = re.search(r'href="([^"]+)"', response_text)
    if href_match.group(1) == "":
        logger.error("抖音分享url指向网页url解析失败")
        raise BussinessException("抖音分享url指向网页url解析失败")

    href_value = href_match.group(1)
    logger.debug(f"抖音分享url指向网页url的值是：{href_value}")

    try:
        # 抖音笔记链接
        note_id_match = re.search(r'/note/(\d+)/', href_value)
        logger.debug(f"抖音网页端图文实际链接：{note_id_match.group(1)}")
        return note_id_match.group(1)
    except:
        # 抖音视频链接
        video_id_match = re.search(r'/video/(\d+)/', href_value)
        logger.debug(f"抖音网页端视频实际链接：{video_id_match.group(1)}")
        return video_id_match.group(1)

def get_ac_nonce() -> str:
    """
        抖音__ac_nonce参数
    """
    sess = requests.session()
    headers_base = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua":"\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    sess.headers = headers_base
    url = 'https://www.douyin.com'
    __ac_nonce = sess.get(url, headers=headers_base).cookies.get('__ac_nonce')
    return __ac_nonce

def parse_real_imgurl(share_url: str, web_img_url: str) -> dict:
    """
        解析抖音无水印的图片url链接
    """
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cookie': '__ac_nonce=06192fe1600efd2f548a4; __ac_signature=_02B4Z6wo00f010oZ.OAAAIDDSL4VSgFGbQNKOPhAALMfzkcLVN8kvHY8F8.4A5amrjhSxq1fBh5cV3Mb3lmu6n1vBZEZ7g2-OJbAE0HGGN.q9D4vlb32.SAnb8XjxYYKuIgSkmi4eQazA1DF9a',
        'user-agent': UserAgent().random,
    }
    try:
        tags = re.findall(r"#(\w+)", share_url.replace(" ",""))  # 标签
        tags[-1] = tags[-1].split("https")[0]
    except Exception as error:
        tags = []
    logger.debug(f"抖音图文标签是：{tags}")

    try:
        match = re.search(r'(.*?)#', share_url.replace(" ","")).group(1) #正文
        desc = re.findall(r'\w+', match)
    except Exception as error:
        desc = ""
    logger.debug(f"抖音图文文案是：{desc}")

    response = requests.get(web_img_url, headers=headers, proxies=proxies).text
    html = response.replace("\\u002F", "/").replace("\n", "").replace(" ", "")
    logger.debug(f"抖音图文接口返回信息是：{html}")
    mp3 = re.search(r'src="(https\:\/\/sf3-cdn-tos.douyinstatic.com.*?)"', html).group(1)  # 音频
    logger.debug(f"抖音图文音频是：{mp3}")
    pattern = re.compile(r'src="(https\:\/\/[^"]+?tplv\-dy\-aweme\-images:[^"]+)"')
    # 提取所有的图片并去重
    img_links = pattern.findall(response.replace("amp;", ""))
    if img_links == []:
        logger.error("抖音图文链接信息提取失败")
        raise BussinessException("抖音图文链接信息提取失败")
    img_links = list(set(img_links))
    logger.debug(f"抖音图文链接：{img_links}")
    # 标题和上传平台带水印的图片链接，接口里面没有，返回空
    detail_dict = {}  # 定义一个字典 以字典的格式返回数据
    detail_dict.update({"title": "", "desc": desc[-1], "tags": tags, "music": mp3, "first_img": img_links[0],"plant_imgs": [],"real_imgs": img_links, "link_type": 0, "method_code": 0})
    logger.debug(f"抖音图文返回的信息：{detail_dict}")
    return detail_dict

def return_detail_url(web_video_url: str) -> str:
    """
        解析实际有用的接口链接
    """
    web_video_id = web_video_url.split("video/")[1]
    logger.debug(f"抖音网页链接video_id是：{web_video_id}")
    if web_video_id == []:
        logger.error("提取抖音网页链接video_id失败")
        raise BussinessException("提取抖音网页链接video_id失败")
    detail_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={web_video_id}"
    logger.debug(f"抖音视频实际调用的接口：{detail_url}")

    return detail_url

def get_ttwid(detail_url: str) -> str:
    """
        # 通过接口拿到随机的ttwid
    """
    conn = http.client.HTTPSConnection("tk.nsapps.cn")

    payload = '{\n  \"url\": \"%s\",\n  \"userAgent\": \"%s\"\n}' %(detail_url,UserAgent().random)

    headers = {'content-type': "application/json"}

    conn.request("POST", "/", payload, headers)

    res = conn.getresponse()
    data = res.read()
    ttwid_value = re.search(r'"ttwid":"(.*?)"', data.decode("utf-8")).group(1)
    if ttwid_value == "":
        logger.error("ttwid获取失败")
        raise BussinessException("ttwid获取失败")
    ttwid_value = "ttwid=" + ttwid_value
    return ttwid_value


# def get_ttwid():
#     try:
#         url = 'https://ttwid.bytedance.com/ttwid/union/register/'
#         data = {
#             "region": "cn",
#             "aid": 1768,
#             "needFid": False,
#             "service": "www.ixigua.com",
#             "migrate_info": {"ticket": "", "source": "node"},
#             "cbUrlProtocol": "https",
#             "union": True
#         }
#
#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(url, json=data, headers=headers)
#
#         set_cookie = response.headers.get('set-cookie', '')
#         regex = re.compile(r'ttwid=([^;]+)')
#         match = regex.search(set_cookie)
#
#         return "ttwid=" + match.group(1) if match else ''
#     except Exception as error:
#         print(error)
#         return ''

def parse_real_video(web_video_url: str, detail_url: str, cookie: str) -> dict:
    """
        解析无水印的url链接
    """
    headers = {
        "accept": "application/json, text/plain, */*",
        "cookie": cookie,
        "referer": web_video_url,
        "user-agent": UserAgent().random,
    }

    response = requests.post(detail_url, headers=headers, proxies=proxies)
    logger.debug(f"抖音视频接口返回的信息：{response.text}")
    title = re.search(r'"title":"(.*?)"', response.text).group(1)  # 标题
    logger.debug(f"抖音视频的标题是：{title}")
    html = response.text.replace("\\u002F", "/").replace("\n", "").replace(" ", "")
    desc = re.search(r'"desc":"(.*?)"', html).group(1)  # 文案
    logger.debug(f"抖音视频的文案是：{desc}")
    tags = re.findall(r"#(\w+)", desc)  # 标签
    logger.debug(f"抖音视频的标签是：{tags}")
    mp3 = re.search(r'"uri":"(https\:\/\/.*?\.mp3)"', html).group(1) #音频
    logger.debug(f"抖音视频的音频是：{mp3}")
    real_video_id = response.json()['aweme_detail']['video']['play_addr']['uri']
    logger.debug(f"抖音视频的无水印视频id是：{real_video_id}")
    if real_video_id == "":
        logger.error("抖音video_id获取失败")
        raise BussinessException("抖音video_id获取失败")
    video_url = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + real_video_id + "&ratio=720p&line=0" #无水印视频链接
    # 无音频的视频文件，接口里面没有，返回空
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "music": mp3, "video_without_mp3": "", "real_video_url": video_url, "link_type": 1, "method_code": 0})
    logger.debug(f"抖音视频返回的信息：{detail_dict}")
    return detail_dict

def analyze_douyin(douyin_share_url: str):
    """
        如果返回为空字符串表示没有成功解析
    """
    logger.debug(f"拿到的可用ip是：{proxies}")
    # 传入参数 --> 抖音分享的url
    logger.info(f"抖音传入的url是：{douyin_share_url}")
    share_url = re.search(r'https?://\S+', douyin_share_url)
    if share_url == None:
        logger.error("抖音分享链接提取失败")
        raise BussinessException("抖音分享链接提取失败")
    if "图文" in douyin_share_url:
        web_url = "https://www.douyin.com/note/" + parse_share_id(share_url.group())
        real_download_url = parse_real_imgurl(douyin_share_url,web_url)
    else:
        web_url = "https://www.douyin.com/video/" + parse_share_id(share_url.group())
        detail_url = return_detail_url(web_url)
        cookie = get_ttwid(detail_url)
        real_download_url = parse_real_video(web_url, detail_url, cookie)
    return real_download_url