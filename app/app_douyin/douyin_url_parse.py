import re
import random
import requests
import http.client
from fake_useragent import UserAgent
from models.BussinessException import BussinessException

def parse_share_id(share_url: str) -> str:
    """
        解析分享的url指向的网页视频url
    """
    path = share_url.split("v.douyin.com")[1]
    conn = http.client.HTTPSConnection('v.douyin.com')
    headers = {
        'Host': 'v.douyin.com',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': UserAgent().random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    conn.request('GET', '%s' % path, headers=headers)
    response = conn.getresponse()
    response_text = response.read().decode('utf-8')
    # 使用正则表达式提取href属性
    href_match = re.search(r'href="([^"]+)"', response_text)
    if href_match.group(1) == "":
        raise BussinessException("抖音分享的url指向的网页视频url解析失败")

    href_value = href_match.group(1)

    try:
        # 抖音笔记链接
        note_id_match = re.search(r'/note/(\d+)/', href_value)
        return note_id_match.group(1)
    except:
        # 抖音视频链接
        video_id_match = re.search(r'/video/(\d+)/', href_value)
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

def parse_real_imgurl(web_img_url: str) -> list:
    """
        解析抖音无水印的图片url链接
    """
    headers = {
        'authority': 'www.douyin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '__ac_nonce=06192fe1600efd2f548a4; __ac_signature=_02B4Z6wo00f010oZ.OAAAIDDSL4VSgFGbQNKOPhAALMfzkcLVN8kvHY8F8.4A5amrjhSxq1fBh5cV3Mb3lmu6n1vBZEZ7g2-OJbAE0HGGN.q9D4vlb32.SAnb8XjxYYKuIgSkmi4eQazA1DF9a',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': UserAgent().random,
    }

    response = requests.get(web_img_url, headers=headers)
    pattern = re.compile(r'src="(https\:\/\/[^"]+?tplv\-dy\-aweme\-images:[^"]+)"')

    # 提取所有的图片并去重
    img_links = pattern.findall(response.text.replace("amp;", ""))
    if img_links == []:
        raise BussinessException("抖音图文链接信息提取失败")
    img_links = list(set(img_links))
    return img_links

def return_detail_url(web_video_url: str) -> str:
    """
        解析实际有用的接口链接
    """
    web_video_id = web_video_url.split("video/")[1]
    if web_video_id == []:
        raise BussinessException("提取抖音网页链接video_id失败")
    detail_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={web_video_id}"

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
    ttwid_value = "ttwid=" + re.search(r'"ttwid":"(.*?)"', data.decode("utf-8")).group(1)
    if ttwid_value == "":
        raise BussinessException("ttwid获取失败")
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

    response = requests.post(detail_url, headers=headers)
    title = re.search(r'"title":"(.*?)"', response.text).group(1)  # 标题
    html = response.text.replace("\\u002F", "/").replace("\n", "").replace(" ", "")
    desc = re.search(r'"desc":"(.*?)"', html).group(1)  # 文案
    tags = re.findall(r"#(\w+)", desc)  # 标签
    mp3 = re.search(r'"uri":"(https\:\/\/.*?\.mp3)"', html).group(1) #音频
    real_video_id = response.json()['aweme_detail']['video']['play_addr']['uri']
    if real_video_id == "":
        raise BussinessException("抖音video_id获取失败")
    video_url = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + real_video_id + "&ratio=720p&line=0"
    # 无音频的视频文件，接口里面没有，返回空
    detail_dict = {}
    detail_dict.update({"title": title, "desc": desc, "tags": tags, "mp3": mp3, "video_without_mp3": "", "real_video_url": video_url})
    return detail_dict

def analyze_douyin(douyin_share_url: str):
    """
        如果返回为空字符串表示没有成功解析
    """
    # 传入参数 --> 抖音分享的url
    if "图文" in douyin_share_url:
        share_url = re.search(r'https?://\S+', douyin_share_url)
        if share_url == None:
            raise BussinessException("链接提取失败")
        web_url = "https://www.douyin.com/note/" + parse_share_id(share_url.group())
        real_download_url = parse_real_imgurl(web_url)
    else:
        share_url = re.search(r'https?://\S+', douyin_share_url)
        if share_url == None:
            raise BussinessException("链接提取失败")
        web_url = "https://www.douyin.com/video/" + parse_share_id(share_url.group())
        detail_url = return_detail_url(web_url)
        cookie = get_ttwid(detail_url)
        real_download_url = parse_real_video(web_url, detail_url, cookie)
    return real_download_url